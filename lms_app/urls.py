

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, QuizViewSet, UserCreateView 

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'quizzes', QuizViewSet, basename='quiz')


urlpatterns = [
    path('', include(router.urls)),
  
    path('register/', UserCreateView.as_view(), name='user-register'), 
]