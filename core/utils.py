from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
import base64
import qrcode
import io


def create_user_account(email, password, username="", first_name="",
                        last_name="", **extra_fields):
    user = get_user_model().objects.create_user(
        username=email, email=email, password=password, first_name=first_name,
        last_name=last_name, **extra_fields)
    return user

def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user


def generate_qr_code(data, size=10, botder=0):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img=qr.make_image()
    return img

def generate_qr(url_text):
    generated_code= generate_qr_code(data=url_text, size=10, border=0)
    bio = io.BytesIO()
    img_save = generated_code.save(bio)
    png_qr = bio.getvalue()
    base64qr = base64.b64encode(png_qr)
    img_name = base64qr.decode('utf-8')
    context_dict = dict()
    context_dict['filte_type'] = 'png'
    context_dict['image_base64'] = img_name
    return context_dict