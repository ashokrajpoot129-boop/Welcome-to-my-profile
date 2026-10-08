from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField(max_length=254)
    mobile_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'type': 'tel', 'autocomplete': 'tel'}),
    )
    message = forms.CharField(max_length=5000, widget=forms.Textarea)