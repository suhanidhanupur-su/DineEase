from django.db import models


class Menu(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	image = models.ImageField(upload_to='menu/', blank=True)
	category = models.CharField(max_length=80, blank=True)
	is_available = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return self.name
