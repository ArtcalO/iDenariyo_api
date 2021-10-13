from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
	id=models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.FloatField()
	account_number = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username+" "+self.account_number

	class Meta:
		constraints = [
			models.CheckConstraint(check=models.Q(amount__gte='0'), name='prix_prix_cannot_be_negative'),
		]

class Depot(models.Model):
	id=models.AutoField(primary_key=True)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	amount = models.FloatField()

	def __str__(self):
		return self.account+' '+self.amount

	class Meta:
		constraints = [
			models.CheckConstraint(check=models.Q(amount__gte='0'), name='d_amount_cannot_be_negative'),
		]

class Retrait(models.Model):
	id=models.AutoField(primary_key=True)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	amount = models.FloatField()
	
	def __str__(self):
		return self.account+' '+self.amount

	class Meta:
		constraints = [
			models.CheckConstraint(check=models.Q(amount__gte='0'), name='r_amount_cannot_be_negative'),
		]

class Transaction(models.Model):
	id=models.AutoField(primary_key=True)
	sender = models.ForeignKey(Account, related_name='tr_from_account', on_delete=models.CASCADE)
	reciever = models.ForeignKey(Account, related_name='tr_to_account', on_delete=models.CASCADE)
	amount = models.FloatField()



