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
    ("excess_next_1m_return", "excess_next_1m_return"),
    ("excess_next_3m_return", "excess_next_3m_return"),
    ("excess_next_6m_return", "excess_next_6m_return"),
)

# creating a form 
class RankForm(forms.Form):
   
    month = forms.IntegerField(
                     )
    year = forms.IntegerField(
                     )
    method = forms.ModelChoiceField(choices = METHOD_CHOICES)

    targer =   forms.ModelChoiceField(choices = TARGET_CHOICES)

class PerformanceForm(forms.Form):
   
    month = forms.IntegerField(
                     )
    year = forms.IntegerField(
                     )