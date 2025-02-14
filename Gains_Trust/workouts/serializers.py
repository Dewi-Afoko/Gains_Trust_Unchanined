from rest_framework import serializers
from .models import Workout, SetDict


class WorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = "__all__"
        read_only_fields = ["user", "id"]

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError(
                {"user": "An authenticated user is required to create a workout."}
            )

        return Workout.objects.create(user=request.user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)

        instance.save()
        return instance


class SetDictSerializer(serializers.ModelSerializer):

    class Meta:
        model = SetDict
        fields = "__all__"
        read_only_fields = ["workout", "set_number", "id", "set_order"]

    def create(self, validated_data):
        workout = self.context.get("workout")
        if not workout:
            raise serializers.ValidationError(
                {"workout": "A valid workout instance must be provided."}
            )

        set_dict = SetDict.objects.create(workout=workout, **validated_data)
        set_dict.refresh_from_db()
        return set_dict

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)

        instance.save()
        return instance
