from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Weight

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "password", "height", "dob"]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user

    def update(self, instance, validated_data):
        height = validated_data.get('height')
        dob = validated_data.get('dob')
        password = validated_data.get('password')
        if height:
            instance.height = height
        if dob:
            instance.dob = dob
        if password:
            instance.set_password(password)
        instance.save()
        return instance
        


class WeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weight
        fields = ["user", "weight", "date_recorded"]
        read_only_fields = ["user", "date_recorded"]

    def create(self, validated_data):
        request = self.context.get("request")
        weight = Weight.objects.create(
            user=request.user,
            weight=validated_data["weight"]
        )
        return weight