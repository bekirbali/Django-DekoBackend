from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
                # 'your-sending-email@example.com',  # This will be configured in settings.py 
                'bfbalidev@gmail.com',  # This will be configured in settings.py -sender address*
                ['bfbalidev@gmail.com'],  # Recipient email address
                fail_silently=False,
            )
            
            return JsonResponse({'message': 'Email sent successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception e
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405) 