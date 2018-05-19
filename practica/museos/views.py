# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from museos.models import Museums, Selected, Comments, User_Page, Scored
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import auth
import time
from museos.analyze import analyze_XML


def show():	
	full_BBDD = False
	museums = Museums.objects.all()
	if len(museums) != 0:
		full_BBDD = True
	return full_BBDD


def home(request):
	if request.method == 'GET':
		# Variable para mostrarla en el 'registration_box' en el caso de que el usuario esté registrado.
		user_login = request.user

		# Variable para mostrarla o no un aspecto u otro en el caso de que la BBDD esté o no vacía.
		full_BBDD = show()

		museums2show = None
		string = ""
		# NOTA: Obtención de la Query String: https://docs.djangoproject.com/en/1.8/ref/request-response/
		qs = request.META['QUERY_STRING']
		# NOTA: Información para sacar el listado de los 5 museos con más comentario: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
			# Con el annotate(num_comments) es como si "añadieramos" a la tabla 'Museums' un nuevo campo denominado 'num_comments'.
		commented_museums = Museums.objects.annotate(num_comments = Count('comments')).order_by('-num_comments')[:5]
		button = "<a href='/?ACCESIBLES'>" + "<button> Accesibles </button>" + "</a><br>"
		if qs == "ACCESIBLES":
			string = "<i>¿Te apetece salir de museos por Madrid?</i> A continuación, se muestra una lista con todos los museos accedibles en este momento."
			museums2show = Museums.objects.filter(Accessibility = 1)
			button = "<a href='/?TODOS'>" + "<button> Todos </button>" + "</a><br>"
		elif qs == "TODOS":
			# NOTA: Supongo que tras terminar de mostrar todos los museos, no aparecerá ningun botón con enlace.
			string = "Estos son todos los museos que tenemos en la BBDD en este momento. Espero que encuentres lo que busques."
			museums2show = Museums.objects.all()
			button = None

		# Bloque para sacar el listado con enlaces a las páginas personales.
		personal_pages = ""
		pages = User_Page.objects.all()
		for name in pages:
			username = name.User
			title = name.Title
			if not title:
				title = "Página de " + username
			personal_pages += "<a href='/" + username + "'>" + title + "</a> | " + username + "<br/><br/>"
		
		return render_to_response('index.html', {'user': user_login, 'commented_museums': commented_museums, 'personal_pages': personal_pages, 
												'str': string, 'button': button, 'museums2show': museums2show, 'full_BBDD': full_BBDD})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def BBDD(request):
	if request.method == 'POST' and "update_BBDD" in request.POST:
		# Al principio de todo es necesario restaurar la BBDD, para no repetir museos.
		d = Museums.objects.all()
		d.delete()
		XML = analyze_XML()
		return HttpResponseRedirect('/')
	else:
		return render_to_response('error.html', {'code': 405})


def xml_home(request):
	if request.method == 'GET':
		commented_museums = Museums.objects.annotate(num_comments = Count('comments')).order_by('-num_comments')[:5]
		personal_pages = User_Page.objects.all()
		accessibility_museums = Museums.objects.filter(Accessibility = 1)
		museums = Museums.objects.all()
		return render_to_response('xml_home.xml', {'commented_museums': commented_museums, 'personal_pages': personal_pages, 
													'accessibility_museums': accessibility_museums, 'museums': museums}, content_type = "text/xml")
	else:
		return render_to_response('error.html', {'code': 405})


def change_title(request, username):
	if request.method == 'POST':
		title = request.POST['title']
		user_page = User_Page.objects.get(User = username)
		new_title = User_Page(id = user_page.id, User = user_page.User, Title = title, Font = user_page.Font, Background_Color = user_page.Background_Color)
		new_title.save()
		return new_title.Title
	elif request.method == 'GET':
		user_page = User_Page.objects.get(User = username)
		title = user_page.Title
		if not user_page.Title:
			title = "Página de " + user_page.User
		return title


