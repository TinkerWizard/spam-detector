from .models import SpamReport, AllUsers

def update_spam_likelihood(user_phone):
    # If user_phone is already a phone number string, use it directly
    # If it's a user object, get the phone number
    if isinstance(user_phone, str):
        phone = user_phone
    else:
        phone = user_phone.phone
    
    # Count reports against this phone number
    total_reports = SpamReport.objects.filter(phone=phone).count()
    
    # Calculate spam likelihood (max 10)
    spam_likelihood = min((total_reports / 10) * 10, 10)  # Scale to 10
    
    # Find the user(s) with this phone number and update them
    users = AllUsers.objects.filter(phone=phone)
    for user in users:
        user.spam_likelihood = round(spam_likelihood, 1)
        user.save()