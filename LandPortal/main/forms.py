from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import LandDetail, FormZero
from django.db import models

class SearchForm(forms.Form):
    query_Aadhaar = forms.CharField(label='Aadhaar to Search', max_length=20)

    def query_Aadhaar(self):
        data = self.cleaned_data['query_Aadhaar']
        data = data.replace('/', '')
        data = data.replace(' ', '')
        return data

class LandForm(forms.ModelForm):
    class Meta:
        model = LandDetail
        fields = ['Land_state', 'Land_district', 'Land_taluk', 'Land_village', 'Land_survey_number', 'Land_subdivision_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirm'))

class LandDetailsForm(forms.ModelForm):
    class Meta:
        model = LandDetail
        fields = ['LandHolder_aadhaar', 'Land_state', 'Land_district', 'Land_taluk', 'Land_village', 'Land_survey_number', 'Land_subdivision_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirm'))

    def clean(self):
        cleaned_data = super(LandDetailsForm, self).clean()
        cleaned_data['LandHolder_aadhaar'] = cleaned_data['LandHolder_aadhaar'].replace('/', '')
        cleaned_data['LandHolder_aadhaar'] = cleaned_data['LandHolder_aadhaar'].replace(' ', '')
        return cleaned_data

class ZeroForm(forms.ModelForm):
    class Meta:
        model = FormZero
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Mine'))
