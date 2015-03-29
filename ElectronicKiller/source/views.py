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

clients = {}
users = {}

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


def send_info_msg(info,user,house):
    content = {}
    content['info'] = info
    content['userid'] = user.id
    content['username'] = user.UserName
    house.SendToReadyClient('info',content)

def get_user_list(request):
    user_list = parser_users(users)
    response = HttpResponse(json.dumps(user_list),content_type=u'application/json')
    return response

def escape(message):
    return message.encode('unicode_escape')

def unescape(message):
    return message.replace('%u','\u').decode('unicode_escape')

"""
进行聊天的socket通信函数
"""
@accept_websocket
def chat(request):
    key = request.GET['sid']
    s = Session.objects.get(session_key=key)
    uid = s.get_decoded().get('_auth_user_id')
    auth_user = User.objects.get(pk=uid)
    user = auth_user.userinfo
    #user = request.user.userinfo
    #print user.id
    house = gameHouses[1]
    try:
        if clients.has_key(user.id):
            data = {'type':'command','content':'close'}
            clients[user.id].send(json.dumps(data))
            clients[user.id].close()

        clients[user.id] = request.websocket
        house.readyClients[user.id] = request.websocket
        #将玩家加入房间
        house.PushUser(user)
        print len(house.users)
        send_info_msg('login',user,house)

        for message in request.websocket:
            if message == 'startgame':
                #开始游戏
                house.StartGame()
                house.SendToReadyClient('command','start')
                break
            print message
            message = unescape(message)
            content = {}
            content['userid'] = user.id
            content['username'] = user.UserName
            content['message'] = message
            house.SendToReadyClient('message',content)
    except:
        pass
    finally:
        clients.pop(user.id)
        #玩家退出房间
        house.PopUser(user)
        send_info_msg('exit',user,house)
        
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




"""以下内容用作测试"""
clientss = []

def echo_index(request):
    return render(request,
            'test.html',
            context_instance = RequestContext(request,
            {
                'title':'聊天室',
                'year':datetime.now().year,
            }))

@accept_websocket
def echo(request):
    if request.is_websocket():
        try:
            clientss.append(request.websocket)
            for message in request.websocket:
                for client in clientss:
                    client.send(message)
        except:
            pass
        finally:
            print 'out'
            clientss.remove(request.websocket)
