from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
import uuid

STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))


#Create your models here.
class FormZero(models.Model):
	date_created = models.DateTimeField("Date Created", default=timezone.now)

class LandDetail(models.Model):
	transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	LandHolder_aadhaar = models.CharField("Aadhaar Number", max_length=20, validators=[RegexValidator(r'^\d{12}$')])
	transaction_time = models.DateTimeField("Time Created", default=timezone.now)

	Land_state = models.CharField("State", choices=STATE_CHOICES, max_length=150)
	Land_district = models.CharField("District", help_text="Enter the District, under whose jurisdiction the Land falls under.", max_length=150)
	Land_taluk = models.CharField("Taluk", max_length=150)
	Land_village = models.CharField("Village", max_length=150)
	Land_survey_number = models.PositiveIntegerField("Survey Number", validators=[MinValueValidator(1)])
	Land_subdivision_number = models.PositiveIntegerField("Subdivision Number", validators=[MinValueValidator(1)])


	def __str__(self):
		return str("TransactionID: " + str(self.transaction_id)+"\nUser: " + str(self.LandHolder_aadhaar))

class Chain(models.Model):
	length = models.PositiveIntegerField("Length")

class Peer(models.Model):
	IP = models.CharField("IP", max_length=150, null=True)
	chain = models.ForeignKey("Chain", related_name='peers', on_delete=models.CASCADE)

class Block(models.Model):
	index = models.PositiveIntegerField("index")

	timestamp = models.DateTimeField("Time Created")
	previous_hash = models.CharField("Previous Hash", max_length=150, null=True)
	nonce = models.PositiveIntegerField("Nonce")
	hash = models.CharField("Hash", max_length=150)

	chain = models.ForeignKey("Chain", related_name='chain', on_delete=models.CASCADE)

	def __str__(self):
		return str("Index: " + str(self.index))

class Transaction(models.Model):
	transaction_id = models.CharField("TransactionID", max_length=150, primary_key=True)

	LandHolder_aadhaar = models.CharField("Aadhaar Number", max_length=12)

	Land_state = models.CharField("State", max_length=150)
	Land_district = models.CharField("District", max_length=150)
	Land_taluk = models.CharField("Taluk", max_length=150)
	Land_village = models.CharField("Village", max_length=150)
	Land_survey_number = models.PositiveIntegerField("Survey Number")
	Land_subdivision_number = models.PositiveIntegerField("Subdivision Number")

	Land_hash = models.CharField("Hash", max_length=150)

	timestamp = models.DateTimeField("Time Created")
	block = models.ForeignKey("Block", related_name='transactions', on_delete=models.CASCADE)

	def __str__(self):
		return str("TransactionID: " + str(self.transaction_id)+"\nUser: " + str(self.LandHolder_aadhaar))

class T2B(models.Model):
	transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE)
	block = models.ForeignKey("Block", on_delete=models.CASCADE)

	def __str__(self):
		return str("BlockID: " + str(self.block.index)+"\nTransactionID: " + str(self.transaction.transaction_id))

class B2C(models.Model):
	block = models.ForeignKey("Block", on_delete=models.CASCADE)
	chain = models.ForeignKey("Chain", on_delete=models.CASCADE)
