from django.urls import path

from . import views

app_name = "mypoll"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("warmhot",views.warmHot , name = "warmhot"),
    path("private/", views.private_questions , name="private_questions"),
    path('private/<int:question_id>/', views.private_question_detail, name='private_question_detail'),
]