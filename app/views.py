import datetime

from django.http import Http404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.timezone import now
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from braces.views import LoginRequiredMixin, OrderableListMixin

from app.range_helpers import to_local_time
from .models import Event, create_event
from .forms import EventForm


class EventListView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Event
    orderable_columns = ('start_time', 'end_time', 'duration')
    orderable_columns_default = 'time_range'
    ordering_default = 'desc'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        date_range = self.request.GET.get('date_range')

        if date_range:
            date_from, date_to = date_range.split(" to ")
            qs = qs.filter(time_range__overlap=[
                datetime.datetime.strptime(date_from, '%Y-%m-%d'),
                datetime.datetime.strptime(date_to, '%Y-%m-%d'),
            ])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['last_data'] = self.get_queryset().order_by('-time_range').first()
        return ctx


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = '/'
    success_message = "Event created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except:
            return render(request, 'app/time_collision.html', {})

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EventUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_url = '/'
    success_message = "Event successfully updated!"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_initial(self):
        event = self.get_object()

        local_start_time = to_local_time(event.start_time)
        local_end_time = to_local_time(event.end_time)
        return {
            'date': local_start_time.date(),
            'time_from': local_start_time.time(),
            'time_to': local_end_time.time() if local_end_time else None,
        }


class EventDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Event
    success_url = '/'
    success_message = "Event deleted."

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


def checkin(request):
    if request.method == 'POST':
        create_event(request.user)
    messages.add_message(request, messages.INFO, 'You have successfully checked in!')
    return redirect('/')


def checkout(request, pk):
    if request.method == 'POST':
        try:
            event = Event.objects.get(user=request.user, id=pk)
            event.time_range = [
                event.start_time,
                now()
            ]
            event.save()
        except:
            raise Http404

    messages.add_message(request, messages.INFO, 'You have successfully checked out!')
    return redirect('/')
