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

from django.urls import reverse
from gifts.utils import generate_qr_code_base64

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        url = self.request.build_absolute_uri(reverse('events:event_detail', args=[event.pk]))
        context['event_url'] = url
        context['event_qr_code'] = generate_qr_code_base64(url)
        return context

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
