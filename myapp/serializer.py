from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
       model = User
       fields = ('email','username', 'password','user_type','phone_number')
       extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create_user to hash the password
        user = User.objects.create_user(**validated_data)
        return user   
    
class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data

#  need to add validation for book 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [ "id" ,'title','author','isbn','quantity','status','genre']
        read_only_fields = ['id']
       

#  need to add validation for book request id



class BookRequestSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
      

    class Meta:
        model = BookRequest
        fields = ["book_id"]




#  need to add validation for the id that id can't be the string ,it needs to be intger where ever we are using id


class BookActionSerializer(serializers.Serializer):
    book_request_id = serializers.IntegerField()
      
        
#  need to add validation for bookrequestaction 

class BookRequestActionSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    book_title = serializers.ReadOnlyField(source='book.title')
    book_id = serializers.ReadOnlyField(source='book.id')

    class Meta:
        model = BookRequest
        fields = ['id', 'user_username', 'book_title', 'book_id', 'status','return_status','approval_date','return_date']
    