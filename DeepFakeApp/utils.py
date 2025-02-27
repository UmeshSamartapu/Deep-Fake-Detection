import os
import shutil
import torch
import torchvision
from torchvision import transforms
import numpy as np
import cv2
import face_recognition
from torch import nn
from PIL import Image as pImage
from torchvision.models import ResNeXt50_32X4D_Weights
from torchvision import models
from torch.utils.data import Dataset

# Model configuration
im_size = 112
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
device = 'cuda' if torch.cuda.is_available() else 'cpu'
sm = nn.Softmax(dim=1)

train_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((im_size, im_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

class Model(nn.Module):
    def __init__(self, num_classes=2, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(weights=ResNeXt50_32X4D_Weights.IMAGENET1K_V1)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim, lstm_layers, bidirectional)
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(hidden_dim, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, -1)
        x_lstm, _ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))

class ValidationDataset(Dataset):
    def __init__(self, video_names, sequence_length=60, transform=None, frames_output_dir="extracted_frames"):
        self.video_names = video_names
        self.transform = transform
        self.sequence_length = sequence_length
        self.frames_output_dir = frames_output_dir
        os.makedirs(self.frames_output_dir, exist_ok=True)

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []
        
        print(f"\nExtracting frames from video: {video_path}")
        
        for i, frame in enumerate(self.frame_extract(video_path)):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb_frame)
            
            try:
                top, right, bottom, left = faces[0]
                original_frame = frame[top:bottom, left:right, :].copy()
                transformed_frame = frame[top:bottom, left:right, :]
            except:
                continue
            
            if self.transform:
                transformed_frame = self.transform(transformed_frame)
            frames.append(transformed_frame)
            
            # Save original frame
            frame_image = pImage.fromarray(cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB))
            frame_image.save(os.path.join(self.frames_output_dir, f"frame_{idx}_{i}.png"))
            
            # Update progress
            print(f"\rFrames processed: {len(frames)}/{self.sequence_length}", end="", flush=True)
            
            if len(frames) == self.sequence_length:
                break
        
        print("\nFrame extraction completed.")
        frames = torch.stack(frames)
        return frames.unsqueeze(0)

    def frame_extract(self, path):
        vidObj = cv2.VideoCapture(path)
        success, image = vidObj.read()
        while success:
            yield image
            success, image = vidObj.read()

def predict(model, img):
    fmap, logits = model(img.to(device))
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    confidence = logits[:, int(prediction.item())].item() * 100
    return int(prediction.item()), confidence

def load_model(model_path):
    model = Model(2).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model

def run_prediction(video_path, model_path, frames_output_dir, sequence_length=60):
    model = load_model(model_path)
    dataset = ValidationDataset(
        [video_path], 
        sequence_length=sequence_length,
        transform=train_transforms, 
        frames_output_dir=frames_output_dir
    )
    print("\nProcessing extracted frames...")
    prediction, confidence = predict(model, dataset[0])
    result = "REAL" if prediction == 1 else "FAKE"
    print(f"\nPrediction Result: {result}")
    print(f"Confidence: {confidence:.2f}%")
    return result, confidence