@csrf_exempt
def user(request, name):
	if request.method == 'GET' or request.method == 'POST':	# El 'POST' es necesario para el bloque de cambiar el título.
		# Variable para mostrarla en el 'registration_box' en el caso de que el usuario esté registrado.
		user_login = request.user

		try:
			user = User.objects.get(username = name)
		except User.DoesNotExist:
			return render_to_response('error.html', {'code': 404})

		# Bloque para cambiar el título 
		title = change_title(request, user.username)

		# NOTA: Obtención de la Query String: https://docs.djangoproject.com/en/1.8/ref/request-response/
		qs = request.META['QUERY_STRING']
		if qs == "":
			qs = 0
			# Un usuario sólo puede seleccionar una vez el museo --> ese control lo realizo en la página del museo (show_select)
			museums = Selected.objects.filter(User = user).order_by('-User')[qs:((qs + 1) * 5)]
		else:
			qs = int(qs)
			museums = Selected.objects.filter(User = user)[(qs * 5):((qs + 1) * 5)]

		# ¿Necesito mostrar más?
		more_museums = Selected.objects.filter(User = user)[((qs + 1) * 5):]
		button = None 
		if len(more_museums) > 0:
			qs += 1
			button = "<a href='/" + name + "?" + str(qs) + "'>" + "<button> Ver más </button>" + "</a><br>"
		return render_to_response('user.html', {'user': user_login, 'user_page': user, 'museums': museums, 'title': title, 'button': button})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def museums(request):
	# Variable para mostrarla en el 'registration_box' en el caso de que el usuario esté registrado.
	user_login = request.user

	# Variable para mostrarla o no un aspecto u otro en el caso de que la BBDD esté o no vacía.
	full_BBDD = show()
	
	# NOTA: Es necesario sacar una lista de los distritos 'unívocos' para pasarlo al formulario. 
		# Gracias al list(set()) lo que obtengo es los valores no repetidos de una lista. 
	# NOTA: La informacion de la lista de valores la saqué de https://docs.djangoproject.com/en/2.0/ref/models/querysets/
	districts = list(set(Museums.objects.all().values_list('District')))
	# NOTA: Es necesario cambiar las tuplas a listas para el desplegable https://stackoverflow.com/questions/10941229/convert-list-of-tuples-to-list
	districts = [districts[0] for districts in districts]

	if request.method == 'GET':
		museums = Museums.objects.all()
		return render_to_response('museums.html', {'user': user_login, 'museums': museums, 'districts': districts, 'full_BBDD': full_BBDD}) 
	elif request.method == 'POST':
		dm = request.POST['Option']
		if dm == "Todos":
			museums = Museums.objects.all()
		else:
			museums = Museums.objects.filter(District = dm)
		return render_to_response('museums.html', {'user': user_login, 'museums': museums, 'districts': districts, 'full_BBDD': full_BBDD})  
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def museum_page(request, id):
	if request.method == 'GET':
		# Variable para mostrarla en el 'registration_box' en el caso de que el usuario esté registrado.
		user_login = request.user

		try:
			museum = Museums.objects.get(id = id)

			# Bloque para sacar la puntuación total del museo en cuestión.
			scored_list = Scored.objects.filter(Museum = museum)
			scored = len(scored_list)
				
			# Variable para mostrarla si el usuario puede añadir o eliminar la selección de un museo.
			show_select = True	
			selections = Selected.objects.filter(User = user_login)
			for selection in selections:
				# No puede seleccionar algo seleccionado.
				if museum.Name == selection.Museum.Name:
					show_select = False

			comments = Comments.objects.filter(Museum = museum)
			return render_to_response('museum_page.html', {'user': user_login, 'museum': museum, 'comments': comments, 
										'show_select': show_select, 'scored': scored})  
		except Museums.DoesNotExist:
			return render_to_response('error.html', {'code': 404})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def delete_museum(request, id):
	if request.method == 'POST':
		museum = Museums.objects.get(id = id)
		museum = Museums.objects.get(Name = museum)
		user_login = request.user
		instance = Selected.objects.get(Museum = museum, User = user_login)
		instance.delete()
		URL = "/museos/" + str(id)
		return HttpResponseRedirect(URL)
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def select_museum(request, id):
	if request.method == 'POST':
		museum = Museums.objects.get(id = id)
		date = time.strftime("%d/%m/%y")
		user_login = request.user
		new_selection = Selected(Museum = museum, User = user_login, Date = date)
		new_selection.save()
		URL = "/museos/" + str(id)
		return HttpResponseRedirect(URL)
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def comment_museum(request, id):
	if request.method == 'POST':
		if 'comment' in request.POST:
			museum = Museums.objects.get(id = id)
			comment = request.POST['comment']
			if comment: # Para el caso de que el mensaje venga vacio.
				new_comment = Comments(Museum = museum,  Commentary = comment)
				new_comment.save()
		URL = "/museos/" + str(id)
		return HttpResponseRedirect(URL)
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def rate_museum(request, id):
	if request.method == 'POST':
		museum = Museums.objects.get(id = id)
		new_scored = Scored(Museum = museum)
		new_scored.save()
		URL = "/museos/" + str(id)
		return HttpResponseRedirect(URL)
	else:
		return render_to_response('error.html', {'code': 405})


