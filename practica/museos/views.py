# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from museos.models import Museums, Selected, Comments, User_Page

MACHINE = "localhost"
PORT = 8000

form = """
<h1><font color="darkslategray"><center><u>URL shortener 2 ~ SARO 2018</u></center></font></h1>
<br>
<form action="" method="POST"><input type="text" name="Distrito" value="">
<input type="submit" value="Enviar"/><input type="reset" value="Reset"></form>
<br><br>
"""

def home(request):
	return HttpResponse("home")

	# Abra una parte con el filtrado del XML de Museos de Madrid.

	# Listado de los 5 museos con mas comentario

	# Listado con enlaces a las paginas personales

	# Boton
	return HttpResponse("home")

def user(request, name):
	return HttpResponse("Pagina del usuario " + name)

@csrf_exempt
def museums(request):
	# El filtrado de los distritos estaria bien con un desplegable con opciones
	# El formulario en un templete.
	
	if request.method == 'GET':
		museums = Museums.objects.all()
		response = "<ul>"
		for museum in museums:
			response += museum.Name + "<a href='//" + MACHINE + ":" + str(PORT) + "/museos/" + str(museum.id) + "'> Enlace</a><br>"
		response += "</ul>"
		return HttpResponse("museos" + form + response) 
	elif request.method == 'POST':
		dm = request.POST['Distrito']
		print(dm)
		district_museums = Museums.objects.filter(District = dm)
		response = "<ul>"
		for district_museum in district_museums:
			response += district_museum.Name + "<br>"
		response += "</ul>"
		return HttpResponse("museos " + response)
	else:
		response = "Method Not Allowed"
		return HttpResponse(response, status = 405)


def museum_page(request, id):
	return HttpResponse("Pagina del museo" + str(id))

def xml_user(request, name):
	return HttpResponse("XML del usuario " + name)

def about(request):
	return HttpResponse("About")
