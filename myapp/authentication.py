# custom tokeniztion  


# class CustomTokenAuthentication(TokenAuthentication):
#     model=Token
  
#     def check_token(self,request):
#         response = {}
#         auth_token=request.META.get("HTTP_AUTHORIZATION")
#         print(auth_token)
#         if auth_token == ""  or auth_token == None:  #token can't be empty or none 
#             response['message'] = "Token is required to authenticate"
#             response['status'] = status.HTTP_401_UNAUTHORIZED
#             raise exceptions.AuthenticationFailed(response)
#         elif not auth_token.startswith("Token"):
#             response["message"] = "Token should start with Token"
#             raise exceptions.AuthenticationFailed(response)
#         else:
#             return auth_token
            
        
#     def authenticate(self,request):
#         response={}
#         auth_token=self.check_token(request)
#         token =Token.objects.filter(key=auth_token[1]).first()
#         if token:
#             return self.authentication_credential(token)
#         else:
#             response['message']="authentication credential is incorrect"
#             return exceptions.AuthenticationFailed(response)
       
#     def authentication_credential(self,token):
#         return (token.user, token)  


from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from .models import *
from rest_framework.authtoken.models import Token

class CustomTokenAuthentication(TokenAuthentication):
    model = Token

    def check_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or auth_header == "":
            raise exceptions.AuthenticationFailed("Token is required to authenticate")
        if not auth_header.startswith("Token "):
            raise exceptions.AuthenticationFailed("Token should start with 'Token'")
        auth_token = auth_header.split(' ')[1]
        return auth_token

    def authenticate(self, request):
        auth_token = self.check_token(request)
        token = Token.objects.filter(key=auth_token).first()
        if token:
            return self.authentication_credential(token)
        raise exceptions.AuthenticationFailed("Authentication credentials were not provided or are invalid.")

    def authentication_credential(self, token):
        return (token.user, token)
