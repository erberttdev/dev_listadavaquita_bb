import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.conf import settings
from contributions.models import Contribution
import mercadopago

sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

class CreatePaymentView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        contribution_id = data.get('contribution_id')
        try:
            contribution = Contribution.objects.get(id=contribution_id)
        except Contribution.DoesNotExist:
            return JsonResponse({'error': 'Contribuição não encontrada'}, status=404)

        preference_data = {
            "items": [
                {
                    "title": contribution.gift.name,
                    "quantity": 1,
                    "unit_price": float(contribution.amount),
                }
            ],
            "payer": {
                "name": contribution.name,
                "email": contribution.email,
            },
            "back_urls": {
                "success": request.build_absolute_uri('/payment/success/'),
                "failure": request.build_absolute_uri('/payment/cancel/'),
                "pending": request.build_absolute_uri('/payment/pending/'),
            },
            "auto_return": "approved",
            "payment_methods": {
                "excluded_payment_types": [
                    {"id": "ticket"}
                ],
                "installments": 1,
            },
            "notification_url": request.build_absolute_uri('/mercadopago/webhook/'),
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return JsonResponse({"init_point": preference["init_point"]})

@csrf_exempt
def mercadopago_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        topic = payload.get('type')
        if topic == 'payment':
            payment_id = payload.get('data', {}).get('id')
            if payment_id:
                payment_response = sdk.payment().get(payment_id)
                payment = payment_response["response"]
                status = payment.get('status')
                external_reference = payment.get('external_reference')
                # Atualizar status da contribuição com base no external_reference (id da contribuição)
                try:
                    contribution = Contribution.objects.get(id=external_reference)
                    contribution.payment_status = status
                    contribution.save()
                except Contribution.DoesNotExist:
                    pass
        return HttpResponse(status=200)
    return HttpResponse(status=405)
