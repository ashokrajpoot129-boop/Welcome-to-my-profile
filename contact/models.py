from django.db import models


class ContactMessage(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField(max_length=254)
	mobile_number = models.CharField(max_length=20)
	message = models.TextField(max_length=5000)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.name} <{self.email}>'
