from django.core.mail import send_mail
from rest_framework.response import Response

from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_email_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-verification')


def verify_token(token , expiration = 3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    
    try :
        email = serializer.loads(token , salt="email-verification" , max_age=expiration)
        return email 
    except Exception as e : 
        return None

def email_verification(email):
    try : 
        token = generate_email_verification_token(email)
        #this link should point to your frontend for redirection, then in the frontend, make a api post request to this route below
        #http://localhost:3000/verify-email/
        #http://127.0.0.1:8000/api/verify-email/{token}/
        #verification_link = f"http://localhost:3000/verify-email/{token}"
        verification_link = f"http://gtdtt.digital/verify-email/{token}"

    # Send email
        send_mail(
        subject="Verify Your Email",
        message=f"Click the link to verify your email: {verification_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
        )
    except Exception as e : 
        return e
    


