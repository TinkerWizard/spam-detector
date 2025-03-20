from django.db import models

class AllUsers(models.Model):
    """
        GLOBAL DATABASE(TABLE) CONTAINING REGISTERED USERS AND ALL THEIR CONTACTS
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    phone = models.BigIntegerField(null=False)
    email = models.EmailField(max_length=255, blank=True)
    is_registered = models.BooleanField(default=False)
    spam_likelihood = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.phone}) - Spam: {self.spam_likelihood}/10"
class PersonalContacts(models.Model):
    """
        TABLE CONTAINS ALL THE CONTACTS OF A PARTICULAR REGISTERED USER/OWNER
    """
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('core.AllUsers', on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey('core.AllUsers', on_delete=models.CASCADE, related_name="saved_as")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('owner', 'contact')  # Prevents duplicate contacts

    def __str__(self):
        return f"{self.owner.name} saved {self.contact.name}"
class SpamReport(models.Model):
    """
        THIS TABLE CONTAINS ALL THE REPORTS THAT HAVE BEEN MADE BY AN USER ON A PARTICULAR PHONE NUMBER
    """
    id = models.AutoField(primary_key=True)
    reported_by = models.ForeignKey('core.AllUsers', on_delete=models.CASCADE, related_name="reports")
    phone = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from core.utils import update_spam_likelihood
        super().save(*args, **kwargs)
        update_spam_likelihood(self.phone)  # Update spam score after saving

    def __str__(self):
        return f"{self.reported_by.name} marked {self.phone} as spam"

class SearchIndex(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.AllUsers', on_delete=models.CASCADE)  
    name = models.CharField(max_length=255, db_index=True)  # Indexed for fast search
    phone = models.CharField(max_length=15, db_index=True)  # Indexed for fast search

    def __str__(self):
        return f"{self.name} ({self.phone})"