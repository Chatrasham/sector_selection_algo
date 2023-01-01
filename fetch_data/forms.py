from django import forms
   
# creating a form 
class RankForm(forms.Form):
   
    month = forms.IntegerField(
                     )
    year = forms.IntegerField(
                     )

class PerformanceForm(forms.Form):
   
    month = forms.IntegerField(
                     )
    year = forms.IntegerField(
                     )