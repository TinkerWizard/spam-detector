from django.db.models import Count
from core.models import AllUsers, SpamReport

def update_spam_likelihood(phone):
    total_reports = SpamReport.objects.count()
    phone_reports = SpamReport.objects.filter(phone=phone).count()

    if total_reports == 0:
        spam_likelihood = 0.0
    else:
        spam_likelihood = (phone_reports / total_reports) * 10

    AllUsers.objects.filter(phone=phone).update(spam_likelihood=round(spam_likelihood, 1))
