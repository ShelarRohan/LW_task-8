
from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import CarForm
from .models import Image
import cv2
import numpy as np
import numpy
import pytesseract
import requests
import xmltodict
import json

import os

from django.conf import settings
from PIL import Image


from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
from django.shortcuts import render

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
    form = CarForm()
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.image = request.FILES['image']
            file_type = car.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return redirect('error')
            car.save()
            return redirect('confirmation')
    context = {"form": form,}
    return render(request, 'index.html', context)


def confirmation(request):
    car = Image.objects.last()
    return render(request, 'confirmation.html',{'car':car})

def error(request):
    return render(request, 'error.html')


def get(request):
    car = Image.objects.last()
    a = car.image
    a= str(a)
    c =a.split('/')
    print(c[2])
    path = "C:/Users/shelar/Documents/t8/media/img/21/" + c[2] 
    print(path)
    b = cv2.imread(path)
    cv2.imshow('ImageWindow', b)
    cv2.waitKey()
    gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    plate_detection = cv2.CascadeClassifier(os.path.join(
               settings.BASE_DIR, 'opencv_haarcascade_data/indian_license_plate.xml'))
    faces = plate_detection.detectMultiScale(
             gray, scaleFactor=1.2, minNeighbors=7)
    if faces is ():
        return b, []
    roi = " "
    for (x, y, w, h) in faces:
        cv2.rectangle(b, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi = b[y:y+h, x:x+w]
        roi = cv2.resize(roi, (400, 150))

    cv2.imshow('ImageWindow1', roi)
    cv2.waitKey()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(roi, config='--psm 11 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' )
    print("Detected license plate Number is:",text)
    print(text)
    text=text.replace(' ','')
    text = text[:-2] 
    p= "http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={}&username=rrr"
    print(p.format(text))
    r=requests.get(p.format(text))
    data=xmltodict.parse(r.content)
    jsonData=data['Vehicle']['vehicleJson']
    dt=json.loads(jsonData)
    return render(request,'getinfo.html',{'car':car,'text':text[:-1] ,"Description": dt["Description"],
            "RegistrationYear": dt["RegistrationYear"],
            "CarMake": dt["CarMake"]['CurrentTextValue'],
            "CarModel": dt["CarModel"]['CurrentTextValue'],		
            "Owner": dt["Owner"],
            "Insurance": dt["Insurance"],
            "Location": dt["Location"],
            "RegistrationDate": dt["RegistrationDate"],
            "EngineNumber": dt["EngineNumber"],
            "VechileIdentificationNumber": dt["VechileIdentificationNumber"],
            "ImageUrl": dt["ImageUrl"]})

