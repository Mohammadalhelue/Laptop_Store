from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Accessory, SearchHistory, Order, OrderItem

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
            base = validated_data.get('name', 'accessory')
            validated_data['slug'] = slugify(base)
        return super().create(validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ('id', 'query', 'created_at')


class CartAddAccessorySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, default=1)
    override = serializers.BooleanField(required=False, default=False)


class CartItemSerializer(serializers.Serializer):
    accessory = AccessorySerializer()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['accessory', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city', 'items', 'total_cost']

    def get_total_cost(self, obj):
        return obj.get_total_cost()
