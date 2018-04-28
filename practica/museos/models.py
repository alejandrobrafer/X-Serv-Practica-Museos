# Create your models here.
from django.db import models

class Museums(models.Model):
	Name = models.CharField(max_length = 128)
	Description = models.TextField
	Schedule = models.TextField
	Transport = models.TextField
	# Solo es posible escoger entre 0 y 1.
	Accessibility = models.IntegerField(choices = ((0, '0'), (1, '1')))
	URL = models.URLField(max_length = 500)
	Street_Name = models.CharField(max_length = 64)
	Street_Type = models.CharField(max_length = 32)
	Street_Num = models.PositiveIntegerField
	Locality = models.CharField(max_length = 32)
	Province = models.CharField(max_length = 32)
	Postal_Code = models.PositiveIntegerField
	Neighborhood = models.CharField(max_length = 32)
	District = models.CharField(max_length = 32)
	Coor_X = models.PositiveIntegerField()
	CoorY = models.PositiveIntegerField()
    # Blank = True, permite que el campo quede vacio.
    # Null = True, permite almacenamiento vacio.
	Latitude = models.FloatField(null = True, blank = True)
	Length = models.FloatField(null = True, blank = True)
	Phone = models.TextField
	Email = models.TextField
	def __str__(self):
		return self.Name

# A través del nombre del usuario yo filtro y me saldran todos los museos seleccionados por el usuario.
class Selected(models.Model):
	Museum = models.ForeignKey(Museums)
	User = models.CharField(max_length = 32)
	Date = models.DateField(auto_now = True)
	def __str__(self):
		return self.Museum

class Comments(models.Model):
	Museum = models.ForeignKey(Museums)
	Commentary = models.TextField
	def __str__(self):
		return self.Museum

class User_Page(models.Model):
	User = models.CharField(max_length = 32)
	Title = models.CharField(max_length = 64, default = '')
	Font = models.CharField(max_length = 32, null = True, blank = True)
	Background_Color = models.CharField(max_length = 32)
	def __str__(self):
		return self.User
