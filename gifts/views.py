from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from decimal import Decimal
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Gift
from events.models import Event
from django.urls import reverse
from events.models import Event
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from .forms import GiftForm


from django.core.management import call_command
from django.http import HttpResponse

def show_migrations_view(request):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        call_command('show_migrations')
    output = f.getvalue()
    return HttpResponse(f"<pre>{output}</pre>")

class GiftCreateView(CreateView):
    model = Gift
    fields = ['name', 'value', 'image']  # ajuste os campos conforme o seu modelo
    template_name = 'gifts/gift_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Captura o evento ao qual o presente será associado
        self.event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Associa o presente ao evento antes de salvar
        form.instance.event = self.event
        # Calcula o valor da vaquinha como 1.15 * value
        if form.instance.value:
            form.instance.fundraising_value = form.instance.value * Decimal('1.15')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Adiciona o evento ao contexto do template
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def get_success_url(self):
        return self.event.get_absolute_url()  # ou reverse('events:event_detail', args=[self.event.pk])


class GiftDetailView(DetailView):
    model = Gift
    template_name = 'gifts/gift_detail.html'
    context_object_name = 'gift'

class GiftUpdateView(LoginRequiredMixin, UpdateView):
    model = Gift
    fields = ['name', 'value', 'store_name', 'store_type', 'store_address_or_link', 'photo', 'product_link', 'priority', 'allow_simultaneous_contributions']
    template_name = 'gifts/gift_form.html'

    def get_queryset(self):
        # Restringe a edição apenas para presentes cujo evento pertence ao usuário autenticado
        return Gift.objects.filter(event__user=self.request.user)

    def form_valid(self, form):
        # Calcula o valor da vaquinha como 1.15 * value
        if form.instance.value:
            form.instance.fundraising_value = form.instance.value * Decimal('1.15')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.object.event
        return context

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.event.pk})

class GiftDeleteView(LoginRequiredMixin, DeleteView):
    model = Gift
    template_name = 'gifts/gift_confirm_delete.html'

    def get_queryset(self):
        # Restringe a exclusão apenas para presentes cujo evento pertence ao usuário autenticado
        return Gift.objects.filter(event__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.event.pk})