def xml_user(request, name):
	if request.method == 'GET':
		try:
			user = User.objects.get(username = name)
		except User.DoesNotExist:
			return render_to_response('error.html', {'code': 404})

		selection = Selected.objects.filter(User = user)
		# El content_type = "text/xml" indica como quiero mostrar los datos en el navegador.
		return render_to_response('xml_user.xml', {'user': user, 'selection': selection}, content_type = "text/xml")
	else:
		return render_to_response('error.html', {'code': 405})


def about(request):
	if request.method == 'GET':
		# Variable para mostrarla en el registration-box
		user_login = request.user
		return render_to_response('about.html', {'user': user_login})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def login(request):
	# http://librosweb.es/libro/django_1_0/capitulo_12/utilizando_usuarios.html 
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None and user.is_active:
			auth.login(request, user)
		return HttpResponseRedirect("/")
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def register(request):
	# https://docs.djangoproject.com/en/2.0/ref/contrib/auth/
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		try:
			# Compruebo que el usuario no esté ya registrado (solo puede haber nombre unívocos)
			# Si lo estuviera, lo resuelvo logeandolo
			user = User.objects.get(username = username)
			user = auth.authenticate(username = username, password = password)
			if user is not None and user.is_active:
				auth.login(request, user)
		except User.DoesNotExist:
			user = User.objects.create_user(username = username, email = email, password = password)
			user.save()

			# Dada la implementación que he realizado, tras dar de alta a los usuarios, es necesario proporcionarle una Pagina de usuario
			user = User_Page(User = user.username)
			user.save()
		return HttpResponseRedirect("/")
	elif request.method == 'GET':
		show_record = True
		return render_to_response('index.html', {'show_record': show_record})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def password(request):
    # http://librosweb.es/libro/django_1_0/capitulo_12/utilizando_usuarios.html 
	if request.method == 'POST':
		user = User.objects.get(username = request.user.username)
		new_password = request.POST['password']
		user.set_password(new_password)
		user.save()
		return HttpResponseRedirect("/")
	elif request.method == 'GET':
		show_pass = True
		return render_to_response('index.html', {'show_pass': show_pass})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def define_style(request):
	default_background_color = "#F0F0F0"
	default_font_size = '0.7'
	if request.method == "GET":
		if request.user.is_authenticated():
			try:
				user_page = User_Page.objects.get(User = request.user.username)
				background_color = user_page.Background_Color
				font_size = user_page.Font
				if not background_color or not font_size:
					background_color = default_background_color
					font_size = default_font_size
			# Metodo de control: Me paso cuando un usuario está registrado pero no tiene Pagina personal. USUARIO ROOT (al principio)
			except User_Page.DoesNotExist:
				background_color = default_background_color
				font_size = default_font_size
		else:
			background_color = default_background_color
			font_size = default_font_size
		return render_to_response('style.css', {'background_color': background_color, 'font_size': font_size}, content_type = "text/css")
	elif request.method == 'POST':
		background_color = request.POST['background_color']
		font_size =request.POST['font']
		user_page = User_Page.objects.get(User = request.user.username)
		new_title = User_Page(id = user_page.id, User = user_page.User, Title = user_page.Title, Font = font_size, Background_Color = background_color)
		new_title.save()
		return HttpResponseRedirect("/" + user_page.User)
	else:
		return render_to_response('error.html', {'code': 405})
