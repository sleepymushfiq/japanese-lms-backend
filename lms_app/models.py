from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=200, help_text="e.g., N5 Beginner, N4 Elementary")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    content_text = models.TextField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, related_name='quiz', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Quiz for {self.lesson.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500, help_text="Write the question here")

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False, help_text="Is this the correct answer?")

    def __str__(self):
        return f"{self.question.text[:30]}... -> {self.text}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    progress_percentage = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"Progress for {self.user.username} in {self.course.title}"
        

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(help_text="Score in percentage (e.g., 80.0)")
    completed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s score for {self.quiz.title}: {self.score}%"