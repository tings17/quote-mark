from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import (
    UserSerializer, 
    BookSerializer, 
    AnnotationSerializer, 
    CustomTokenObtainPairSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response
from rest_framework.views import APIView
from pytesseract import pytesseract
import cv2
import numpy as np
from PIL import Image
from .models import Annotation, Book

import logging
logger = logging.getLogger(__name__)

import subprocess
import logging

logger = logging.getLogger(__name__)

try:
    result = subprocess.run([settings.TESSERACT_PATH, '--version'], 
                           capture_output=True, text=True)
    logger.info(f"Tesseract version check: {result.stdout}")
except Exception as e:
    logger.error(f"Error checking tesseract: {str(e)}")


pytesseract.tesseract_cmd = settings.TESSERACT_PATH

logger.info(f"Using Tesseract path: {pytesseract.tesseract_cmd}")
logger.info(f"Tesseract path from settings: {settings.TESSERACT_PATH}")

# Also check if the file exists
import os
logger.info(f"Tesseract file exists: {os.path.exists(pytesseract.tesseract_cmd)}")

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AuthCheckView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'authenticated': True,
            'username': request.user.username,
            'user_id': request.user.id
        }, status=status.HTTP_200_OK)

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        book_id = self.request.query_params.get("id")
        if book_id:
            return Book.objects.filter(user=self.request.user, id=book_id)
        return Book.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

class AnnotationListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        book_id = self.request.query_params.get("book")
        if book_id:
            return Annotation.objects.filter(book__user=self.request.user, book_id=book_id)
        return Annotation.objects.filter(book__user=self.request.user)
    
    def perform_create(self, serializer):
        annotation_type = self.request.data.get("annotation_type", "scan")

        annotation = serializer.save()
        
        if annotation_type == "manual":
            book = annotation.book
            book.number_of_annotations = book.annotations.count()
            book.save()

        else:
            try:
                img_path = annotation.image.path
                highlighter_color = self.request.data.get("highlighter_color")
                if highlighter_color == "yellow":
                    logger.info("YELLOW")
                    print("HEREEEE")
                    annotation.image_text = extract_highlight(img_path, np.array([22, 93, 0]), np.array([40, 255, 255]))
                elif highlighter_color == "pink":
                    annotation.image_text = extract_highlight(img_path, np.array([160, 50, 100]), np.array([180, 255, 255]))
                elif highlighter_color == "blue":
                    annotation.image_text = extract_highlight(img_path, np.array([22, 93, 0]), np.array([40, 255, 255]))
                annotation.save()
            except Exception as e:
                logger.info("error processsing image" + str(e))

        book = annotation.book
        book.number_of_annotations = book.annotations.count()
        book.save()

class AnnotationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Annotation.objects.filter(book__user=self.request.user)
        book_id = self.request.query_params.get("book")
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset
    
    def perform_update(self, serializer):
        annotation = serializer.save()

        if "image" in self.request.data:
            img_path = annotation.image.path
            annotation.image_text = self.extract_highlight(img_path, np.array([22, 93, 0]), np.array([40, 255, 255]))
            annotation.save()

    def perform_destroy(self, instance):
        book = instance.book
        instance.delete()
        book.number_of_annotations -= 1
        book.save()

def extract_highlight(image, lower, upper):
    logger.info("extracting")
    img = cv2.imread(image)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_lower = np.array(lower, np.uint8)
    hsv_upper = np.array(upper, np.uint8)
    img_mask = cv2.inRange(img_hsv, hsv_lower, hsv_upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    mask_denoised = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(mask_denoised, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_mask = np.zeros_like(mask_denoised)
    cv2.drawContours(contour_mask, contours, -1, 255, -1)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 1))
    wider_mask = cv2.dilate(contour_mask, horizontal_kernel, iterations=1)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
    dilated_mask = cv2.dilate(wider_mask, vertical_kernel, iterations=1)

    smooth_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    final_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, smooth_kernel, iterations=2)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    highlighted = cv2.bitwise_and(gray, gray, mask=final_mask)
    pil_img = Image.fromarray(highlighted)

    highlighted_text = pytesseract.image_to_string(pil_img)
    logger.info(highlighted_text)

    return highlighted_text