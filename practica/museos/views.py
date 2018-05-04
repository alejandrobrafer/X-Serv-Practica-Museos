# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from museos.models import Museums, Selected, Comments, User_Page
# ACCESO A TRAVES DE ESTE MODELO DADO QUE UN USUARIO SOLO PUEDE TENER MUSEOS SELECCIONADOS SI ESTA REGISTRADO
from django.contrib.auth.models import User
# https://docs.djangoproject.com/en/2.0/topics/db/aggregation/ --> Para mostrar los museos con mas comentarios
from django.db.models import Count

MACHINE = "localhost"
PORT = 8000

form = """
<h1><font color="darkslategray"><center><u>URL shortener 2 ~ SARO 2018</u></center></font></h1>
<br>
<form action="" method="POST"><input type="text" name="Distrito" value="">
<input type="submit" value="Enviar"/><input type="reset" value="Reset"></form>
<br><br>
"""

# NOTA: HE SUPUESTO QUE UNICAMENTE LOS USUARIOS QUE SE ENCUENTRAS REGISTRADOS SON LOS QUE TENDRAN PAGINA
def home(request):

	# Abra una parte con el filtrado del XML de Museos de Madrid.

	# Listado de los 5 museos con mas comentario
	# Con el annotate(num_comments) es como si añadieramos a la tabla Museums un nuevo campo denominado numero de comentarios
	commented_museums = Museums.objects.annotate(num_comments = Count('comments')).order_by('-num_comments')[:5]
	response = ""
	for commented_museum in commented_museums:
		# NOTA: ME SALTA EL PROBLEMA DE QUE SIEMPRE SALEN 5 AUN NO HABIENDO COMENTARIO
		# SOLUCION
		if commented_museum.num_comments > 0:
			response += commented_museum.Name + "<br/>"
	
	# Listado con enlaces a las paginas personales
	response1 = ""
	pages = User_Page.objects.all()
	for name in pages:
		username = name.User
		link = "<a href='//" + MACHINE + ":" + str(PORT) + "/" + username + "'>" + username + "</a><br>"
		title = name.Title
		if not title:
			title = "Página de " + username
		show = link + title
		response1 += show + "<br/>"

	# Boton
	# Obtención de la Query String
	# https://docs.djangoproject.com/en/1.8/ref/request-response/
	qs = request.META['QUERY_STRING']

	if qs == "":
		qs = "ACCESIBLES"
		button = "<a href='//" + MACHINE + ":" + str(PORT) + "/" + "?" + qs + "'>" + "MAS" + "</a><br>"
	elif qs == "ACCESIBLES":
		# NOTA LOS PRINT SON DE COPROBACION, DEBERIAN IR EN EL HTML
		access_museums = Museums.objects.filter(Accessibility = 1)
		print(access_museums)
		button = "<a href='//" + MACHINE + ":" + str(PORT) + "/" + "?" + qs + "'>" + "MAS" + "</a><br>"
	elif qs == "TODOS":
		button = "<a href='//" + MACHINE + ":" + str(PORT) + "/" + "?" + qs + "'>" + "MAS" + "</a><br>"
	return HttpResponse(response + response1)

@csrf_exempt
def user(request, name):
	# NOTA: QUE PASA SI EL MISMO USUARIO SELECCIONA EL MISMO MUSEO 2 O MAS VECES
	# POSIBLE SOLUCION:
	# Obtengo los valores unicos de una lista
    # http://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
	# NOTA: FALTA LA FECHA DE SELECCION
	try:
		user = User.objects.get(username = name)
	except User.DoesNotExist:
		# NOTA: MEJORAR CON EL USO DE UN TEMPLATES PARA USUARIO NO EXISTENTE
		return HttpResponseNotFound("USER NOT EXIT.")

	# Obtención de la Query String
	# https://docs.djangoproject.com/en/1.8/ref/request-response/
	qs = request.META['QUERY_STRING']
	
	if qs == "":
		qs = 0
		# 1 usuario = 1 museo seleccionado --> museo = usuario
		# Lo que muestro son los 5 primeros 

		# NOTA LOS PRINT SON DE COPROBACION, DEBERIAN IR EN EL HTML
		print("Mostrados los primeros 5 museos")
		museums = Selected.objects.filter(User = user)[qs:((qs + 1) * 5)]
		print(museums)
	else:
		print("Mostrados los sigueintes museos")
		qs = int(qs)
		museums = Selected.objects.filter(User = user)[(qs * 5):((qs + 1) * 5)]
		print(museums)

	#¿necesito mostrar el enlace MAS?
	more_museums = Selected.objects.filter(User = user)[((qs + 1) * 5):]
	more = ""
	if len(more_museums) > 0:
		qs += 1
		more = "<a href='//" + MACHINE + ":" + str(PORT) + "/" + name + "?" + str(qs) + "'>" + "MAS" + "</a><br>"

	return HttpResponse(more)

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

		return HttpResponse(museum.Name + response)	# Falta mostrar todos los datos restantes del museo --- Solucion igual que xml-user con un HTML
	except Museums.DoesNotExist:
		response = "Page not found"
		return HttpResponseNotFound(response)

def xml_user(request, name):
	try:
		user = User.objects.get(username = name)
	except User.DoesNotExist:
		# NOTA: MEJORAR CON EL USO DE UN TEMPLATES PARA USUARIO NO EXISTENTE
		return HttpResponseNotFound("USER NOT EXIT.")

	selection = Selected.objects.filter(User = user)
	# EL content_type = "text/xml" INDICA COMO QUIERO MOSTRAR LOS DATOS EN EL NAVEGADOR
	return render_to_response('xml_user.xml', {'user': user, 'selection': selection}, content_type = "text/xml")


def about(request):
	return HttpResponse("About")
