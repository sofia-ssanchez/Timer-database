from .models import User, Exercise, Workout
from rest_framework import serializers

# UserSerializer helps convert data between python objects and JSON
# this allows the server to send and receive data in a format that can easily be used in my app

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: # inner class that tells serializer how to behave
        model = User # tells it what model to work with
        fields = [ 'username', 'email', 'password'] # which fields from the model (db) will be serialized
        extra_kwargs = {'password' : {'write_only': True}} # adds addition settings for extra fields, means password field can only be used for writing data so it doenst get include din serialized output

        # defines how a new user should be created when valid data is submitted to API
        def create(self, validated_data): # validated_data is a dictionary of data that the serializer receives, serializer automatically validates it.
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password']
            )
            return user
        

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields =['name', 'number-of_cycles', 'workout_id']

        def create(self, validated_data):
            return Workout.objects.create(**validated_data)
        
        

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['workout', 'type', 'exercise_duration'] 

    def create(self, validated_data):
        # Extract the workout UUID from the validated data
        workout_uuid = validated_data.pop('workout')

        try:
            # Try to retrieve the workout by its UUID
            workout = Workout.objects.get(workout_id=workout_uuid) 
        except Workout.DoesNotExist:
            raise serializers.ValidationError("Workout not found")

        # Now create the Exercise object with the workout and remaining validated data
        exercise = Exercise.objects.create(workout=workout, **validated_data)

        return exercise
