"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from dwebsocket.decorators import accept_websocket,require_websocket
from source.models import UserInfo
from source.GameModels import GameHouse
import json
from source.forms import UserForm
from django.contrib import auth
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from source.utils import GetUserByRequest
from source.controllers.decorators import ajax

gameHouses = {}
gameHouses[1] = GameHouse(1)
def parse_users(users):
    result = []
    for key in users:
        result.append({'id':users[key].id,'username':users[key].UserName})
    return json.dumps(result)

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/login") 
    else:
        return render(request,
            'gameHome.html',
            context_instance = RequestContext(request,
            {
                'title':'聊天室',
                'sid':request.COOKIES['sessionid'],
                'year':datetime.now().year,
                'user_data':parse_users(gameHouses[1].users)
            }))

@ajax
def get_user_list(request):
    user_list = parser_users(users)
    return user_list

"""
进行聊天的socket通信函数
"""
@accept_websocket
def chat(request):
    GetUserByRequest(request)
    user = request.userinfo

    house = gameHouses[1]
    try:
        if house.readyClients.has_key(user.id):
            data = {'type':'command','content':'close'}
            house.readyClients[user.id].send(json.dumps(data))
            house.readyClients[user.id].close()

        house.readyClients[user.id] = request.websocket
        #将玩家加入房间
        house.PushUser(user)
        print len(house.users)

        house.SendToReadyClient('info',info='login',userid=user.id,username=user.UserName)

        for message in request.websocket:
            if message == 'startgame':
                #开始游戏
                house.StartGame()
                house.SendToReadyClient('command','start')
                break
            message = GameHouse.unescape(message)
            house.SendToReadyClient('message',userid=user.id,username=user.UserName,message=message)
    except:
        pass
    finally:
        #玩家退出房间
        house.PopUser(user)
        house.SendToReadyClient('info',info='exit',userid=user.id,username=user.UserName)
        
def login(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data
            username = item['username']
            user = UserInfo.GetOrCreateInstance(username)
            #toDo:权限验证
            authUser = auth.authenticate(username=user.AuthUser.username,password="onlytest")
            auth.login(request, authUser)
            request.session['username'] = user.UserName

            return HttpResponseRedirect("/")
    else:
        form = UserForm()
        return render(request,'login.html',context_instance=RequestContext(request,{
                'form':form,
            }))

