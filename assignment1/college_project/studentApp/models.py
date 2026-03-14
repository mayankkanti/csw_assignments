from django.db import models

class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_code = models.CharField(max_length=20)

    def __str__(self):
        return self.dept_name

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='students'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name