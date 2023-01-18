from django import forms
   
METHOD_CHOICES = (
    ("Decision Tree", "Decision Tree"),
    ("Random Forest Regressor", "Random Forest Regressor"),
    ("K Neighbors Regressor", "K Neighbors Regressor"),
    ("Kernel Ridge", "Kernel Ridge"),
    ("Support Vector Regressor", "Support Vector Regressor"),
    ("Neural Network", "Neural Network"),
    ("Combine Decision Tree and K Neighbors and Kernel Ridge", "Combine Decision Tree and K Neighbors and Kernel Ridge"),
    ("Combine Decision Tree and SVR and Neural Network", "Combine Decision Tree and SVR and Neural Network"),
    ("Combine K Neighbors and Kernel Ridge and Neural Network", "Combine K Neighbors and Kernel Ridge and Neural Network"),
)

TARGET_CHOICES = (
    ("excess_next_1m_return", "Next 1 Month"),
    ("excess_next_3m_return", "Next 3 Month"),
    ("excess_next_6m_return", "Next 6 Month"),
)

# creating a form 
class RankForm(forms.Form):
   
    month = forms.IntegerField(
                     )
    year = forms.IntegerField(
                     )
    method = forms.ChoiceField(choices = METHOD_CHOICES)

    target =   forms.ChoiceField(choices = TARGET_CHOICES)

class PerformanceForm(forms.Form):
   
    month = forms.IntegerField(
                     )
    year = forms.IntegerField(
                     )