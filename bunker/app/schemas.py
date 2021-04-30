from typing import List,Any
from datetime import datetime
from datetime import date
from ninja import Schema
from ninja.orm import create_schema
from . import models
from django.contrib.auth.models import Group as Role,Permission


UserSchema = create_schema(models.User,name="User",depth=1,exclude=['password','is_staff','groups','user_permissions','is_superuser','is_active'])
GameSchema = create_schema(models.Game,name="Game")
GameCreateSchema = create_schema(models.Game,name="GameCreate",fields=['password'])
# UserCreateSchemaIn = create_schema(models.User, fields=['email','phone','password'])

class UserCreateSchemaIn(Schema):
    username: str
    password: str
