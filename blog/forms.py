from django.forms import ModelForm, ChoiceField, CharField
from django import forms
from .models import Search
from django.core.validators import MinLengthValidator

class SearchForm(ModelForm):
    class Meta:
        model = Search
        exclude = ['from_user']

class LinkedinForm(forms.Form):

    action = forms.ChoiceField(widget=forms.Select(),choices= ([(1, "Name Search"),(2, "Company Search"), (3, "People with Job"), (4, "Group Search"),]))
    search_for = forms.CharField(MinLengthValidator(1))
