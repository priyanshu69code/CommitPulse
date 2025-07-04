#import model serializers
from rest_framework import serializers
from .models import User, GitHubTokern


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # or 'email' if using email-based login

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data = super().validate(attrs)
        data.update({
            "user_id": user.id,
            "email": user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            # Add more user info if needed
        })

        return data
