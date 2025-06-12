from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
        # Removendo gifts e contributions do contexto para exibir apenas eventos
        return context
