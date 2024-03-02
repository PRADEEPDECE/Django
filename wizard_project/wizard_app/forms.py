from django import forms

class Step1Form(forms.Form):
    name = forms.CharField(label='Your Name')

class Step2Form(forms.Form):
    email = forms.EmailField(label='Your Email')

class Step3Form(forms.Form):
    address = forms.CharField(label='Your Address')
