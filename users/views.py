from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import paginate
from .models import Profile
from .forms import CustomUserCreationForm,ProfileForm,RoleForm
from django.core.mail import send_mail
from django.conf import settings
import os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from .models import *
import cv2
#

# Create your views here.

def home(request):
    return render(request,'home.html')

def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request,'Username does not exit')
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request,'users/login_register.html')

def logoutUser(request):
    messages.error(request,'User was logged out')
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    roleform = RoleForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        roleform = RoleForm(request.POST)
        role = request.POST['role']
        if form.is_valid() and roleform.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
            profile = Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=user.first_name,
                role=role
            )

            subject = 'Welcome to MOODSENSE'
            message = 'We are glad you are here!'

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
            )
            messages.success(request,'User account was created')

            login(request,user)
            return redirect('edit-account')
        
        else:
            messages.error(request,'An error has occurred during registration')

    context={'page':page,'form':form,'roleform':roleform}
    return render(request,'users/login_register.html',context)



def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    context = {'profile':profile}
    return render(request,'users/user-profile.html',context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
   
    context={'profile':profile}
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method=='POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
            form.save()
            return redirect('account')

    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def timetable(request):
    return render(request,'timetable.html')

import logging

@login_required(login_url='login')
@csrf_exempt
def recording(request):
    if request.method == "POST":
        video_file = request.FILES.get("video_file", None)

        # Check if the file is in the MP4 format
        if video_file.content_type != "video/mp4":
            return JsonResponse({"error": "Invalid file format."})

        # Save the video file to the desired location in the 'media/recording' folder
        with open("media/recording/recording.mp4", "wb") as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        return JsonResponse({"message": "Recording saved successfully."})
    else:
        return render(request,'recording.html')

import numpy as np
import cv2
from keras.models import load_model
from django.shortcuts import render
from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.db.models import Max

def emotion_analysis(request):
    recognition_model = load_model('users/p2.h5')
    facial_dict = {0: 'fear', 1: 'happy', 2: 'neutral', 3: 'sad', 4: 'surprise'}

    video_path = "media/recording/recording.mp4"
    cap = cv2.VideoCapture(video_path)
    
    recognized_expressions = []
    
   # Create a dictionary to store the emotion percentages for each lecture
    all_lectures = []
    
  
    emotion_count = Counter()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
    
    
        bounding_box = cv2.CascadeClassifier('users/haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in num_faces:
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            rgb_frame = cv2.cvtColor(roi_gray_frame, cv2.COLOR_GRAY2RGB)
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(rgb_frame, (48, 48)), 0), -1)
            facial_prediction = recognition_model.predict(cropped_img)
            maxindex = int(np.argmax(facial_prediction))
            expression = facial_dict[maxindex]
            # cv2.putText(frame.copy(), expression, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            
            print("Recognized expression:", expression)
            recognized_expressions.append(expression)
            
            # Increment the count for this emotion
            emotion_count[expression] += 1
            
        
                
        # Calculate the total number of recognized emotions
        total_recognized = sum(emotion_count.values())
        
        # Calculate the percentage for each emotion
        emotion_percentages = {emotion: count / total_recognized * 100 for emotion, count in emotion_count.items()}
        
       
       # Fetch the latest lecture ID from the database
        latest_lecture = Lecture.objects.order_by('-lecture_id').first()

        # Calculate the next lecture ID
        if latest_lecture:
            next_lecture_id = latest_lecture.lecture_id + 1
        else:
            next_lecture_id = 1  # If there are no lectures, start with 1

        # Fetch the lecture instance you're working with (replace lecture_id with actual ID)
        lecture = Lecture.objects.create(lecture_id=next_lecture_id)
        all_lectures.append({
            'lecture_id': lecture.lecture_id,
            'emotion_percentages': emotion_percentages
        })
    cap.release()
    
    
    
    # Create Emotion instance and associate with the lecture
    emotion_instance = Emotion.objects.create(
        profile=request.user.profile,
        emotion=emotion_percentages
    )
    emotion_instance.save()
    
    
    context = {
        'all_lectures': all_lectures,
    }
    
    
    return render(request, 'emotion_analysis.html', context)


from django.shortcuts import render


def all_emotions(request):
    
    emotions = Emotion.objects.values_list('emotion', flat=True)
    return render(request, 'all_emotions.html', {'emotions': emotions})
