
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Course, Lesson, Quiz, Question, Choice, UserProgress, QuizResult
from .serializers import CourseSerializer, LessonSerializer, QuizSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
   
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        try:
            course = self.get_object()
            lessons = course.lessons.all()
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


class LessonViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class QuizViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit(self, request, pk=None):
        try:
            quiz = self.get_object()
            user = request.user
            answers = request.data.get('answers', {})

            if not isinstance(answers, dict):
                return Response({'error': 'Answers must be a dictionary.'}, status=status.HTTP_400_BAD_REQUEST)

            total_questions = quiz.questions.count()
            correct_answers = 0

            for question_id, choice_id in answers.items():
                try:
                    question = Question.objects.get(id=question_id, quiz=quiz)
                    choice = Choice.objects.get(id=choice_id, question=question)
                    if choice.is_correct:
                        correct_answers += 1
                except (Question.DoesNotExist, Choice.DoesNotExist):
                    pass
            
            score = 0
            if total_questions > 0:
                score = (correct_answers / total_questions) * 100

            result, _ = QuizResult.objects.update_or_create(
                user=user, quiz=quiz, defaults={'score': score}
            )

            if score >= 70:
                lesson = quiz.lesson
                user_progress, _ = UserProgress.objects.get_or_create(user=user, course=lesson.course)
                user_progress.completed_lessons.add(lesson)
                
                total_lessons_in_course = lesson.course.lessons.count()
                completed_lessons_count = user_progress.completed_lessons.count()
                
                if total_lessons_in_course > 0:
                    progress_percentage = (completed_lessons_count / total_lessons_in_course) * 100
                    user_progress.progress_percentage = progress_percentage
                    user_progress.save()

            return Response({
                'score': score,
                'correct_answers': correct_answers,
                'total_questions': total_questions
            }, status=status.HTTP_200_OK)

        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer 

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]