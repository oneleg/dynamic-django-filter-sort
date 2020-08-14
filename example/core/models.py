from django.db import models

# Create your models here.
class Lesson(models.Model):
    name = models.CharField(max_length=40)
    unit = models.IntegerField(default=1)

class Course(models.Model):
    name = models.CharField(max_length=40)
    lessons = models.ManyToManyField(Lesson)

    def lessons_count(self):
        return self.lessons.all().count()