import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# This file designs the database, collumns and tables

# saving workouts model: 2 models, 1 for the workouts and the other for the exercises.
# workout model : workout name, number of cycles, id of workout
# exercise model: type(high, low break), duration, media, workout id
# user model: username, password, 

# manager is a class that has methods to interact w the databse, used to query or save data
# userManager is used to create new users

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("Usermust have a username")
        
        user = self.model( #creating an instance of the User model
            email=self.normalize_email(email), # normalizes the email so all emails are stored in the same format (makes everything lowercase)
            username=username,
        )

        user.set_password(password) # sets and hashes the password
        user.save(using=self._db) # saves the new user to the db
        return user 
    
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True) # says all usernames need to be unique
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    objects = UserManager() # use my UserManager instead of the default

    USERNAME_FIELD = 'username' # users will use their username to login, could be email instead
    REQUIRED_FIELDS = ['email']

    def __str__(self): 
        return self.username # returnt he username as a human readable string
    


class Workout(models.Model):
    name = models.CharField(max_length=50)
    number_of_cycles = models.IntegerField(default=1)
    workout_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    WARMUP = 'warmup'
    HIGH = 'high'
    LOW = 'low'
    BREAK = 'break'

    INTERVAL_TYPE_CHOICES = [
        (WARMUP, 'warmup'),
        (HIGH, 'high'),
        (LOW, 'low'),
        (BREAK, 'break')
    ]
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    type = models.CharField(max_length=10, choices=INTERVAL_TYPE_CHOICES)
    exercise_duration = models.IntegerField(default=1)

    def __str__(self):
        return self.name