from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm
from .models import Ticket


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "flux/index.html"


# @login_required
# def index(request):
#     return render(request, 'flux/index.html', {'section': 'flux'})


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






