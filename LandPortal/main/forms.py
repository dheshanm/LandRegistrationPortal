from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import LandHolder, Land

class OwnerDetailsForm(forms.ModelForm):
	class Meta:
		model = LandHolder
		fields = ['LandHolder_aadhaar']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Confirm'))

class LandDetailsForm(forms.ModelForm):
	class Meta:
		model = Land
		fields = ['Land_state', 'Land_district', 'Land_taluk', 'Land_village', 'Land_survey_number', 'Land_subdivision_number']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Confirm'))
