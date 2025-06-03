from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE=(
        ('employer','Employer'),
        ('jobseeker','Job seeker')
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type=models.CharField(max_length=10,choices=USER_TYPE)
    def __str__(self):
        return self.user.username
class Job(models.Model):
    title=models.CharField(max_length=100)
    company=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    posted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Application(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    applicant=models.ForeignKey(User,on_delete=models.CASCADE)
    resume=models.FileField(upload_to='resume/')
    applied_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"


    

# Create your models here.
