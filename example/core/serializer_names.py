from core.serializers import CourseSerializer
from core.serializers import LessonSerializer

serializer_list = {
    'Course': CourseSerializer,
    'Lesson': LessonSerializer,
}