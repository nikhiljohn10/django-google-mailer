from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse

from gmailer.gmail import mailer

def auth(request):
    url, request.session['oauth_state'] = mailer.authorize()
    return redirect(url)

def verify(request):
    result = mailer.verify(request)
    return JsonResponse(result)

def revoke(request):
    mailer.revoke()
    return JsonResponse({'message': 'Successfully revoked the API service'})

def test_send_mail(request):
    mailer.test_mail()
    return JsonResponse({'message': 'Successfully send test mail'})
