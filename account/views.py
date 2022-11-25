from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import UserFollows

from django.http import JsonResponse


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def user_detail(request):
    user = request.user
    users_followed_queryset = UserFollows.objects.filter(user_id=user.id)
    followers_queryset = UserFollows.objects.filter(followed_user_id=user.id)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'abonnements',
                   'user': user,
                   'usersfollowed': users_followed_queryset,
                   'followers': followers_queryset})


@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                UserFollows.objects.get_or_create(user=request.user, followed_user=user)
            else:
                UserFollows.objects.filter(user=request.user, followed_user=user).delete()
            return HttpResponseRedirect(reverse('user_detail'))
        except User.DoesNotExist:
            return render(request, {
                'error_message': "Cet utilisateur n'existe pas ou plus",
            })
