from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from events.models import Event
from gifts.models import Gift
from contributions.models import Contribution
from django.shortcuts import render
from django.urls import reverse
from gifts.utils import generate_qr_code_base64


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        events = Event.objects.filter(user=user)
        events_with_share = []
        for event in events:
            url = self.request.build_absolute_uri(reverse('events:event_detail', args=[event.pk]))
            qr_code = generate_qr_code_base64(url)
            events_with_share.append({
                'event': event,
                'event_url': url,
                'event_qr_code': qr_code,
            })
        context['events'] = events_with_share
        # Removendo gifts e contributions do contexto para exibir apenas eventos
        return context
