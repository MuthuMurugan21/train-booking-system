from django import forms

class PassengerForm(forms.Form):
    name = forms.CharField(max_length=50)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
