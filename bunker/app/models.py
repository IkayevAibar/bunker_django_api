from django.contrib.auth.base_user import BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser,UserManager as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
import os
from django.core.cache import cache 
from bunker import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
# from comment.models import Comment

class UserManager(BaseUserAdmin):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


# Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
# Group.add_to_class('school_id', models.ForeignKey('app.School',on_delete=models.SET_NULL,blank=True,null=True,help_text='Школа'))
# Group.add_to_class('creator_id', models.ForeignKey('app.User',on_delete=models.SET_NULL,blank=True,null=True,help_text='zxc'))

def content_file_name_user(instance, filename):
    return os.path.join(str(instance.school_id.id),'avatar',str(instance.id),filename)



class User(AbstractUser):
    email = None
    first_name=None
    last_name=None
    is_online = models.BooleanField(default=False)
    avatar = models.FileField('Аватар',upload_to=content_file_name_user,blank=True, null=True)
    REQUIRED_FIELDS = []
    objects = UserManager()

    # USERNAME_FIELD = 'identifier'
    def has_group(user, group_name):
        return user.groups.filter(name=group_name).exists()
    def __str__(self):
        return "%d | %s" % (self.id, self.username)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Game(models.Model):
    creator_id = models.ForeignKey('User', related_name='creator', on_delete=models.CASCADE,blank=True, null=True)
    password = models.CharField('Пароль', max_length=50,blank=True, null=True)

class GameRules(models.Model):
    type = models.CharField('Тип Катастрофы', max_length=5,blank=True, null=True)
    area = models.CharField('Площадь', max_length=5,blank=True, null=True)
    days = models.CharField('Количество дней', max_length=5,blank=True, null=True)
    items = models.CharField('Предметы находящие в бункере', max_length=5,blank=True, null=True)
    population = models.CharField('Количество(%) население оставщихся людей в мире', max_length=5,blank=True, null=True)
    desc = models.CharField('Описание', max_length=5,blank=True, null=True)
    game = models.ForeignKey('Game', related_name='gamerule', on_delete=models.CASCADE,blank=True, null=True)
    

class UserChar(models.Model):
    biodate = models.CharField('Биологические данные', max_length=5,blank=True, null=True)
    job = models.CharField('Профессия', max_length=5,blank=True, null=True)
    health = models.CharField('Здоровье', max_length=5,blank=True, null=True)
    phobia = models.CharField('Фобия', max_length=5,blank=True, null=True)
    hobby = models.CharField('Хобби', max_length=5,blank=True, null=True)
    addinfo = models.CharField('Допольнительная информация', max_length=5,blank=True, null=True)
    character = models.CharField('Характер', max_length=5,blank=True, null=True)
    baggage = models.CharField('Багаж', max_length=5,blank=True, null=True)
    spell_1 = models.CharField('Карта способности 1', max_length=5,blank=True, null=True)
    spell_2 = models.CharField('Карта способности 2', max_length=5,blank=True, null=True)
    player = models.ForeignKey('User', related_name='player', on_delete=models.CASCADE,blank=True, null=True)
    game = models.ForeignKey('Game', related_name='gameuser', on_delete=models.CASCADE,blank=True, null=True)
    