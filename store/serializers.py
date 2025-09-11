from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from .models import Accessory, SearchHistory

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('الحساب معطل.')
            else:
                raise serializers.ValidationError('بيانات الدخول غير صحيحة.')
        else:
            raise serializers.ValidationError('يجب إدخال اسم المستخدم وكلمة المرور.')

        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data.get('email', ''))
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccessorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Accessory
        fields = (
        'id', 'name', 'slug', 'description', 'category', 'price', 'stock', 'image', 'created_at', 'updated_at')

    def create(self, validated_data):
        # auto-generate slug if not provided
        from django.utils.text import slugify
        if not validated_data.get('slug'):
            base = validated_data.get('name', 'item')
            validated_data['slug'] = slugify(base)
        return super().create(validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ('id', 'query', 'created_at')
