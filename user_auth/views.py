from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from home.models import CourseReview, SiteFeedback
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

    form = UpdateProfile(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                  'birth_date': request.user.birth_date, 'photo': request.user.photo})
    return render(request, 'account/update_profile.html', {'form': form})
