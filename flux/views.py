from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import CharField, Value

from itertools import chain

from .forms import TicketForm
from .models import Ticket
from account.models import UserFollows


@login_required
def edit_ticket(request, pk=None):
    if pk is not None:
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        ticket = None

    if request.method == "POST":
        form = TicketForm(request.POST,  request.FILES, instance=ticket, initial={'user': request.user})
        if form.is_valid():
            updated_ticket = form.save()
            if ticket is None:
                messages.success(request, f"Le ticket {updated_ticket} a été créé.")
            else:
                messages.success(request, f"Le ticket {updated_ticket} a été mis à jour.")

            return redirect("edit_ticket", updated_ticket.pk)
    else:
        form = TicketForm(instance=ticket, initial={'user': request.user})

    return render(request, 'flux/create_ticket.html', {'section': 'posts', "method": request.method, "form": form})


def get_users_viewable_tickets(user):
    followed_users = UserFollows.objects.filter(user_id=user.id)
    followed_users_ids = [user.followed_user_id for user in followed_users]
    tickets = Ticket.objects.filter(user_id__in=followed_users_ids)
    return tickets


@login_required
def feed(request):
    # reviews = get_users_viewable_reviews(request.user)
    # # returns queryset of reviews
    # reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    # tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    return render(request, 'flux/index.html', context={'tickets': tickets, 'section': 'flux'})

    # # combine and sort the two types of posts
    # posts = sorted(
    #     chain(reviews, tickets),
    #     key=lambda post: post.time_created,
    #     reverse=True
    # )
    # return render(request, 'index.html', context={'posts': posts})



