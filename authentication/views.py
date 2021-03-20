from authentication.serializers import UserSerializer, LoginSerializer
from rest_framework import status
from backend.helper.response import Response
from django.contrib import auth
from authentication.models import Users
from rest_framework.generics import GenericAPIView

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response.ok(
                data = serializer.data,
                status = status.HTTP_200_OK,
                message= "Registrasi berhasil"
            )
        return Response.badRequest(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message= "Registrasi gagal"
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if not user:
            return Response.badRequest(
                status=status.HTTP_400_BAD_REQUEST,
                message= "Login gagal, masukkan username dan password yang benar"
            )
        
        user_data = Users.objects.filter(username=username).first()
        serializer = UserSerializer(user_data, many=False)
        
        data = {
            'tokens' : user_data.tokens()
        }
        data.update(serializer.data)
        
        return Response.ok(
            data=data,
            status=status.HTTP_200_OK,
            message= "Login berhasil"
        )