import uuid
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
class Guid(object):
    @staticmethod
    def New():
        id = uuid.uuid1()
        return uuid.uuid3(id,str(id))

def GetUserByRequest(request):
    key = request.GET['sid']
    s = Session.objects.get(session_key=key)
    uid = s.get_decoded().get('_auth_user_id')
    auth_user = User.objects.get(pk=uid)
    request.userinfo = auth_user.userinfo
    return request