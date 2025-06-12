from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).order_by('date')

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'date', 'visibility']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'date', 'visibility']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
