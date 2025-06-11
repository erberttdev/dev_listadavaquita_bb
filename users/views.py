from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from events.models import Event
from gifts.models import Gift
from contributions.models import Contribution
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['events'] = Event.objects.filter(user=user)
        context['gifts'] = Gift.objects.filter(event__user=user)
        context['contributions'] = Contribution.objects.filter(gift__event__user=user)
        return context
