from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.conf import settings
from django.shortcuts import redirect,render
from django.http import JsonResponse,HttpResponse

ms_identity_web = settings.MS_IDENTITY_WEB

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('/login')


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response





class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        # Check if the user is logged in with Microsoft Azure or if there's no token
        if not token or not ms_identity_web.is_authenticated(request):
            return redirect('login')  # Redirect to your login URL

        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
        except jwt.ExpiredSignatureError:
            return redirect('login')  # Redirect to your login URL

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


def loginPageView(request):
    return  render(request,'users/login.html')


def signUpPageView(request):
    return  render(request,'users/signup.html')

def homePageView(request):
    token = request.COOKIES.get('jwt')
    if not token:
        if request.identity_context_data.authenticated:
            return HttpResponse('login success')
        else:
            return HttpResponse('login failed')
    else:
        return HttpResponse('login success')
