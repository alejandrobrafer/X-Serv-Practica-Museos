# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from museos.models import Museums, Selected, Comments, User_Page
from django.contrib.auth.models import User
# Museos con más comentario: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
from django.db.models import Count
from django.contrib import auth
import time
import urllib.request
from xml.dom import minidom


def analyze_XML():
 	# http://www.decodigo.com/python-leer-archivo-xml
	# Nota: Abra una parte con el filtrado del XML de Museos de Madrid.
	doc = urllib.request.urlopen('https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full')
	dom = minidom.parse(doc)

	attributes = dom.getElementsByTagName('atributo')
	for attribute in attributes:
		item = attribute.getAttribute("nombre")
		if item == "NOMBRE":
			value_name = attribute.firstChild.data
		elif item == "DESCRIPCION-ENTIDAD":
			value_description = attribute.firstChild.data
		elif item == "HORARIO":
			value_schedule = attribute.firstChild.data
		elif item == "TRANSPORTE":
			value_transport = attribute.firstChild.data
		elif item == "ACCESIBILIDAD":
			value_accessibility = attribute.firstChild.data
		elif item == "CONTENT-URL":
			value_url = attribute.firstChild.data
		elif item == "NOMBRE-VIA":
			value_street_name = attribute.firstChild.data
		elif item == "CLASE-VIAL":
			value_street_type = attribute.firstChild.data
		elif item == "NUM":
			value_street_num = attribute.firstChild.data
		elif item == "LOCALIDAD":
			value_locality = attribute.firstChild.data
		elif item == "PROVINCIA":
			value_province = attribute.firstChild.data
		elif item == "CODIGO-POSTAL":
			value_postal_code = attribute.firstChild.data
		elif item == "BARRIO":
			value_neighborhood = attribute.firstChild.data
		elif item == "DISTRITO":
			value_district = attribute.firstChild.data
		elif item == "COORDENADA-X":
			value_x = attribute.firstChild.data
		elif item == "COORDENADA-Y":
			value_y = attribute.firstChild.data
		elif item == "LATITUD":
			value_latitude = attribute.firstChild.data
		elif item == "LONGITUD":
			value_length = attribute.firstChild.data
		elif item == "TELEFONO":
			value_phone = attribute.firstChild.data
		elif item == "EMAIL":
			value_email = attribute.firstChild.data
		# Dado que TIPO es la ultima etiqueta del XML, aprovecho y guardo
		elif item == "TIPO":
			new_museum = Museums(Name = value_name, Description = value_description, Schedule = value_schedule, Transport = value_transport, Accessibility = value_accessibility, URL = value_url, Street_Name = value_street_name, Street_Type = value_street_type, Street_Num = value_street_num, Locality = value_locality, Province = value_province, Postal_Code = value_postal_code, Neighborhood = value_neighborhood, District = value_district, Coor_X = value_x, CoorY = value_y, Latitude =  value_latitude, Length = value_length, Phone = value_phone, Email = value_email)
			new_museum.save()
		else:
			pass

def show():	
	# Utilizado para mostrar o no ciertas cosas si la BBDD esta vacia
	full_BBDD = False
	museums = Museums.objects.all()
	if len(museums) != 0:
		full_BBDD = True
	return full_BBDD

