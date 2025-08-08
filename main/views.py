from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            from_email = data.get('email')
            topic = data.get('topic')
            message = data.get('message')

            if not all([name, phone, from_email, topic]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            subject = f'Contact Form Submission: {topic}'
            email_message = f"""
            You have a new message from your website contact form:

            Name: {name}
            Phone: {phone}
            Email: {from_email}
            Topic: {topic}

            Message:
            {message}
            """
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,  # sender address (from settings)
                ['infodekoelektrik@gmail.com'],  # recipient email address
                fail_silently=False,
            )
            
            return JsonResponse({'message': 'Email sent successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the detailed exception for debugging
            logger.error(f"Email sending failed: {str(e)}")
            print(f"EMAIL ERROR: {str(e)}")  # Console output for debugging
            return JsonResponse({'error': f'Email sending failed: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405) 