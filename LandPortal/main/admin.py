from django.contrib import admin
from .models import LandDetail, Transaction, Block
# from .models import LandHolder, Land

# Register your models here.

# class LandHolderAdmin(admin.ModelAdmin):
# 	fields = ["LandHolder_date_created",
# 			  "LandHolder_aadhaar"]

# class LandAdmin(admin.ModelAdmin):
# 	fieldsets = [
# 		("Date", {
# 			'fields': ["Land_date_added"]
# 		}),
# 		("Land Metadata", {
# 			'fields': ["Land_state",
# 					   "Land_district",
# 					   "Land_taluk",
# 					   "Land_village",
# 					   "Land_survey_number",
# 					   "Land_subdivision_number"]
# 		})
# 	]

# admin.site.register(LandHolder, LandHolderAdmin)
# admin.site.register(Land, LandAdmin)

class TransactionAdmin(admin.ModelAdmin):
	fieldsets = [
		("Land Holder", {
			'fields': ["LandHolder_aadhaar"]
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

class BlockAdmin(admin.ModelAdmin):
	fieldsets = [
		("Block Details", {
			'fields': ["index",
					   "timestamp",
					   "previous_hash",
					   "nonce",
					   "hash"]
		})
	]

class LandDetailsAdmin(admin.ModelAdmin):
	fieldsets = [
		("Land Holder", {
			'fields': ["LandHolder_aadhaar"]
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

# admin.site.register(LandDetails, LandDetailsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Block, BlockAdmin)