# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from museos.models import Museums, Selected, Comments, User_Page
from django.contrib.auth.models import User

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

@csrf_exempt
def user(request, name):
	return HttpResponse("hola")


@csrf_exempt
def museums(request):
	# El filtrado de los distritos estaria bien con un desplegable con opciones
	# El formulario en un templete.
	# Añadir CSS
	
	if request.method == 'GET':
		museums = Museums.objects.all()
		response = "<ul>"
		for museum in museums:
			response += "<a href='//" + MACHINE + ":" + str(PORT) + "/museos/" + str(museum.id) + "'>" + museum.Name + "</a><br>"
		response += "</ul>"
		return HttpResponse("museos" + form + response) 
	elif request.method == 'POST':
		dm = request.POST['Distrito']
		district_museums = Museums.objects.filter(District = dm)
		response = "<ul>"
		for district_museum in district_museums:
			response += district_museum.Name + "<br>"
		response += "</ul>"
		return HttpResponse("museos " + response)
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)


def museum_page(request, id):
	# Mostrar todos los datos del museo y los comentarios asociados
	try:
		museum = Museums.objects.get(id = id)
		comments = Comments.objects.filter(Museum = museum)
		response = "<ul>"
		for commentary in comments:
			response += commentary.Commentary + "<br>"
		response += "</ul>"

		return HttpResponse(museum.Name + response)	# Falta mostrar todos los datos restantes del museo
	except Museums.DoesNotExist:
		response = "Page not found"
		return HttpResponseNotFound(response)

def xml_user(request, name):
	try:
		user = User.objects.get(username = name)
	except User.DoesNotExist:
		# NOTA: MEJORAR CON EL USO DE UN TEMPLATES PARA USUARIO NO EXISTENTE
		return HttpResponseNotFound("USER NOT EXIT.")

	museum_selection = Selected.objects.filter(User = user)
	# EL content_type = "text/xml" INDICA COMO QUIERO MOSTRAR LOS DATOS EN EL NAVEGADOR
	return render_to_response('xml_user.xml', {'user': user, 'selection':museum_selection}, content_type = "text/xml")

def about(request):
	return HttpResponse("About")
