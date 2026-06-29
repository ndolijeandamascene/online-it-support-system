from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/new/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("knowledge/", views.knowledge_list, name="knowledge_list"),
    path("knowledge/<int:pk>/", views.knowledge_detail, name="knowledge_detail"),
    path("reports/", views.reports, name="reports"),
]
