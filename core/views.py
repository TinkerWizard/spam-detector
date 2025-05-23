from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from core.utils import update_spam_likelihood
from .models import PersonalContacts, SpamReport, AllUsers
from .serializers import SearchSerializer, SearchDetailSerializer, PersonalContactSerializer, SpamReportSerializer
from django.apps import apps
from django.db.models import Case, When, IntegerField

class SearchView(generics.ListAPIView):
    serializer_class = SearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query", "").strip()
        if not query:
            return AllUsers.objects.none()  

        if query.isdigit():  
            registered_user = AllUsers.objects.filter(phone=query, is_registered=True).first()
            return [registered_user] if registered_user else AllUsers.objects.filter(phone=query)


        return (
            AllUsers.objects.filter(name__icontains=query)
            .annotate(
                priority=Case(
                    When(name__istartswith=query, then=0),  
                    default=1,  
                    output_field=IntegerField(),
                )
            )
            .order_by("priority", "name")  
        )

class SearchDetailedView(generics.RetrieveAPIView):
    serializer_class = SearchDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise ValidationError("Primary key (pk) is required.")

        person = get_object_or_404(AllUsers, pk=pk)
        logged_in_user = self.request.user

        logged_in_alluser = AllUsers.objects.get(email=logged_in_user.email)  

        is_contact = PersonalContacts.objects.filter(
            owner=logged_in_alluser,  # Use the AllUsers instance, not the auth user
            contact=person
        ).exists()
        # is_contact = PersonalContacts.objects.filter(owner=logged_in_user, contact=person).exists()
        show_email = person.is_registered and is_contact
        self.request.show_email = show_email  

        return person

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['show_email'] = getattr(self.request, 'show_email', False)  
        return context



    
class PersonalContactView(generics.ListAPIView):
    """
    This view allows users to retrieve their saved contacts.
    Only contacts belonging to the logged-in user are shown.
    """
    serializer_class = PersonalContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_phone = self.request.user.phone  

        try:
            all_users_instance = AllUsers.objects.get(phone=user_phone)
        except AllUsers.DoesNotExist:
            return PersonalContacts.objects.none()  

        return PersonalContacts.objects.filter(owner=all_users_instance)

class SpamReportView(generics.CreateAPIView):
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        phone_number = self.request.data.get("phone")
        if not phone_number:
            raise ValidationError({"error": "Phone number is required."})
        
        try:
            reporting_user = AllUsers.objects.get(phone=self.request.user.phone)
        except AllUsers.DoesNotExist:
            raise ValidationError({"error": "Your user record was not found in the AllUsers table."})
        
        # Save both the reporting user and the phone number
        serializer.save(reported_by=reporting_user, phone=phone_number)