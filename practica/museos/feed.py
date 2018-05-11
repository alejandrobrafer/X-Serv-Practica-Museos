from django.contrib.syndication.views import Feed
from museos.models import Comments

# https://www.tutorialspoint.com/django/django_rss.htm
#https://www.youtube.com/watch?v=iqZIT_ke2OI
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
      link = '/museos/' + str(item.Museum.id)
      return link