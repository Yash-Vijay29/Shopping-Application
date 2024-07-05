from django import forms
class UploadImageForm(forms.Form):
    image = forms.ImageField()
class TextInputer(forms.Form):
    text = forms.CharField(label='Item to Search', max_length=100)