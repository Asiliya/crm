from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password", "photo", "description")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        password_validation.validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        new_email = validated_data.get("email")
        if new_email and new_email != instance.email:
            raise serializers.ValidationError({"email": "This field can't to be change."})

        if "password" in validated_data:
            validated_data.pop("password")

        validated_data.pop("email", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старий пароль введено неправильно.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Паролі не збігаються."})

        user = self.context['request'].user
        password_validation.validate_password(attrs['new_password'], user)
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user