from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, View
from decimal import Decimal
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from .models import Gift, CatalogProduct, GiftList, GiftListItem
from events.models import Event
from .forms import GiftForm, AddToGiftListForm
from django.contrib import messages

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

from .utils import scrape_product_data

class GiftCreateView(CreateView):
    model = Gift
    form_class = GiftForm
    template_name = 'gifts/gift_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        product_link = self.request.GET.get('product_link')
        if product_link:
            scraped_data = scrape_product_data(product_link)
            if scraped_data:
                initial.update({
                    'name': scraped_data.get('name'),
                    'photo': scraped_data.get('photo'),
                    'value': scraped_data.get('price'),
                    'store_name': scraped_data.get('store_name'),
                    'store_type': scraped_data.get('store_type'),
                    'product_link': product_link,
                })
        return initial

    def form_valid(self, form):
        form.instance.event = self.event
        if form.instance.value:
            form.instance.fundraising_value = form.instance.value * Decimal('1.15')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def get_success_url(self):
        return self.event.get_absolute_url()


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

class CatalogProductListView(ListView):
    model = CatalogProduct
    template_name = 'gifts/catalog_product_list.html'
    context_object_name = 'products'
    paginate_by = 20

class AddProductToGiftListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(CatalogProduct, id=product_id)
        gift_list, created = GiftList.objects.get_or_create(user=request.user, name='Minha Lista de Presentes')
        # Check if product already in gift list
        if GiftListItem.objects.filter(gift_list=gift_list, product=product).exists():
            messages.info(request, 'Produto já está na sua lista de presentes.')
        else:
            GiftListItem.objects.create(gift_list=gift_list, product=product)
            messages.success(request, 'Produto adicionado à sua lista de presentes.')
        return redirect('gifts:catalog_product_list')
