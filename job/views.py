from django.shortcuts import render,redirect
from .forms import profileform,User_registration,JobForm
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job,Application
from django.http import HttpResponse
def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            auth_login(request,user)
            profile=user.profile
            if profile.user_type=='employer':
                return redirect("post_job")
            else:
                return redirect('job_listings')
        else:
            messages.error(request,'invalid credentials')
    return render(request,'job/login.html')


def home(request):
    print("home view called")
    return render(request,"job/home.html")


def signup(request):
    if request.method=='POST':
        userform=User_registration(request.POST)
        profile_form=profileform(request.POST)

        if userform.is_valid() and profile_form.is_valid():
            user=userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()

            auth_login(request,user)
            return redirect('home')
    else:
        userform=User_registration()
        profile_form=profileform()
    return render(request,'job/signup.html',{
        'userform':userform,
        'profileform':profile_form
    })


@login_required
def job_listings(request):
    if request.user.profile.user_type!='jobseeker':
        return redirect('home')
    jobs=Job.objects.all()
    return render(request, 'job/job_listings.html',{'jobs':jobs})
@login_required
def post_job(request):
    if request.user.profile.user_type!='employer':
        return redirect('home')
    if request.method=="POST":
        form=JobForm(request.POST)
        if form.is_valid():
            job=form.save(commit=False)
            job.posted_by=request.user
            job.save()
            return redirect('my_jobs')
    else:
        form=JobForm()
    return render(request,'job/post_job.html',{'form':form})

@login_required
def my_jobs(request):
    if request.user.profile.user_type != 'employer':
        return redirect('home')
    
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'job/my_jobs.html', {'jobs': jobs})
def logout_view(request):
    auth_logout(request)
    return redirect('home')
@login_required
def apply_job(request,job_id):
    if request.user.profile.user_type != 'jobseeker':
        return redirect('home')

    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        if resume:
            # prevent duplicate applications if needed
            existing = Application.objects.filter(job=job, applicant=request.user)
            if existing.exists():
                messages.error(request, "You've already applied for this job.")
                return redirect('job_listings')

            Application.objects.create(
                job=job,
                applicant=request.user,
                resume=resume
            )
            messages.success(request, "Application submitted successfully.")
            return redirect('my_applications')  # or job_listings

        else:
            messages.error(request, "Please upload a resume.")
            return redirect('job_listings')

    # If not POST, redirect or handle graceful
@login_required
def my_applications(request):
    if request.user.profile.user_type != 'jobseeker':
        return redirect('home')
    
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'job/my_applications.html', {'applications': applications})


    

# Create your views here.
