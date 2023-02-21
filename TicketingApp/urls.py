from django.urls import path
from . import views

app_name = 'TicketingApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('view/', views.view, name='view'),
    path('view/<int:ticket_id>/', views.view, name='view'),
    path('view/<int:ticket_id>/edit/', views.edit, name='edit'),
    path('view/<int:ticket_id>/delete/', views.delete, name='delete'),
    path('view/<int:ticket_id>/resolve/', views.resolve, name='resolve'),
    path('view/<int:ticket_id>/close/', views.close, name='close'),
    path('view/<int:ticket_id>/reopen/', views.reopen, name='reopen'),
    path('view/<int:ticket_id>/comment/', views.comment, name='comment'),
    path('view/<int:ticket_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('view/<int:ticket_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
]
