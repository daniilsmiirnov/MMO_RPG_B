from django.core.mail import mail_managers, EmailMultiAlternatives
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from mmo_rpg import settings
from webapp.models import Response, Message


@receiver(post_save, sender=Response)
def notify_message_author(sender, instance, created, **kwargs):
    if created:
        template = 'mail/new_response.html'
        email_subject = f'Новый отклик на объявление'
        message_author_email = [instance.message.messageAuthor.email]
        html = render_to_string(
            template_name=template,
            context={
                'response_author': instance.responseAuthor,
                'message': instance.message,
            }
        )

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=message_author_email
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


@receiver(pre_save, sender=Response)
def notify_message_author(sender, instance, **kwargs):
    previous = Response.objects.get(id=instance.id)
    if not previous.isAccepted:
        template = 'mail/response_accepted.html'
        email_subject = 'Ваш отклик принят'
        message_author_email = [instance.responseAuthor.email]
        html = render_to_string(
            template_name=template,
            context={
                'message_author': instance.message.messageAuthor,
                'text': instance.text,
                'message': instance.message,
            }
        )

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=message_author_email
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


def get_subscribers(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


@receiver(post_save, sender=Message)
def new_message_subscription(sender, instance, created, **kwargs):
    if created:
        template = 'mail/new_message.html'
        email_subject = f'Новое объявление в категории {instance.category}'
        message_author_email = get_subscribers(instance.category)
        html = render_to_string(
            template_name=template,
            context={
                'category': instance.category,
                'author': instance.messageAuthor,
                'title': instance.title,
                'id': instance.id,
            }
        )

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=message_author_email
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
