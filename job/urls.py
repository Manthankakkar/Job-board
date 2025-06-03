from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('',views.home,name='home'),
     
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('post-job/', views.post_job, name='post_job'),
    path('job-listings/', views.job_listings, name='job_listings'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
]