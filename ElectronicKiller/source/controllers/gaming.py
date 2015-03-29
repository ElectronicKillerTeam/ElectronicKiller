
from source.dwebsocket.decorators import accept_websocket
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from source.views import gameHouses
from source.models import CardInfo
import json
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

def ajaxResponse(obj):
    return HttpResponse(json.dumps(obj),content_type=u'application/json')

def onlinePage(request):
    houseId = 1
    house = gameHouses[houseId]
    selfuser = request.user.userinfo
    users = house.users.values()
    users = [user for user in users if user.id != selfuser.id]
    return render(request,
        'gaming.html',
        context_instance = RequestContext(request,
        {
            'title':'聊天室',
            'sid':request.COOKIES['sessionid'],
            'houseId':houseId,
            'users':users,
            'selfuser':selfuser
        }))

"""
本函数演示了如何进行ajax请求
"""
def getCards(request):
    #todo:整形判断
    count = int(request.GET.get('count',0))
    hasCount = int(request.GET.get('hasCount',0))
    cards = []
    for i in range(count):
        cards.append(CardInfo.GetNewCard().GetJsonCardInfo())
    houseId = 1
    house = gameHouses[houseId]
    user = request.user.userinfo
    house.Send('getcards',{'count':count + hasCount,'userid':user.id})
    return ajaxResponse(cards)

#使用一张卡牌
def useCard(request):
    id = request.GET.get('cardid','')
    return ajaxResponse([])

def _getUserBySession(request):
    key = request.GET['sid']
    s = Session.objects.get(session_key=key)
    uid = s.get_decoded().get('_auth_user_id')
    auth_user = User.objects.get(pk=uid)
    user = auth_user.userinfo
    return user

@accept_websocket
def onlineSocket(request):
    user = _getUserBySession(request)
    houseId = 1
    house = gameHouses[houseId]
    print user.id
    house.clients[user.id] = request.websocket
    if len(house.clients) == len(house.users):
        house.Send('command','ready')
    for message in request.websocket:
        print message
        pass



