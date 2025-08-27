from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import json
import logging
import re

logger = logging.getLogger(__name__)

def is_suspicious_content(content):
    """
    Şüpheli içerik kontrolü - spam ve bot saldırılarını tespit eder
    """
    suspicious_patterns = [
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URL'ler
        r'(?:viagra|casino|porn|sex|adult|drug|pill|pharmacy|loan|credit|insurance|mortgage)',  # Spam kelimeleri
        r'(?:click here|free money|guarantee|limited time|act now|urgent|winner)',  # Spam ifadeleri
        r'[A-Z]{10,}',  # Çok fazla büyük harf
        r'(.)\1{5,}',  # Aynı karakterin tekrarı
    ]
    
    content_lower = content.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, content_lower, re.IGNORECASE):
            return True
    return False

def check_email_limit(ip_address, email):
    """
    IP ve email bazlı limit kontrolü
    """
    # IP bazlı kontrol (1 saatte en fazla 5 mesaj)
    ip_key = f"contact_form_ip_{ip_address}"
    ip_count = cache.get(ip_key, 0)
    if ip_count >= 5:
        return False, "Bu IP adresinden çok fazla mesaj gönderildi. Lütfen 1 saat sonra tekrar deneyin."
    
    # Email bazlı kontrol (1 günde en fazla 10 mesaj)
    email_key = f"contact_form_email_{email}"
    email_count = cache.get(email_key, 0)
    if email_count >= 10:
        return False, "Bu email adresinden çok fazla mesaj gönderildi. Lütfen 24 saat sonra tekrar deneyin."
    
    return True, None

def update_email_limits(ip_address, email):
    """
    Email limit sayaçlarını güncelle
    """
    # IP bazlı sayaç (1 saat)
    ip_key = f"contact_form_ip_{ip_address}"
    ip_count = cache.get(ip_key, 0)
    cache.set(ip_key, ip_count + 1, 3600)  # 1 saat
    
    # Email bazlı sayaç (24 saat)
    email_key = f"contact_form_email_{email}"
    email_count = cache.get(email_key, 0)
    cache.set(email_key, email_count + 1, 86400)  # 24 saat

@csrf_exempt
@ratelimit(key='ip', rate='3/m', method='POST', block=True)  # Dakikada en fazla 3 istek
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
                return JsonResponse({'error': 'Gerekli alanlar eksik'}, status=400)

            # IP adresini al
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            # Rate limiting kontrolü
            can_send, limit_error = check_email_limit(ip_address, from_email)
            if not can_send:
                return JsonResponse({'error': limit_error}, status=429)

            # Spam kontrolü
            full_content = f"{name} {from_email} {phone} {topic} {message}"
            if is_suspicious_content(full_content):
                return JsonResponse({'error': 'Mesajınız güvenlik kontrolünden geçemedi. Lütfen içeriğinizi kontrol edin.'}, status=400)

            # Email format kontrolü
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, from_email):
                return JsonResponse({'error': 'Geçerli bir email adresi girin'}, status=400)

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
            
            # Başarılı gönderimden sonra limit sayaçlarını güncelle
            update_email_limits(ip_address, from_email)
            
            return JsonResponse({'message': 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Geçersiz JSON verisi'}, status=400)
        except Exception as e:
            # Log the detailed exception for debugging
            logger.error(f"Email sending failed: {str(e)}")
            print(f"EMAIL ERROR: {str(e)}")  # Console output for debugging
            # Rate limit aşımı durumu
            if "Rate limit exceeded" in str(e):
                return JsonResponse({'error': 'Çok fazla istek gönderdiniz. Lütfen birkaç dakika bekleyin.'}, status=429)
            return JsonResponse({'error': 'Email gönderilirken bir hata oluştu. Lütfen tekrar deneyin.'}, status=500)

    return JsonResponse({'error': 'Geçersiz istek metodu'}, status=405) 