from django import forms

class CreateNewSuperMarket(forms.Form):
    supermarket_id = forms.IntegerField(label="Supermarket Identifier")
    supermarket_name = forms.CharField(label="Supermarket name", max_length=50)
    
