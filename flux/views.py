from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import CharField, Value
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from itertools import chain

from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from account.models import UserFollows


@login_required
def create_ticket(request):
    """
    Creates a ticket
    :param request: http request
    :return: render template
    """

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            created_ticket = form.save(commit=False)
            created_ticket.user = request.user
            created_ticket.save()
            messages.success(request, f"Le ticket {created_ticket} a été créé.")
            return redirect("index")
    else:
        form = TicketForm()

    return render(request, 'flux/create_ticket.html', {'section': 'posts', "method": request.method, "form": form})


@login_required
def edit_ticket(request, pk):
    """
    edit a ticket
    :param request: http request
    :param pk: id of the ticket
    :return: render template
    """
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            updated_ticket.user = request.user
            updated_ticket.save()
            messages.success(request, f"Le ticket {updated_ticket} a été mis à jour.")
            return redirect("posts")
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'flux/create_ticket.html', {'section': 'posts', "method": request.method, "form": form})


@login_required
def create_review_from_ticket(request, pk=None):
    """
    Creates a review in response to a ticket
    :param request:
    :param pk: ticket id
    :return:
    """
    ticket = None
    form_review = None
    if request.method == 'GET':
        if pk is not None:
            # Get ticket information
            ticket = get_object_or_404(Ticket, pk=pk)
            form_review = ReviewForm(initial={'user': request.user, 'ticket': ticket})
    else:
        # Creates the review
        form_review = ReviewForm(request.POST)
        if form_review.is_valid():
            created_review = form_review.save(commit=False)
            created_review.user = request.user
            created_review.ticket = get_object_or_404(Ticket, pk=pk)
            created_review.ticket.save()
            created_review.save()
            messages.success(request, f"La critique {created_review} a été créée")
            return redirect("index")

    return render(request, 'flux/create_review.html',
                  {"section": 'posts', "method": request.method,
                   "form_review": form_review, 'ticket': ticket})


@login_required
def edit_review(request, pk):
    """
    Edit a review
    :param request:
    :param pk: ticket id
    :return:
    """
    review = get_object_or_404(Review, pk=pk)
    ticket_id = review.ticket.id
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form_review = ReviewForm(initial={'user': request.user, 'ticket': ticket}, instance=review)

    if request.method == 'POST':
        form_review = ReviewForm(request.POST, instance=review)
        if form_review.is_valid():
            updated_review = form_review.save(commit=False)
            updated_review.user = request.user
            updated_review.ticket = ticket
            updated_review.save()
            messages.success(request, f"La critique {updated_review} a été mise à jour")
            return redirect("posts")

    return render(request, 'flux/create_review.html',
                  {"section": 'posts', "method": request.method,
                   "form_review": form_review, 'ticket': ticket})


@login_required
def create_review(request):
    """
    Creates a review and a ticket
    """
    form_ticket = TicketForm()
    form_review = ReviewForm()
    if request.method == 'POST':
        form_ticket = TicketForm(request.POST, request.FILES)
        form_review = ReviewForm(request.POST)
        if all([form_ticket.is_valid(), form_review.is_valid()]):
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, f"La critique {review} a été créée")
            return redirect("index")

    return render(request, 'flux/create_review.html',
                  {"section": 'posts', "form_ticket": form_ticket, "form_review": form_review})


def get_users_viewable_tickets(user):
    """
    Returns list of tickets from users followed
    """
    followed_users = UserFollows.objects.filter(user_id=user.id)
    users_viewable_tickets = [user.followed_user_id for user in followed_users]
    tickets = Ticket.objects.filter(user_id__in=users_viewable_tickets)
    return tickets


def get_users_viewable_reviews(user):
    """
    Returns list of reviews to display: from users followed + request.user
    also reviews from user not followed in response to request.user ticket
    """
    followed_users = UserFollows.objects.filter(user_id=user.id)
    users_viewable_reviews = [user.followed_user_id for user in followed_users]
    # Add current user
    users_viewable_reviews.append(user.id)
    reviews = Review.objects.filter(user_id__in=users_viewable_reviews)
    return reviews


@login_required
def feed(request):
    """
    Display feed of the current user
    """
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    followed_users = UserFollows.objects.filter(user_id=request.user.id)

    # Get ticket review
    for ticket in tickets:
        if ticket.review_set.all():  # has a review
            review = ticket.review_set.filter(ticket=ticket)
            ticket.rev = review.first()

    # # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'flux/index.html',
                  context={'posts': posts, 'followed_users': followed_users, 'section': 'flux'})


def get_user_posts(user):
    """
    Returns list of tickets and reviews from current user
    """
    tickets = Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return posts


@login_required
def user_posts(request):
    user = request.user
    posts = get_user_posts(user)

    return render(request, 'flux/posts.html',
                  context={'posts': posts, 'section': 'posts'})


# todo ajouter login required
class TicketDeleteView(SuccessMessageMixin, DeleteView):
    model = Ticket
    template_name = 'flux/ticket_delete_form.html'
    success_message = "Le ticket a été supprimé"
    success_url = reverse_lazy('posts')


class ReviewDeleteView(SuccessMessageMixin, DeleteView):
    model = Review
    template_name = 'flux/review_delete_form.html'
    success_message = "La critique a été supprimée"
    success_url = reverse_lazy('posts')
