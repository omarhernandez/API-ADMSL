from django.conf.urls import patterns,url

urlpatterns = patterns('apps.notificacion.views', 


	 url(r'notificacion/$' ,    'notificacion' ,  name = 'notificacion_path') , 

 )
