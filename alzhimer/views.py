from django.shortcuts import render
from django.http import request
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "models", "alzhemers.h5"),
    compile=False,
    safe_mode=False
)
def predict(request):
    return HttpResponse("Model temporarily disabled")
CLASS_NAMES = [ "Mild Impairment", "Moderate Impairment", "No Impairment","Very Mild Impairment" ]  # same as before

def read_file_as_image(data):
    image = Image.open(BytesIO(data)).convert("RGB")  # Ensure 3 channels
    image = image.resize((128, 128))  # Match model input size
    image = np.array(image) / 255.0   # Normalize if model was trained with normalized data
    return image


def predict(request):
    if request.method == "POST" and request.FILES.get('file'):
        image = read_file_as_image(request.FILES['file'].read())
        img_batch = np.expand_dims(image, 0)  # Add batch dimension
        predictions = MODEL.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = f"{np.max(predictions[0]):.0%}"
        return render(request, 'op.html', {
            "a": predicted_class,
            "b": confidence,
            "c": request.FILES['file'].name
        })
    return redirect('index')

def dashboard(request):
    return render(request, 'dashboard.html')

def index(request):
    return render(request,"index.html")
def donate(request):
    return render(request,"donate.html")

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/dashboard/')  # Redirect to the admin panel
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
    return render(request, 'custom_login.html')
def dashboard(request):
    return render(request,"dashboard.html")


def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to your custom login page
