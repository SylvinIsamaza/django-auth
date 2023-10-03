from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

from django.shortcuts import redirect, render

from django.contrib.auth import authenticate
from allauth.socialaccount.models import SocialAccount
from dotenv import  load_dotenv
import  os
load_dotenv()

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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(os.getenv('TOKEN_EXPIRE_TIME')),
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
