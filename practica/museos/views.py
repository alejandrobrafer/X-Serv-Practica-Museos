# Create your views here.

from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from museos.models import Museums, Selected, Comments, User_Page
from django.contrib.auth.models import User
# https://docs.djangoproject.com/en/2.0/topics/db/aggregation/ --> Para mostrar los museos con mas comentarios
from django.db.models import Count
from django.contrib import auth


@csrf_exempt
def home(request):
	if request.method == 'GET':
		user_login = request.user
		
		# Nota: Abra una parte con el filtrado del XML de Museos de Madrid.
		museums2show = None
		string = ""
		# Obtención de la Query String: https://docs.djangoproject.com/en/1.8/ref/request-response/
		qs = request.META['QUERY_STRING']
		# 1/ Listado de los 5 museos con más comentario: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
		# Con el annotate(num_comments) es como si añadieramos a la tabla Museums un nuevo campo denominado 'num_comments'
		commented_museums = Museums.objects.annotate(num_comments = Count('comments')).order_by('-num_comments')[:5]
		button = "<a href='/?ACCESIBLES'>" + "<button> Ver más...</button>" + "</a><br>"
		if qs == "ACCESIBLES":
			string = "accesibles."
			museums2show = Museums.objects.filter(Accessibility = 1)
			button = "<a href='/?TODOS'>" + "<button> Ver más...</button>" + "</a><br>"
		elif qs == "TODOS":
			# NOTA: Supongo que tras terminar de mostrar todos los museos, no aparecerá ningun botón con enlace.
			string = "que tenemos actualmente."
			museums2show = Museums.objects.all()
			button = None

		# 2/ Listado con enlaces a las páginas personales
		# NOTA: He distinguido que un usuario esté registrado, pero no tenga pagina personal (es decir el adjetivo disponible del enunciado)
		personal_pages = ""
		pages = User_Page.objects.all()
		for name in pages:
			username = name.User
			title = name.Title
			if not title:
				title = "Página de " + username
			personal_pages += "<a href='/" + username + "'>" + title + "</a> | " + username + "<br/><br/>"
		
		return render_to_response('index.html', {'user': user_login, 'commented_museums': commented_museums, 'personal_pages': personal_pages, 
												'str': string, 'button': button, 'museums2show': museums2show})
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)


@csrf_exempt
def user(request, name):
	if request.method == 'GET':	
		user_login = request.user
		
		# NOTA: QUE PASA SI EL MISMO USUARIO SELECCIONA EL MISMO MUSEO 2 O MAS VECES <----> Idea en Notas
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
			museums = Selected.objects.filter(User = user).order_by('-User')[qs:((qs + 1) * 5)]
		else:
			qs = int(qs)
			museums = Selected.objects.filter(User = user)[(qs * 5):((qs + 1) * 5)]

		#¿Necesito mostrar más?
		more_museums = Selected.objects.filter(User = user)[((qs + 1) * 5):]
		button = None 
		if len(more_museums) > 0:
			qs += 1
			button = "<a href='/" + name + "?" + str(qs) + "'>" + "<button> Ver más...</button>" + "</a><br>"

		return render_to_response('user.html', {'user': user_login, 'museums': museums, 'name': name, 'button': button})
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)


@csrf_exempt
def museums(request):
	# NOTA: supongo que aqui es donde se añadiran los museos a un usuario registrado
	
	user_login = request.user
	# Es necesario sacar una lista de los distritos para pasarlo al formulario
	# Con el list(set()) lo que obtengo es los valores no repetidos de una lista
	# value_list: https://docs.djangoproject.com/en/2.0/ref/models/querysets/
	districts = list(set(Museums.objects.all().values_list('District')))
	# https://stackoverflow.com/questions/10941229/convert-list-of-tuples-to-list
	districts = [districts[0] for districts in districts]

	if request.method == 'GET':
		museums = Museums.objects.all()
		return render_to_response('museums.html', {'user': user_login, 'museums': museums, 'districts': districts}) 
	elif request.method == 'POST':
		dm = request.POST['Option']
		if dm == "Todos":
			museums = Museums.objects.all()
		else:
			museums = Museums.objects.filter(District = dm)
		return render_to_response('museums.html', {'user': user_login, 'museums': museums, 'districts': districts})  
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)

@csrf_exempt
def museum_page(request, id):
	if request.method == 'GET' or request.method == 'POST':
		# Variable para mostrarla en el registration-box
		user_login = request.user
		try:
			museum = Museums.objects.get(id = id)
			if request.method == 'POST':
				comment = request.POST['comment']
				new_comment = Comments(Museum = museum,  Commentary = comment)
				new_comment.save()
			comments = Comments.objects.filter(Museum = museum)
			return render_to_response('museum_page.html', {'user': user_login, 'museum': museum, 'comments': comments})  
		except Museums.DoesNotExist:
			response = "Page not found"
			# NOTA: Faltaria Responder a través de un template de "Page Not Found"
			return HttpResponseNotFound(response)
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)


def xml_user(request, name):
	if request.method == 'GET':
		try:
			user = User.objects.get(username = name)
		except User.DoesNotExist:
			# NOTA: MEJORAR CON EL USO DE UN TEMPLATES PARA USUARIO NO EXISTENTE
			return HttpResponseNotFound("USER NOT EXIT.")

		selection = Selected.objects.filter(User = user)
		# EL content_type = "text/xml" INDICA COMO QUIERO MOSTRAR LOS DATOS EN EL NAVEGADOR
		return render_to_response('xml_user.xml', {'user': user, 'selection': selection}, content_type = "text/xml")
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)


def about(request):
	#NOTA: Falta por hacer
	return HttpResponse("About")


@csrf_exempt
# http://librosweb.es/libro/django_1_0/capitulo_12/utilizando_usuarios.html --> parte opcional de registro tambien
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None and user.is_active:
			auth.login(request, user)
		return HttpResponseRedirect("/")
	else:
		response = "Method not allowed"
		return HttpResponse(response, status = 405)
