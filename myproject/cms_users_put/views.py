
from django.shortcuts import render
from models import Table
from django.http import HttpResponse,HttpResponseNotFound
from django.template.loader import get_template
from django.template import Context
# Create your views here.


def analyze (request,recurso):
    
    salida =""
    if request.method == 'GET':
        print str(request.user.is_authenticated())
        try:
            record = Table.objects.get(resource=recurso)
            return HttpResponse(record.name)
        except Table.DoesNotExist:
            
            lista=Table.objects.all()
            for fila in lista:
                salida += "<ul><li> Recurso: "+str(fila.resource)+"\r"+str(fila.name)+"</li></ul>" 
            return HttpResponseNotFound('<br>Recurso no disponible'+salida)
    elif request.method == 'PUT':
        print str(request.user.is_authenticated())
        if request.user.is_authenticated():
            record = Table(resource= recurso,name =request.body)  
            record.save()
            return HttpResponse("<h1><p>Logged in as "  + request.user.username+"</p>Actualizando.../h1>"+ str(recurso)+"......"+str(request.body))
            
        else:
            return HttpResponse("Not logged in"+"<a href=http://"+request.get_host()+"/admin"+"> Log in</a>")
            
def template (request,recurso):
    salida=""
    try:
        record = Table.objects.get(resource=recurso)    
        template = get_template("Rounded_2/index.html")
        return HttpResponse(template.render(Context({'title': request.user,'resource': recurso,'page':record.name})))
    except Table.DoesNotExist:        
        lista=Table.objects.all()
        for fila in lista:
            salida += "<ul><li> Recurso: "+str(fila.resource)+"\r"+str(fila.name)+"</li></ul>" 
        return HttpResponseNotFound('<br>Recurso no disponible'+salida)
