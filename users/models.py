import uuid
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=255, blank=True, null=True, help_text='Endereço completo')
	city = models.CharField(max_length=100, blank=True, null=True, help_text='Cidade')
	state = models.CharField(max_length=2, blank=True, null=True, help_text='Estado (UF)')
	level = models.IntegerField(default=1)
	xp = models.IntegerField(default=0)
	max_xp = models.IntegerField(default=1000)

	def __str__(self):
		return f'Perfil de {self.user.username}'


class History(models.Model):
	STATUS_CHOICES = [
		('Ativo', 'Ativo'),
		('Resolvido', 'Resolvido'),
	]

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
	title = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	icon = models.CharField(max_length=50)
	color = models.CharField(max_length=20)
	likes = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.title} - {self.user.username}'

	@property
	def time(self):
		from django.utils import timezone

		diff = timezone.now() - self.created_at
		if diff.days == 0:
			hours = diff.seconds // 3600
			return f'Há {hours} horas'
		if diff.days == 1:
			return 'Ontem'
		return f'Há {diff.days} dias'

	class Meta:
		verbose_name_plural = 'Histories'
		ordering = ['-created_at']
