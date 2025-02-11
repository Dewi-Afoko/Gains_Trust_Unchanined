from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Workout, SetDict
from .serializers import SetDictSerializer, WorkoutSerializer

# Create your views here.

class WorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all workouts for the authenticated user."""
        workouts = Workout.objects.filter(user=request.user).order_by("-date")
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create a new workout for the authenticated user."""
        serializer = WorkoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            workout = serializer.save()
            return Response({'message': f'{workout.workout_name} created for {request.user.username}'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, workout_id):
        """Update a specific workout"""
        workout = get_object_or_404(Workout, id=workout_id, user=request.user)
        serializer = WorkoutSerializer(instance=workout, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            updated_workout = serializer.save()
            return Response({
                'message': f'{updated_workout.workout_name} updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, workout_id):
        """Delete a specific workout"""
        workout = get_object_or_404(Workout, id=workout_id, user=request.user)
        workout.delete()
        return Response({'message': f'Workout {workout.workout_name} deleted'}, status=status.HTTP_200_OK)

    

class SetDictView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, workout_id):
        """Retrieve all SetDicts for a specific workout"""
        workout = get_object_or_404(Workout, id=workout_id, user=request.user)
        set_dicts = SetDict.objects.filter(workout=workout).order_by('-set_order')
        serializer = SetDictSerializer(set_dicts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, workout_id):
        workout = get_object_or_404(Workout, id=workout_id, user=request.user)  # ✅ Ensures workout exists
        serializer = SetDictSerializer(data=request.data, context={'request': request, 'workout': workout}) 

        if serializer.is_valid():
            set_dict = serializer.save()
            return Response({
                'message': f'{set_dict.exercise_name} #{set_dict.set_number} created for {workout.workout_name}'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, workout_id, set_dict_id):
        """Update a SetDict"""
        set_dict = get_object_or_404(SetDict, id=set_dict_id, workout__id=workout_id, workout__user=request.user)
        serializer = SetDictSerializer(instance=set_dict, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            updated_set_dict = serializer.save()
            return Response({
                'message': f'{updated_set_dict.exercise_name} #{updated_set_dict.set_number} updated for {updated_set_dict.workout.workout_name}'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, workout_id, set_dict_id):
        """Delete a SetDict"""
        set_dict = get_object_or_404(SetDict, id=set_dict_id, workout__id=workout_id, workout__user=request.user)
        set_dict.delete()
        return Response({'message': f'SetDict #{set_dict_id} deleted from {set_dict.workout.workout_name}'}, status=status.HTTP_200_OK)
