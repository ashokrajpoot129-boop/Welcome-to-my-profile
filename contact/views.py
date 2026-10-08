import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .forms import ContactForm
from .models import ContactMessage


@require_GET
def home(request):
    return render(request, 'index.html')


@require_GET
def profile(request):
    return render(request, 'home.html')


@require_GET
def about(request):
    return render(request, 'about.html')


@require_GET
def services(request):
    return render(request, 'services.html')


@require_GET
def contact_page(request):
    return render(request, 'contact/contact.html', {'form': ContactForm()})


def deliver_contact(form):
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    mobile_number = form.cleaned_data['mobile_number']
    message = form.cleaned_data['message']
    ContactMessage.objects.create(
        name=name,
        email=email,
        mobile_number=mobile_number,
        message=message,
    )
    subject = f'Website contact from {name}'
    body = f'Name: {name}\nEmail: {email}\nMobile: {mobile_number}\n\nMessage:\n{message}'

    recipients = list(dict.fromkeys(
        address for address in (settings.CONTACT_NOTIFY_EMAIL, 'ashokrajpoot129@gmail.com') if address
    ))
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
    send_mail(
        'We received your message',
        f"Hi {name},\n\nThanks for contacting us. We received your message and will get back to you soon.",
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )


@require_POST
def submit_contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        deliver_contact(form)
        return render(request, 'contact/contact.html', {
            'form': ContactForm(),
            'success': 'Your message was saved successfully.',
        })
    return render(request, 'contact/contact.html', {'form': form}, status=400)


@require_POST
def contact_api(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'ok': False, 'error': 'Request body must be valid JSON.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'ok': False, 'error': 'Request body must be a JSON object.'}, status=400)

    form = ContactForm(payload)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors.get_json_data()}, status=400)

    deliver_contact(form)
    return JsonResponse({'ok': True, 'message': 'Your message was saved successfully.'})
