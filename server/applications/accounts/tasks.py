# from django.core.mail import send_mail

# @app.task
# def send_act_code_celery(email, code):
#     link = f'http://localhost:8000/api/v1/account/confirm/{code}/'
#     send_mail(
#         'Ваш код для активации аккаунта',
#         f'Здрвствуйте {email}, нажмите на данную ссылку для активации вашего аккаунта: \n {link}',
#         'dcabatar@gmail.com',
#         [email]    
#     )
    
    
# @app.task    
# def send_confirmation_code(email, code):
#     send_mail(
#         'Код для восстановления пароля',
#         f'Здравствуйте {email}, скопируйте этот код для восстановления пароля: \n{code}',
#         'dcabatar@gmail.com',
#         [email],
#     )


from events.celery import app
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@app.task
def send_act_code_celery(email, code):
    link = f'http://localhost:8000/api/v1/account/confirm/{code}/'
    html_content = render_to_string('emails/activation_email.html', {'email': email, 'link': link})
    text_content = strip_tags(html_content)
    
    email_message = EmailMultiAlternatives(
        'Ваш код для активации аккаунта',
        text_content,
        'dcabatar@gmail.com',
        [email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()


@app.task    
def send_confirmation_code(email, code):
    html_content = render_to_string('emails/confirmation_email.html', {'email': email, 'code': code})
    text_content = strip_tags(html_content)
    
    email_message = EmailMultiAlternatives(
        'Код для восстановления пароля',
        text_content,
        'dcabatar@gmail.com',
        [email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
