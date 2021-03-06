from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse

from gmailer.gmail import mailer

def auth(request):
    """Generate Google OAuth authorization url and state. State is stored inside session and view is redirected to the authorization url.

    :param request: A request object received from requested view
    :rtype: Redirection to authorization url
    """
    url, request.session['oauth_state'] = mailer.authorize()
    return redirect(url)

def verify(request):
    """Verify code and state received from request.

    :param request: A request object received from requested view
    :rtype: :class:`JsonResponse` instance
    """
    try:
        result = mailer.verify(request)
    except mailer.StateError as err:
        return JsonResponse({'error': str(err)})
    return JsonResponse(result)

def revoke(request):
    """Revoke the Google OAuth authorization.

    :param request: A request object received from requested view
    :rtype: :class:`JsonResponse` instance
    """
    try:
        mailer.revoke()
    except mailer.UnauthorizedAPIError:
        return JsonResponse({'error': 'API access is already revoked. Please authorize api access.'})
    return JsonResponse({'message': 'Successfully revoked the API service'})

def test_send_mail(request):
    """Test the Gmail API by sending an email to self.

    :param request: A request object received from requested view
    :rtype: :class:`JsonResponse` instance
    """
    try:
        mailer.test_mail()
    except mailer.UnauthorizedAPIError:
        return JsonResponse({'error': 'Unable to send test mail. Please authorize api access.'})
    return JsonResponse({'message': 'Successfully send test mail'})
