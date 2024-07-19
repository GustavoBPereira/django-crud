from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password", trim_whitespace=False, write_only=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user_model = get_user_model()
            try:
                username = user_model.objects.get(email=email)
            except user_model.DoesNotExist:
                self.access_denied()

            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                self.access_denied()
        else:
            raise serializers.ValidationError(
                'email" and "password" are required', code="authorization"
            )
        attrs["user"] = user
        return attrs

    @staticmethod
    def access_denied():
        raise serializers.ValidationError("Access denied", code="authorization")
