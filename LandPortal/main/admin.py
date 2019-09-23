from django.contrib import admin
from .models import LandHolder, Land

# Register your models here.

class LandHolderAdmin(admin.ModelAdmin):
	fields = ["LandHolder_date_created",
			  "LandHolder_aadhaar"]

class LandAdmin(admin.ModelAdmin):
	fieldsets = [
		("Date", {
			'fields': ["Land_date_added"]
		}),
		("Land Metadata", {
			'fields': ["Land_state",
					   "Land_district",
					   "Land_taluk",
					   "Land_village",
					   "Land_survey_number",
					   "Land_subdivision_number"]
		})
	]

admin.site.register(LandHolder, LandHolderAdmin)
admin.site.register(Land, LandAdmin)