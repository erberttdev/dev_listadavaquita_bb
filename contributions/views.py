from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Contribution
from gifts.models import Gift

class ContributionCreateView(CreateView):
    model = Contribution
    fields = ['name', 'email', 'phone', 'cpf', 'amount', 'message']
    template_name = 'contributions/contribution_form.html'

    def form_valid(self, form):
        gift_id = self.kwargs.get('gift_id')
        gift = get_object_or_404(Gift, id=gift_id)
        form.instance.gift = gift
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contributions:progress', kwargs={'gift_id': self.object.gift.id})

class ContributionProgressView(DetailView):
    model = Gift
    template_name = 'contributions/contribution_progress.html'
    context_object_name = 'gift'

    def get_object(self):
        gift_id = self.kwargs.get('gift_id')
        return get_object_or_404(Gift, id=gift_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contributions = self.object.contributions.filter(payment_status='approved')
        total_contributed = sum(c.amount for c in contributions)
        context['total_contributed'] = total_contributed
        context['goal'] = self.object.value
        context['progress_percent'] = int((total_contributed / self.object.value) * 100) if self.object.value > 0 else 0
        return context
