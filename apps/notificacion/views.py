from django.template import RequestContext
from django.shortcuts import render_to_response 
import json as simplejson


def notificacion(request): 





	ctx = {}
	return render_to_response('notificacion/index.html',ctx,  context_instance = RequestContext(request)  )     
