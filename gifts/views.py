from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Gift
from events.models import Event

class GiftCreateView(LoginRequiredMixin, CreateView):
    model = Gift
    fields = ['event', 'name', 'value', 'store_name', 'store_type', 'store_address_or_link', 'photo', 'product_link', 'priority', 'allow_simultaneous_contributions']
    template_name = 'gifts/gift_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Limitar eventos ao usuário logado
        form.fields['event'].queryset = Event.objects.filter(user=self.request.user)
        return form

class GiftDetailView(LoginRequiredMixin, DetailView):
    model = Gift
    template_name = 'gifts/gift_detail.html'
    context_object_name = 'gift'

class GiftUpdateView(LoginRequiredMixin, UpdateView):
    model = Gift
    fields = ['name', 'value', 'store_name', 'store_type', 'store_address_or_link', 'photo', 'product_link', 'priority', 'allow_simultaneous_contributions']
    template_name = 'gifts/gift_form.html'

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.event.pk})

class GiftDeleteView(LoginRequiredMixin, DeleteView):
    model = Gift
    template_name = 'gifts/gift_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.event.pk})
