# Create your models here.
from django.db import models

class Museums(models.Model):
	Name = models.CharField(max_length = 128)
	Description = models.TextField(null = True, blank = True)
	Schedule = models.TextField(null = True, blank = True)
	Transport = models.TextField(null = True, blank = True)
	# Solo es posible escoger entre 0 y 1.
	Accessibility = models.IntegerField(choices = ((0, '0'), (1, '1')))
	URL = models.URLField(max_length = 500, null = True, blank = True)
	Street_Name = models.CharField(max_length = 64, null = True, blank = True)
	Street_Type = models.CharField(max_length = 32, null = True, blank = True)
	Street_Num = models.PositiveIntegerField(null = True, blank = True)
	Locality = models.CharField(max_length = 32, null = True, blank = True)
	Province = models.CharField(max_length = 32, null = True, blank = True)
	Postal_Code = models.PositiveIntegerField(null = True, blank = True)
	Neighborhood = models.CharField(max_length = 32, null = True, blank = True)
	District = models.CharField(max_length = 32, null = True, blank = True)
	Coor_X = models.PositiveIntegerField(null = True, blank = True)
	CoorY = models.PositiveIntegerField(null = True, blank = True)
    # Blank = True, permite que el campo quede vacio.
    # Null = True, permite almacenamiento vacio.
	Latitude = models.FloatField(null = True, blank = True)
	Length = models.FloatField(null = True, blank = True)
	Phone = models.TextField(null = True, blank = True)
	Email = models.TextField(null = True, blank = True)
	def __str__(self):
		return self.Name

# A través del nombre del usuario yo filtro y me saldran todos los museos seleccionados por el usuario.
class Selected(models.Model):
	Museum = models.ForeignKey(Museums)
	User = models.CharField(max_length = 32)
	Date = models.DateField(auto_now = True)

class Comments(models.Model):
	Museum = models.ForeignKey(Museums)
	Commentary = models.TextField()

class User_Page(models.Model):
	User = models.CharField(max_length = 32)
	Title = models.CharField(max_length = 64 , null = True, blank = True)
	Font = models.CharField(max_length = 32, null = True, blank = True)
	Background_Color = models.CharField(max_length = 32, null = True, blank = True)
	def __str__(self):
		return self.User
