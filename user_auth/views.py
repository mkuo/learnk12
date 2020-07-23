from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from home.forms.tutor_user_form import TutorForm, UpdateTutorForm
from home.models import CourseReview, SiteFeedback, AllTutorsPage, TutorPage
from user_auth.forms import SignUpForm, UpdateProfile


@login_required
def profile(request):
    return render(request, 'account/profile.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.photo = form.cleaned_data.get('photo')
            user.save()
            CourseReview.objects.filter(email=user.email).update(email=None, name=None, user=user)
            SiteFeedback.objects.filter(email=user.email).update(email=None, name=None, user=user)
            return redirect('account_login')
        else:
            return render(request, 'account/signup.html', {'form': form})
    form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfile(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'account/update_profile.html', {'form': form})

    form = UpdateProfile(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name})
    return render(request, 'account/update_profile.html', {'form': form})


@login_required
def create_tutor(request):
    tutor = TutorPage.objects.filter(user=request.user).first()
    if tutor:
        return redirect('update_tutor', tutor.pk)
    else:
        if request.method == 'POST':
            form = TutorForm(request.POST, user=request.user)
            all_tutors = AllTutorsPage.objects.all()[0]

            if form.is_valid():
                tutor_page = form.save(commit=False)
                all_tutors.add_child(instance=tutor_page)
                messages.success(request, 'New Tutor Created!')
                return redirect('profile')
    form = TutorForm()
    return render(request, 'home/tutor_user_page.html', {'form': form})


@login_required
def update_tutor(request, tutor_id):
    tutor = get_object_or_404(TutorPage, id=tutor_id)
    if request.method == 'POST':
        form = UpdateTutorForm(instance=tutor, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tutor successfully updated!')
            return redirect('all_tutors')

    form = UpdateTutorForm(initial={'title': tutor.user, 'course_subjects': tutor.course_subjects,
                                    'hourly_rate': tutor.hourly_rate, 'timezone': tutor.timezone,
                                    'description': tutor.description,
                                    'is_accepting_students': tutor.is_accepting_students,'public': tutor.public})
    return render(request, 'home/tutor_update_user_page.html', {'form': form})


@login_required
def user_tutors(request):
    tutors = TutorPage.objects.filter(user=request.user)
    return render(request, 'home/user_tutors.html', {'tutors': tutors})
