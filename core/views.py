from django.db.models import query
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import *
from .pagination import CustomPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .utils import get_and_authenticate_user, create_user_account
from rest_framework import status
from django.contrib.auth import get_user_model, logout, login
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import User
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from .permissions import *
from rest_framework.filters import *
from django.db.models import Q

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import check_password

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .decorators import validate_request_data
from .utils import generate_qr
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.csrf import csrf_exempt
import json

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import *
from django.urls import reverse_lazy
from django.utils import timezone




# UserProfile

class UserProfileView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_field = 'pk'
      

    def get_queryset(self, *args, **kwargs):
        users = User.objects.filter(id=self.request.user.id)
        return users


class UserProfileEditView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        users = User.objects.filter(id=self.request.user.id)
        return users


class UserProfileDeleteView(generics.RetrieveDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_field = 'pk'
      

    def get_queryset(self, *args, **kwargs):
        users = User.objects.filter(id=self.request.user.id)
        return users
      


class QrCodeView(generics.ListCreateAPIView):
    queryset = QRCode.objects.all()
    serializer_class = QrCodeSerializer

    def get_quertset(self):
        return QRCode.objects.get(participant=self.request.user.username)


# Category

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsOwnerOrReadOnly,]


class CategoryDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly,]


# Event

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventListCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizer,]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class EventUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly,]


class EventDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsOwnerOrReadOnly,]



# Commnent

class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['event', 'user__username']

    def get_queryset(self):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(event__icontains=query) |
                Q(event__icontains=query)
            ).distinct()
        return queryset_list


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    


# MyEvents

class MyEventView(generics.ListAPIView):
    serializer_class = MyEventSerializer
    permission_classes = [IsOwnerOrReadOnly,]
  
    def get_queryset(self, *args, **kwargs):
        event = Event.objects.filter(owner=self.request.user.id)
        print(event)
        return event


class MyEventEditView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = MyEventSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        event = Event.objects.filter(id=self.request.user.id)
        return event

class MyEventDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = MyEventSerializer
    permission_classes = [IsOwnerOrReadOnly,]

    def get_queryset(self, *args, **kwargs):
        event = Event.objects.filter(id=self.request.user.id)
        return event





#--------------for discharge patient bill (pdf) download and printing


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request, qrcodeID, userID, eventID):
    qrcode = QRCode.objects.get(id=qrcodeID)
    user=User.objects.get(id=userID)
    event=Event.objects.get(id=eventID)
    mydict={
        'fullName':user.full_name,
        'UserPhoneNumber':user.phone_number,

        'eventTitle':event.title,
        'eventLocation':event.location,
        'eventStartDate':event.start_date,
        'eventEndDate':event.end_date,
        'eventStartTime':event.start_time,
        'eventEndTime':event.end_time,

        'qrCode': qrcode.qr_code
    }
    return render_to_pdf('core/download_pdf.html',mydict)




# class UserList(generics.ListAPIView):
#     serializer_class = UserSerializer

#     def get_queryset(self, *args, **kwargs):
#         is_participant = self.request.POST.get('is_participant', 'True')
#         return User.objects.filter(is_participant=is_participant)
        

def organizer_send_notification_participant(request):
    is_participant = request.POST.get('is_participant', 'True')
    participants=User.objects.filter(is_participant=is_participant)
    return render(request,'participant_notification.html',{"participants":participants})


@csrf_exempt
def send_participant_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    participant=User.objects.get(id=id)
    token=participant.fcm_token
    print(message)
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Event Management System",
            "body":message,
        },
        "to":token
    }
    notification=Notification(participant_id=participant, message=message)
    notification.save()
    return HttpResponse("True")




#####

def participant_all_notification(request):
    participant=User.objects.get(id=request.user.id)
    notifications=Notification.objects.filter(participant_id=participant.id)
    return render(request,"all_notification.html",{"notifications":notifications})



def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.6.8/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.6.8/firebase-analytics.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyAQEiRl5hY5Wifrs-RhhvNk28NJEplA5fc",' \
         '        authDomain: "notification-d0baf.firebaseapp.com",' \
         '        projectId: "notification-d0baf",' \
         '        storageBucket: "notification-d0baf.appspot.com",' \
         '        messagingSenderId: "884861487621",' \
         '        appId: "1:884861487621:web:f2a7a2b87d6e09b8cbea6c",' \
         '        measurementId: "G-N14YB4MRVE"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


@csrf_exempt
def participant_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        participant=User.objects.get(id=request.user.id)
        participant.fcm_token=token
        participant.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")



# class OrganizerCreateChat(LoginRequiredMixin, CreateView):
#     form_class = ChatForm
#     model = Chat
#     template_name = 'organizer_chat_form.html'
#     success_url = reverse_lazy('organizer-chatlist')


#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)


# class OrganizerListChat(LoginRequiredMixin, ListView):
#     model = Chat
#     template_name = 'organizer_chat_list.html'

#     def get_queryset(self):
#         return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')




# class ParticipantCreateChat(LoginRequiredMixin, CreateView):
#     form_class = ChatForm
#     model = Chat
#     template_name = 'participant_chat_form.html'
#     success_url = reverse_lazy('participant-chatlist')


#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)




# class ParticipantListChat(LoginRequiredMixin, ListView):
#     model = Chat
#     template_name = 'participant_chat_list.html'

#     def get_queryset(self):
#         return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')




