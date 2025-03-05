# Deep fake detection Django Application
## Requirements:

**Note :** Nvidia GPU is mandatory to run the application.
- CUDA version >= 10.0 for GPU
- GPU Compute Capability > 3.0 


You can find the list of requirements in [requirements.txt](https://github.com/UmeshSamartapu/Deep-Fake-Detection/blob/main/requirements.txt). Main requirements are listed below:

```
Python >= v3.6
Django >= v3.0
```

## Directory Structure

- DeepFakeProject/
- ├── DeepFakeApp/
- │   └── model/
- │       └── model.pt
- │   ├── migrations/
- │   ├── __init__.py
- │   ├── admin.py
- │   ├── apps.py
- │   ├── forms.py
- │   ├── models.py
- │   ├── views.py
- │   └── utils.py
- ├── DepFakeProject/
- │   ├── __init__.py
- │   ├── settings.py
- │   ├── urls.py
- │   └── wsgi.py
- ├── static/
- │   ├── css/
- │   │   └── style.css
- │   └── images/
- │       ├── background.png
- │       ├── thumbsup.png
- │       └── thumbsdown.png 
- ├── templates/
- │   ├── base.html
- │   └── home.html
- ├── media/
- │   └── uploads/
- │       └── [uuid folders will be created here automatically]
- ├── uploads/
- │   └── Elon_musk.mp4
- │   └── Obama 1.mp4
- │   └── Obama 2.mp4
- │   └── TomCruise.mp4
- └── manage.py
- └── requirements.txt

# Running application locally on your machine

#### Step 1 : Clone the repo and Navigate to Django Application

`git clone https://github.com/UmeshSamartapu/Deep-Fake-Detection.git`

#### Step 2: Create virtualenv (optional)

`python -m venv venv`

#### Step 3: Activate virtualenv (optional)

`venv\Scripts\activate`

#### Step 4: Install requirements

`pip install -r requirements.txt`

#### Step 5: Copy Models

`Copy your trained model to the models folder i.e DeepFakeProject\DeepFakeApp/model/`

- You can download our trained models from [Google Drive](https://drive.google.com/file/d/1ZPFYNaEllVp88UZXrH8VdL8BHhYT2k06/view?usp=drive_link)

### Step 6: Run project

`python manage.py runserver`

## Demo 
### You can watch the [youtube video](https://youtu.be/p1ls3xzZTwY) for demo
<p align="center">
  <img src="https://github.com/UmeshSamartapu/Deep-Fake-Detection/blob/main/static/images/DeepFakeDetectionDemo.gif" />
</p>  


## 📫 Let's Connect

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/umesh-samartapu-42793025a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://x.com/umeshsamartapu?t=graUTdTs4QlUc3a5OOH7hA&s=09)
[![Email](https://img.shields.io/badge/-Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:umeshsamartapu@gmail.com)
[![Instagram](https://img.shields.io/badge/-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/umeshsamartapu?igsh=MWsxbWVzbHd0bDgyag==)
[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20Me%20a%20Coffee-FBAD19?style=flat-square&logo=buymeacoffee&logoColor=black)](https://www.buymeacoffee.com/umeshsamartapu)

---

🔥 Always exploring new technologies and solving real-world problems with code!
