# Fichero para la parte opcional de generación de un canal RSS para los comentarios puestos en el sitio.
# NOTA: Para realizarlo me he apoyado en la información ofrecida en los siguientes enlaces:
   # https://www.tutorialspoint.com/django/django_rss.htm
   #https://www.youtube.com/watch?v=iqZIT_ke2OI
from django.contrib.syndication.views import Feed
from museos.models import Comments


class Feeds(Feed):
   title = "Comentarios Museo | SARO 2018"
   link = ""
   description = "Canal RSS para los comentarios."

   def items(self):
      return Comments.objects.all()
		
   def item_title(self, item):
      return item.Museum
		
   def item_description(self, item):
      return item.Commentary
		
   def item_link(self, item):
      link = '/museos/' + str(item.Museum.id) # Enlace para ir a la página del museo.
      return link