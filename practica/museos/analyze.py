# Fichero para analizar los datos del fichero XML del portal de museos de Madrid.
# NOTA: Para realizarlo me he apoyado en la información ofrecida en los siguientes enlaces:
	# http://www.decodigo.com/python-leer-archivo-xml
from museos.models import Museums
import urllib.request
from xml.dom import minidom


def analyze_XML():
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
		# Dado que 'TIPO' es la última etiqueta del XML, aprovecho y guardo los datos que me interesan del museo.
		elif item == "TIPO":
			new_museum = Museums(Name = value_name, Description = value_description, Schedule = value_schedule, 
								Transport = value_transport, Accessibility = value_accessibility, URL = value_url,
								Street_Name = value_street_name, Street_Type = value_street_type, Street_Num = value_street_num,
								Locality = value_locality, Province = value_province, Postal_Code = value_postal_code, 
								Neighborhood = value_neighborhood, District = value_district, Coor_X = value_x, CoorY = value_y, 
								Latitude =  value_latitude, Length = value_length, Phone = value_phone, Email = value_email)
			new_museum.save()
		else:
			pass