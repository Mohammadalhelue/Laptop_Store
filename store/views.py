from django.db.models import Q

from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.shortcuts import get_object_or_404
from .models import Accessory, SearchHistory, Order, OrderItem
from .carts import Cart

from .serializers import (
    AccessorySerializer,
    RegisterSerializer,
    LoginSerializer,
    CartAddAccessorySerializer,
    CartItemSerializer,
    OrderSerializer,
)


# Disable CSRF enforcement for session-authenticated API requests (so browsable API forms work)
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # no-op


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'تم تسجيل الخروج بنجاح.'}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all().order_by('-created_at')
    serializer_class = AccessorySerializer

    # Browsers (session) + apps (token), with CSRF exempt so forms work
    authentication_classes = [CsrfExemptSessionAuthentication, SessionAuthentication, TokenAuthentication]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price', 'created_at', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'edit', 'do_delete', 'method_override']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        q = request.query_params.get('search') or request.query_params.get('q')
        if q and request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=q)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        accessory = self.get_object()
        if accessory.stock > 0:
            accessory.stock -= 1
            if accessory.stock == 0:
                accessory.save()
                accessory.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            accessory.save()
            return Response({"message": "تمت عملية الشراء بنجاح", "remaining": accessory.stock})
        return Response({"error": "المنتج غير متوفر"}, status=status.HTTP_400_BAD_REQUEST)

    # Standard RESTful handlers for API clients
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if getattr(instance, 'stock', None) == 0:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def method_override(self, request, *args, **kwargs):
        override = (request.data.get('_method') or request.query_params.get('_method') or '').upper()
        if override == 'PUT':
            kwargs['partial'] = False
            return self.update(request, *args, **kwargs)
        if override == 'PATCH' or override == '':
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        if override == 'DELETE':
            return self.destroy(request, *args, **kwargs)
        return Response({'detail': 'Unsupported _method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['post'], url_path='edit')
    def edit(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if getattr(instance, 'stock', None) == 0:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], url_path='do-delete')
    def do_delete(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommendationsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last = SearchHistory.objects.filter(user=request.user).order_by('-created_at').all()
        if not last:
            return Response({'detail': 'No search history'}, status=status.HTTP_200_OK)
        terms = [t.query for t in last]
        if not terms:
            return Response({'detail': 'No useful terms in last query'}, status=status.HTTP_200_OK)
        q = Accessory.objects.filter(category__icontains=terms[0])

        for t in terms:
            q |= (Accessory.objects.filter(name__icontains=t) |
                  Accessory.objects.filter(description__icontains=t) |
                  Accessory.objects.filter(category__icontains=t))

        serializer = AccessorySerializer(q, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        serializer = CartItemSerializer(list(cart), many=True)
        return Response({"cart": serializer.data, "total": cart.get_total_price()})


class CartAddUpdateAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, accessory_id):
        cart = Cart(request)
        accessory = get_object_or_404(Accessory, id=accessory_id)
        serializer = CartAddAccessorySerializer(data=request.data)
        if serializer.is_valid():
            cart.add(accessory=accessory, **serializer.validated_data)
            return Response({"message": "Cart updated"})
        return Response(serializer.errors, status=400)


class OrderCreateAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart(request)
        if not cart.cart:
            return Response({"error": "Cart is empty"}, status=400)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    accessory=item['accessory'],  # Matches renamed key
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
