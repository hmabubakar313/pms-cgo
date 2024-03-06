# In yourapp/management/commands/send_email.py
from user.models import Lead

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Sends an email"

    def handle(self, *args, **options):
        current_time = timezone.now()
        one_day_from_now = current_time + timedelta(days=1)

        # Query leads with date_time less than 1 day away from current time
        leads = Lead.objects.filter(datetime__lte=one_day_from_now)

        # for lead in leads:
        #     # Send email to lead
        #     subject = "Reminder: Follow-up on Lead"
        #     message = f"Dear {lead.name},\n\nThis is a reminder to follow-up on your lead.\n\nBest regards,\nYour Company"
        #     recipient_list = [lead.email]
        #     sender = "testdango2@gmail.com"

        #     send_mail(subject, message, sender, recipient_list)
        self.stdout.write(self.style.SUCCESS("Reminder emails sent successfully."))
        subject = "Reminder: testing"
        message = f"Dear Tester,\n\nThis is a reminder to follow-up on your lead.\n\nBest regards,\nYour Company"
        recipient_list = ["testdango62@gmail.com"]
        sender = "testdango62@gmail.com"

        send_mail(subject, message, sender, recipient_list)
