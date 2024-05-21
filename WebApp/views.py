import json
import logging
from django.http import JsonResponse
from .models import GoogleAccount
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

@api_view(['POST'])
def submit_google_account(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    logger.debug(f'Received email: {email}, password: {password}')

    if email and password:
        account = GoogleAccount(email=email, password=password)
        account.save()
        return JsonResponse({'message': 'Your account details saved successfully.'})
    else:
        return JsonResponse({'error': 'Email and password are required.'}, status=400)

@api_view(['POST'])
def login_google_account(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    logger.debug(f'Attempting login with email: {email}, password: {password}')

    if email and password:
        try:
            account = GoogleAccount.objects.get(email=email)
            if password == account.password:
                return JsonResponse({'message': 'Login successful.'})
            else:
                return JsonResponse({'error': 'Invalid password.'}, status=400)
        except GoogleAccount.DoesNotExist:
            return JsonResponse({'error': 'Account not found, Please register'}, status=404)
    else:
        return JsonResponse({'error': 'Email and password are required.'}, status=400)

@api_view(['GET'])
def get_google_account(request):
    google_accounts = GoogleAccount.objects.all()
    serialized_data = [{'email': account.email, 'password': account.password} for account in google_accounts]
    return JsonResponse(serialized_data, safe=False)
