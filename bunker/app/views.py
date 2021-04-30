from bunker import settings
from app import models, schemas
from auth.jwt import AuthBearer
# from .tokens import account_activation_token

from typing import List

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth.models import Group as Role,Permission

from ninja import Router, File
from ninja.files import UploadedFile
from ninja.renderers import BaseRenderer
from ninja.errors import ValidationError
from ninja.errors import HttpError
from ninja import errors
from ninja.params import Form

import json
import codecs
import time
import random
import asyncio
from asgiref.sync import sync_to_async,async_to_sync

api = Router()

# @api.get("/say-after",auth=None)
# async def say_after(request, delay: int, word: str):
#     await asyncio.sleep(delay)
#     return {"saying": word}

# @api.get("/say-sync",auth=None)
# def say_after_sync(request, delay: int, word: str):
#     time.sleep(delay)
#     return {"saying": word}

'''USER'''

@api.get("/users/{user_id}",response=schemas.UserSchema, tags=["users"])
async def get_user(request, user_id: int):
    return await sync_to_async(models.User.objects.get)(id=user_id)

@api.get("/users",response=List[schemas.UserSchema], tags=["users"])
async def get_users(request):
    return await sync_to_async(list)(models.User.objects.all())

@api.post("/user", response=schemas.UserSchema, tags=["users"],auth=None)
def create_user(request , data: schemas.UserCreateSchemaIn):
    user = models.User(username=data.username) # User is django auth.User
    user.set_password(data.password)
    try:
        user.save()
    except:
        raise HttpError(422, "Введены неправильные данные(username,password) или существует такой аккаунт!!!")
    return user

'''GAME'''

@api.get("/game/{id}",response=schemas.GameSchema, tags=["game"])
async def get_game(request, id: int):
    return await sync_to_async(models.Game.objects.get)(id=id)

@api.get("/games",response=List[schemas.GameSchema], tags=["game"])
async def get_games(request):
    return await sync_to_async(list)(models.Game.objects.all())

@api.post("/game", response=schemas.GameSchema, tags=["game"])
def create_game(request , data: schemas.GameCreateSchema):
    game = models.Game(creator_id=request.auth,password=data.password)
    try:
        game.save()
    except:
        raise HttpError(422, "ERROR")
    return game

'''JSON'''
@sync_to_async
def get_json_param(param,id):
    f = codecs.open('app\\txts\\character.json', "rU", "utf-8")
    json_file = json.loads(f.read())
    try:
        if(id or id==0):
            result = json_file[param][0][str(id)]
        else:
            result = json_file[param][0]
    except:
        result = None
    return result

@api.get("/char/{param}", tags=["json"],auth=None)
async def get_char_json(request, param: str, id: int = None):
    ''' 
    Params be like: addinfos, baggages, biodates, chcaracters, healthes, hobbies, jobs, phobias, spells
    '''
    return await get_json_param(param,id)

@sync_to_async
def get_c_json_param(param,id):
    f = codecs.open('app\\txts\\catastrophes.json', "rU", "utf-8")
    json_file = json.loads(f.read())
    try:
        if(id or id==0):
            result = json_file["catastrophes_"+param][0][str(id)]
        else:
            result = json_file["catastrophes_"+param][0]
    except:
        result = None
    return result

@api.get("/catast/{param}", tags=["json"],auth=None)
async def get_catast_char_json(request, param: str,id: int = None):
    ''' 
    Params be like: area, days, desc, items, population, type
    '''
    return await get_c_json_param(param,id)
