from django.shortcuts import render
from .models import UploadedImage
from .forms import UploadImageForm
from django.http import HttpResponseRedirect

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            modelff = UploadedImage(image=request.FILES['image'])	
            url = str(modelff.image.url)
            modUrl = url.replace("/media/","media/uploads/")
            uploaded_image = form.save(commit=False)
            uploaded_image.vehicle_number = extract_number(modUrl)
            uploaded_image.save()
            form.save()
            return HttpResponseRedirect('/upload/')
    else:
        form = UploadImageForm()
    images = UploadedImage.objects.all()
    return render(request, 'upload_image.html', {'form': form, 'images': images})



def extract_number(image):
 import cv2
 from matplotlib import pyplot as plt
 import numpy as np
 import imutils
 import easyocr
 print(image)
 img = cv2.imread(image)
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

 bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
 edged = cv2.Canny(bfilter, 10, 50) #Edge detection
 plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

 keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 contours = imutils.grab_contours(keypoints)
 contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

 location = None
 for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
 mask = np.zeros(gray.shape, np.uint8)
 new_image = cv2.drawContours(mask, [location], 0,255, -1)
 new_image = cv2.bitwise_and(img, img, mask=mask)

 (x,y) = np.where(mask==255)
 (x1, y1) = (np.min(x), np.min(y))
 (x2, y2) = (np.max(x), np.max(y))
 cropped_image = gray[x1:x2+1, y1:y2+1]
 reader = easyocr.Reader(['en'])
 result = reader.readtext(cropped_image)
 for out in result:
    text_box, text, text_score = out
 return text
