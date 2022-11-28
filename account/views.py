from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import UserFollows


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

    def render_user_detail(error_message=""):
        return render(request,
                      'account/user/detail.html',
                      {'section': 'abonnements',
                       'user': user,
                       'usersfollowed': users_followed_queryset,
                       'followers': followers_queryset,
                       'error_message': error_message})

    related_user = ''

    # Case no action, initial view
    if request.method == 'GET':
        return render_user_detail()

    elif request.method == 'POST' and not request.POST.get('id') and not request.POST.get('username').strip():
        return render_user_detail("Merci de renseigner un nom d'utilisateur")

    # Case action (post request)
    # Get user to follow or unfollow
    elif request.POST.get('id'):  # From unfollow form
        user_id = request.POST.get('id')
        try:
            related_user = User.objects.get(id=user_id)
        except (ValueError, User.DoesNotExist):
            return render_user_detail("Cet utilisateur n'existe pas ou plus.")

    elif request.POST.get('username'):  # From follow form
        username = request.POST.get('username')
        try:
            related_user = User.objects.get(username=username)

        except (ValueError, User.DoesNotExist):
            return render_user_detail("Cet utilisateur n'existe pas ou plus.")

    # Get action (follow / unfollow)
    action = request.POST.get('action')

    if related_user and action:
        try:
            if action == 'follow':
                UserFollows.objects.get_or_create(user=request.user, followed_user=related_user)
            else:
                UserFollows.objects.filter(user=request.user, followed_user=related_user).delete()
            return HttpResponseRedirect(reverse('user_detail'))
        except (ValueError, User.DoesNotExist):
            return render_user_detail("Cet utilisateur n'existe pas ou plus.")
