from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import VideoUploadForm
from .utils import run_prediction
import os
import uuid
from django.conf import settings
from glob import glob

def home(request):
    result = None
    frames = []
    video_url = None
    unique_id = str(uuid.uuid4())

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle video upload
            video = request.FILES['video']

            # Create upload directory
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', unique_id)
            os.makedirs(upload_dir, exist_ok=True)

            # Save video
            video_path = os.path.join(upload_dir, video.name)
            with open(video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)

            # Run prediction with default sequence_length=60
            model_path = os.path.join(settings.BASE_DIR, 'DeepFakeApp', 'model', 'model.pt')
            frames_output_dir = os.path.join(upload_dir, 'extracted_frames')
            result_status, confidence = run_prediction(
                video_path=video_path,
                model_path=model_path,
                frames_output_dir=frames_output_dir
            )

            # Prepare results
            is_fake = result_status == 'FAKE'
            
            # Get frame paths
            frame_files = sorted(glob(os.path.join(frames_output_dir, '*.png')))
            frames = [os.path.join(settings.MEDIA_URL, 'uploads', unique_id, 'extracted_frames', os.path.basename(f)) for f in frame_files]
            
            # Get video URL
            video_url = os.path.join(settings.MEDIA_URL, 'uploads', unique_id, video.name)

            result = {
                'is_fake': is_fake,
                'accuracy': round(confidence, 2)
            }
    else:
        form = VideoUploadForm()

    return render(request, 'home.html', {
        'form': form,
        'frames': frames,
        'result': result,
        'video_path': video_url
    })