@csrf_exempt
def home(request):
	if request.method == 'GET' or request.method == 'POST':
		if request.method == 'POST' and "update_BBDD" in request.POST:
			# Al principio de todo es necesario restaurar la BBDD
			d = Museums.objects.all()
			d.delete()
			XML = analyze_XML()

		# Variable para mostrarla en el registration-box
		user_login = request.user

		full_BBDD = show()

		museums2show = None
		string = ""
		# Obtención de la Query String: https://docs.djangoproject.com/en/1.8/ref/request-response/
		qs = request.META['QUERY_STRING']
		# 1/ Listado de los 5 museos con más comentario: https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
		# Con el annotate(num_comments) es como si "añadieramos" a la tabla Museums un nuevo campo denominado 'num_comments'
		commented_museums = Museums.objects.annotate(num_comments = Count('comments')).order_by('-num_comments')[:5]
		button = "<a href='/?ACCESIBLES'>" + "<button> ... </button>" + "</a><br>"
		if qs == "ACCESIBLES":
			string = "<i>¿Te apetece salir de museos por Madrid?</i> A continuación, se muestra una lista con todos los museos accedibles en este momento."
			museums2show = Museums.objects.filter(Accessibility = 1)
			button = "<a href='/?TODOS'>" + "<button> ... </button>" + "</a><br>"
		elif qs == "TODOS":
			# NOTA: Supongo que tras terminar de mostrar todos los museos, no aparecerá ningun botón con enlace.
			string = "Estos son todos los museos que tenemos en la BBDD en este momento. Espero que encuentres lo que busques."
			museums2show = Museums.objects.all()
			button = None

		# 2/ Listado con enlaces a las páginas personales
		personal_pages = ""
		pages = User_Page.objects.all()
		print("aqui")
		for name in pages:
			username = name.User
			title = name.Title
			if not title:
				title = "Página de " + username
			personal_pages += "<a href='/" + username + "'>" + title + "</a> | " + username + "<br/><br/>"
			print(personal_pages)
		
		return render_to_response('index.html', {'user': user_login, 'commented_museums': commented_museums, 'personal_pages': personal_pages, 
												'str': string, 'button': button, 'museums2show': museums2show, 'full_BBDD': full_BBDD})
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
	# NOTA IMPORTANTE: HE REALIZADO LA DISTINCION DE TRES 'TIPO DE USUARIO':
	# 1.-LOS USUARIOS REGISTRADOS
	# 2.-LOS USUARIOS QUE TIENEN PAGINA PERSONAL
	# 3.- LOS USUARIOS LOGEADOS

	if request.method == 'GET' or request.method == 'POST':	
		# Variable para mostrarla en el registration-box
		user_login = request.user

		try:
			user = User.objects.get(username = name)
		except User.DoesNotExist:
			return render_to_response('error.html', {'code': 404})

		# Bloque para cambiar el título 
		title = change_title(request, user.username)

		# Query String: https://docs.djangoproject.com/en/1.8/ref/request-response/
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
			button = "<a href='/" + name + "?" + str(qs) + "'>" + "<button> Ver más </button>" + "</a><br>"
		return render_to_response('user.html', {'user': user_login, 'user_page': user, 'museums': museums, 'title': title, 'button': button})
	else:
		return render_to_response('error.html', {'code': 405})


@csrf_exempt
def museums(request):
	# Variable para mostrarla en el registration-box
	user_login = request.user

	full_BBDD = show()
	
	# Es necesario sacar una lista de los distritos 'unívocos' para pasarlo al formulario.
	# Con el list(set()) lo que obtengo es los valores no repetidos de una lista.
	# value_list: https://docs.djangoproject.com/en/2.0/ref/models/querysets/
	districts = list(set(Museums.objects.all().values_list('District')))
	# https://stackoverflow.com/questions/10941229/convert-list-of-tuples-to-list
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
	if request.method == 'GET' or request.method == 'POST':
		# Variable para mostrarla en el registration-box
		user_login = request.user

		try:
			museum = Museums.objects.get(id = id)
			if request.method == 'POST':
				if 'comment' in request.POST:
					comment = request.POST['comment']
					new_comment = Comments(Museum = museum,  Commentary = comment)
					new_comment.save()
				elif 'select' in request.POST:
					selection = request.POST['select']
					museum = Museums.objects.get(Name = selection)
					date = time.strftime("%d/%m/%y")
					new_selection = Selected(Museum = museum, User = user_login, Date = date)
					new_selection.save()
				elif 'delete' in request.POST:
					deleted = request.POST['delete']
					museum = Museums.objects.get(Name = deleted)
					instance = Selected.objects.get(Museum = museum, User = user_login)
					instance.delete()

			# Bloque para determinar si puedo añadir/eliminar o no el museo a un usuario
			show_select = True	
			selections = Selected.objects.filter(User = user_login)
			for selection in selections:
				if museum.Name == selection.Museum.Name:
					show_select = False

			comments = Comments.objects.filter(Museum = museum)
			return render_to_response('museum_page.html', {'user': user_login, 'museum': museum, 'comments': comments, 'show_select': show_select})  
		except Museums.DoesNotExist:
			return render_to_response('error.html', {'code': 404})
	else:
		return render_to_response('error.html', {'code': 405})


def xml_user(request, name):
	if request.method == 'GET':
		try:
			user = User.objects.get(username = name)
		except User.DoesNotExist:
			return render_to_response('error.html', {'code': 404})

		selection = Selected.objects.filter(User = user)
		# EL content_type = "text/xml" INDICA COMO QUIERO MOSTRAR LOS DATOS EN EL NAVEGADOR
		return render_to_response('xml_user.xml', {'user': user, 'selection': selection}, content_type = "text/xml")
	else:
		return render_to_response('error.html', {'code': 405})


def about(request):
	if request.method == 'GET':
		return render_to_response('about.html')
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
