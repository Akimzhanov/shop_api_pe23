import logging

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .tasks import send_activation_sms
from .utils import normalize_phone


User = get_user_model()
logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'password', 'password_confirm')

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Не верный формат телефона')
        return phone 

    def validate(self, attrs):
        password = attrs.get('password')  # в переменной attrs храниться эти поля и достаем её
        password_confirm = attrs.pop('password_confirm')  #в переменной attrs храниться эти поля и достаем её, но в потом удаляется 
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):  # validated_data - это пройденные проверку данные 
        user = User.objects.create_user(**validated_data)    # ** - это расспаковка данных с validated_data
        user.create_activation_code()
        try:
            send_activation_sms(user.phone, user.activation_code)
        except Exception as e:
            logger.error(str(e))
        return user

        
class ActivationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13, required=True)
    code = serializers.CharField(max_length=10, required=True)

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Не верный формат телефона ')
        if User.objects.filter(phone=phone).exists():    # проверяет сущ в базе данных веденный номер
            raise serializers.ValidationError('Пользователь с таким номером телефона не найден')
        return phone

    def validate_code(self, code):
        if User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неверный код')
        return code 

    def activate_account(self):
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        user.is_active = True   # поле активирует аккаунт пользователя 
        user.activation_code = ''
        user.save()


