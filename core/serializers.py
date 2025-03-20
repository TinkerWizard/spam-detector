from rest_framework import serializers
from .models import SearchIndex, PersonalContacts, SpamReport, AllUsers

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUsers
        fields = ['name', 'phone', 'spam_likelihood']

class SearchDetailSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = AllUsers
        fields = ['id', 'name', 'phone', 'spam_likelihood', 'email']

    def get_email(self, obj):
        show_email = self.context.get('show_email', False)  
        print(f"DEBUG: Serializer - show_email -> {show_email} for {obj.name}")
        return obj.email if show_email else None


class PersonalContactSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    contact_phone = serializers.CharField(source='contact.phone', read_only=True)

    class Meta:
        model = PersonalContacts
        fields = ['id', 'contact_name', 'contact_phone', 'created_at']

class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['id', 'reported_by', 'phone', 'timestamp']
        read_only_fields = ['id', 'reported_by', 'timestamp']