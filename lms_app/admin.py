

from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Choice, UserProgress, QuizResult

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserProgress)
admin.site.register(QuizResult)