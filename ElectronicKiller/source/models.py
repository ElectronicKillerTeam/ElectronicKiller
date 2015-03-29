"""
Definition of models.
"""

from django.db import models
import hashlib
from source.utils import Guid
from django.contrib.auth.models import User
import datetime
import random

# Create your models here.
class UserInfo(models.Model):
    id = models.CharField(max_length=36,primary_key=True)
    CreatedTime = models.DateTimeField(auto_now_add=True)
    LastLoginTime = models.DateTimeField(null=True)
    LastLoginIP = models.IPAddressField(null=True)
    UserName = models.CharField(max_length=50)
    AuthUser = models.OneToOneField(User)
    #以下字段用于身份识别
    UserIP = models.IPAddressField(null=True)
    ComputerName = models.CharField(max_length=255,null=True)
    #以下字段用于浏览器识别
    UserAgent = models.CharField(max_length=500,null=True)
    MD5 = models.CharField(max_length=32,null=True)

    def UpdateMD5(self):
        content = '%s@%s@%s' % (self.ComputerName,self.UserIP,self.UserAgent)
        self.MD5 = hashlib.md5(content.encode('utf-8')).hexdigest()
        return self.MD5

    @staticmethod
    def GetOrCreateInstance(username):
        try:
            u = UserInfo.objects.get(UserName=username)
        except UserInfo.DoesNotExist:
            u = UserInfo(UserName=username)
            u.CreatedTime = datetime.datetime.now()
            u.id = Guid.New()
            a = User.objects.create_user(username=str(u.id)[-10:] + '@@' + username,password='onlytest')
            u.AuthUser = a
            u.save()
        return u

class GameHouse(object):
    def __init__(self,id):
        self.id = id
        self.users = {}
        self.clients = {}
        self.isStartGame = False
        pass

    def StartGame(self):
        self.isStartGame = True

    def PushUser(self,user):
        if self.isStartGame:
            return
        self.users[user.id] = user

    def PopUser(self,user):
        if self.isStartGame:
            return
        self.users.pop(user.id)

class CardInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    CreatedTime = models.DateTimeField(auto_now_add=True)
    CardName = models.CharField(max_length=50)
    CardNum = models.IntegerField()
    Color = models.IntegerField()
    Description = models.CharField(max_length=255,null=True)

    @staticmethod
    def GetNewCard():
        card = CardInfo(id=Guid.New())
        card.CardNum = random.randint(1,10)
        card.Color = random.randint(1,4)
        card.CardName = u'南蛮入侵'
        card.Description = u'待补充描述'
        return card
    
    def GetJsonCardInfo(self):
        json_params = ['CardName','CardNum','Color','Description']
        card = {'id':str(self.id)}
        for p in json_params:
            card[p] = getattr(self,p)
        return card