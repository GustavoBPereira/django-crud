from rest_framework import permissions, views, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.contrib.auth import login
from app.user.rest.serializers import LoginSerializer, CreateUserSerializer


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(
            data=self.request.data, context={"request": self.request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data["user"]
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class CreateUserView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(
            data=self.request.data, context={"request": self.request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data["user"]
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
