# generator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.thread_list, name='thread_list'),
    path('review/add/', views.add_review, name='add_review'),
    path('thread/<int:thread_id>/revise/', views.revise_thread, name='revise_thread'),
    path('thread/<int:thread_id>/apply_revision/', views.apply_revision, name='apply_revision'),
    path('thread/<int:thread_id>/copy-log/', views.log_copy, name='log_copy'),
    path('thread/<int:thread_id>/feedback/', views.thread_feedback, name='thread_feedback'),
]