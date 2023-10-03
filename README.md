# django-auth

1.Clone this github repository

2.Open the directory where you cloned the repository

3.Install the required dependencies by running this command pip install -r requirements.txt

4.make dotenv in root directory if not exist

5.navigate to microsoft azure to create your application this link https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps

6.after registering your application navigate to your application and then client credentials  and create the credentials

add the following into the .env 

SECRET_KEY = '{your application secret key given when creating django project}'
AZURE_CLIENT_ID= '{azure client id from microsoft azure}'
AZURE_SECRET= '{secret from microsoft azure}'
AZURE_KEY= 'login.microsoftonline.com/{your tenant id from microsoft azure}'
AZURE_TENANT_ID='{tenant id from microsoft azure}'
TOKEN_EXPIRE_TIME={time you want your token to expire in minutes}


4.To run the application go to terminal and type python manage.py runserver




