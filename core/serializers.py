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
    phone = serializers.CharField(write_only=True)
    
    class Meta:
        model = SpamReport
        fields = ['phone']
    
    def create(self, validated_data):
        # Just use the phone number directly as intended in the model
        # No need to look up a user by phone
        return SpamReport.objects.create(**validated_data)