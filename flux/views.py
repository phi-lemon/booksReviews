from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import CharField, Value

from itertools import chain

from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from account.models import UserFollows


@login_required
def edit_ticket(request, pk=None):
    """
    Creates or edit a ticket
    :param request: http request
    :param pk: id of the ticket, None if url is 'ticket/new/'
    :return: render template
    """
    if pk is not None:
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        ticket = None

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            updated_ticket.user = request.user
            updated_ticket.save()
            if ticket is None:
                messages.success(request, f"Le ticket {updated_ticket} a été créé.")
            else:
                messages.success(request, f"Le ticket {updated_ticket} a été mis à jour.")

            return redirect("edit_ticket", updated_ticket.pk)
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
            # created_review = form_review.save()
            created_review = form_review.save(commit=False)
            created_review.user = request.user
            created_review.ticket = get_object_or_404(Ticket, pk=pk)  # new
            created_review.ticket.save()  # new
            created_review.save()  # new
            messages.success(request, f"La critique {created_review} a été créée")
            return redirect("index")

    return render(request, 'flux/create_review.html',
                  {"section": 'posts', "method": request.method,
                   "form_review": form_review, 'ticket': ticket})


@login_required
def create_review(request):
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
    Returns list of users to display tickets from (users followed + request.user)
    """
    followed_users = UserFollows.objects.filter(user_id=user.id)
    users_viewable_tickets = [user.followed_user_id for user in followed_users]
    tickets = Ticket.objects.filter(user_id__in=users_viewable_tickets)
    return tickets


def get_users_viewable_reviews(user):
    """
    Returns list of users to display reviews from (users followed + request.user)
    """
    followed_users = UserFollows.objects.filter(user_id=user.id)
    users_viewable_reviews = [user.followed_user_id for user in followed_users]
    # Add current user
    users_viewable_reviews.append(user.id)
    reviews = Review.objects.filter(user_id__in=users_viewable_reviews)
    return reviews


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

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
    return render(request, 'flux/index.html', context={'posts': posts, 'section': 'flux'})


@login_required
def my_posts(request):
    pass
