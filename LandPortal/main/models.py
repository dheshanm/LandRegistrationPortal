from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone

STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))


# Create your models here.
class LandHolder(models.Model):
	LandHolder_aadhaar = models.CharField("Aadhaar Number", primary_key=True, unique=True, max_length=12, validators=[RegexValidator(r'^\d{12}$')])
	LandHolder_date_created = models.DateTimeField("Date Created", default=timezone.now)

	def __str__(self):
		return str("UserID: " + str(self.LandHolder_aadhaar)+"\ndateCreated: " + str(self.LandHolder_date_created))

class Land(models.Model):
	Land_state = models.CharField("State", choices=STATE_CHOICES, max_length=150)
	Land_district = models.CharField("District", help_text="Enter the District, under whose jurisdiction the Land falls under.", max_length=150)
	Land_taluk = models.CharField("Taluk", max_length=150)
	Land_village = models.CharField("Village", max_length=150)
	Land_survey_number = models.PositiveIntegerField("Survey Number", validators=[MinValueValidator(1)])
	Land_subdivision_number = models.PositiveIntegerField("Subdivision Number", validators=[MinValueValidator(1)])

	Land_date_added = models.DateTimeField("Date Created", default=timezone.now)
