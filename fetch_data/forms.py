from django import forms
   
# creating a form 
class InputForm(forms.Form):
   
    month = forms.IntegerField(
                     help_text = "Enter the month"
                     )
    year = forms.IntegerField(
                     help_text = "Enter the year"
                     )