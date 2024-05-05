from django.core.mail import send_mail
from events.celery import app

@app.task
def send_act_code_celery(email, code):
    link = f'http://localhost:8000/api/v1/account/confirm/{code}/'
    send_mail(
        'Your activation code',
        f'Hello, please tap this link to activate your account: \n {link}',
        'dcabatar@gmail.com',
        [email]    
    )
    
    
@app.task    
def send_confirmation_code(email, code):
    send_mail(
        'Password recovery',
        f'Hello, please copy this code to recovery your password: \n{code}',
        'dcabatar@gmail.com',
        [email],
    )