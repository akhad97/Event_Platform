from django.urls import path, include
from rest_framework import routers, views
from .views import *
from . import views
from django.conf.urls.static import static



urlpatterns = [

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('comment-list/', views.CommentListAPIView.as_view(), name='comment-thread'),
    path('comment-create/', views.CommentListCreate.as_view(), name='comment-create'),
    path('comment-detail/<int:pk>/', views.CommentUpdateView.as_view(), name='comment-detail'),

    path('event-list/', EventListView.as_view(), name='event_list'),
    path('event-create/', EventListCreateView.as_view(), name='event-create'),
    path('event-detail/<int:pk>/', views.EventUpdateAPIView.as_view(), name='event-detail'),
    path('event-delete/<int:pk>/', views.EventDeleteView.as_view(), name='event-delete'),

    
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('category-create/', CategoryListCreateView.as_view(), name='category-create'),
    path('category-detail/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-detail'),
    path('category-delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user-profile-edit/<int:pk>/', views.UserProfileEditView.as_view(), name='user-profile'),
    path('user-profile-delete/<int:pk>/', views.UserProfileDeleteView.as_view(), name='user-profile'),

    path('myevents/', views.MyEventView.as_view(), name='myevents'),
    path('myevents-edit/<int:pk>/', views.MyEventEditView.as_view(), name='myevents'),
    path('myevents-delete/<int:pk>/', views.MyEventDeleteView.as_view(), name='myevents'),

    path('qrcode-create/', views.QrCodeView.as_view(), name="qrcode-create"),
    path('download-pdf/<int:userID>/<int:eventID>/<int:qrcodeID>/', views.download_pdf_view, name='download-pdf'),
    

    path('organizer_send_notification_participant/', views.organizer_send_notification_participant,name="organizer_send_notification_participant"),
    path('send_participant_notification/', views.send_participant_notification,name="send_participant_notification"),

    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('participant_fcmtoken_save', views.participant_fcmtoken_save, name="participant_fcmtoken_save"),
    path('participant_all_notification/',views.participant_all_notification,name="participant_all_notification"),
     
    # path('organizer-chat/', views.OrganizerCreateChat.as_view(), name='organizer-chat'),
    # path('organizer-chatlist/', views.OrganizerListChat.as_view(), name='organizer-chatlist'),

    # path('participant-chat/', views.ParticipantCreateChat.as_view(), name='participant-chat'),
    # path('participant-chatlist/', views.ParticipantListChat.as_view(), name='participant-chatlist'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)