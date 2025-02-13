from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt


@shared_task
def send_email(recipient_email,name,url,template,subject,company_name,msg=""):
        subject = subject
        from_email = settings.EMAIL_HOST_USER  # Replace with your from email
        to = recipient_email

        html_content = render_to_string(f'api/{template}.html', {
                'name': name,
                'url': url,
                'team_name': company_name,
                'msg':msg 
        })
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_registeration_email(recipient_email,name,subject,organizer,start_date,start_time,location,event_name):
        subject = subject
        from_email = settings.EMAIL_HOST_USER  # Replace with your from email
        to = recipient_email

        html_content = render_to_string(f'api/registeration.html', {
                'name': name,
                'organizer_name': organizer,
                'date' : start_date,
                
                'time': start_time,
                
                'location' : location,
                'event_name' : event_name
                
                # 'event_description': event_description
        })
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


