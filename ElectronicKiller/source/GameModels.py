# -*- coding: utf-8 -*-
import json
# author: yml
class GameHouse(object):
    def __init__(self,id):
        self.id = id
        self.users = {}
        self.clients = {}
        self.readyClients = {}
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

    """
    向浏览器发送websocket信息
    type:信息类型 command,info,message
    content:信息内容，如果不填此信息，将以kw可变参数字典为准
    except_userid:如果不为空，则向除userid之外的人发送此信息
    一般传入本玩家的userid
    """
    def Send(self,type,content=None,except_userid=None,**kw):
        if content == None:
            content = kw
        data = json.dumps({'type':type,'content':content})
        data = GameHouse.escape(data)
        for key in self.clients:
            #是否要发给除自己之外的人
            if except_userid == key:
                continue
            self.clients[key].send(data)

    def SendToReadyClient(self,type,content=None,except_userid=None,**kw):
        if content == None:
            content = kw
        data = json.dumps({'type':type,'content':content})
        data = GameHouse.escape(data)
        for key in self.readyClients:
            #是否要发给除自己之外的人
            if except_userid == key:
                continue
            self.readyClients[key].send(data)



    @staticmethod
    def escape(message):
        return message.encode('unicode_escape')

    @staticmethod
    def unescape(message):
        return message.replace('%u','\u').decode('unicode_escape')