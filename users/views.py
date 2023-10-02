from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from allauth.socialaccount.models import SocialAccount

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
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()

        try:
            # Try GitHub authentication first
            github_account = SocialAccount.objects.get(provider='azure', user=User.objects.get(username=email))

            if github_account:
                return redirect('/accounts/azure/login/')
        except User.DoesNotExist:
            response.data = {
                'message': 'Login failed',

            }


        except SocialAccount.DoesNotExist:
            # If GitHub authentication fails, try normal authentication
            user = authenticate(request, username=email, password=password)

            print(user)

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token=jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
            if user:
                response.data = {
                    'message': 'Login Success (Normal Authentication)',
                    'jwt':token
                }
                response.set_cookie(key='jwt', value=token, httponly=True)

            else:
                raise AuthenticationFailed('Login Failed (Normal Authentication)')

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
    return render(request, 'users/login.html')


def signUpPageView(request):
    return render(request, 'users/signup.html')


def homePageView(request):
    return render(request, 'users/homepage.html')
