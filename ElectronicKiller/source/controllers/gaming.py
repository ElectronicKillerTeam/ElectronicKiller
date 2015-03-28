
from source.dwebsocket.decorators import accept_websocket
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.context import RequestContext
from source.views import gameHouses

def onlinePage(request):
    
    houseId = 1
    house = gameHouses[houseId]
    return render(request,
        'gaming.html',
        context_instance = RequestContext(request,
        {
            'title':'聊天室',
            'sid':request.COOKIES['sessionid'],
            'houseId':houseId,
            'users':house.users.values()
        }))

@accept_websocket
def onlineSocket(request):
    pass
