# -*- coding: utf-8 -*-
import functools
from django.http.response import HttpResponse
import json
# author: yml

#在函数上增加@ajax此装饰符即可将其转为ajax对应的response
def ajax(func):
    from functools import wraps
    @wraps(func)
    def new_func(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        return HttpResponse(json.dumps(response),content_type=u'application/json')
    return new_func