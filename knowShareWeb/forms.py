from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    passwordConfirm = forms.CharField(widget=forms.PasswordInput())

class TeacherRegistrationForm(forms.Form):
    name = forms.CharField()
    highschool = forms.CharField()
    university = forms.CharField()
    age = forms.IntegerField()
    sex = forms.IntegerField()
    
