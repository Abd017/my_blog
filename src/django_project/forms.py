from django import forms


class ContactForm(forms.Form):
    Full_name = forms.CharField()
    email = forms.EmailField()
    query = forms.CharField(widget=forms.Textarea)

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if email.endswith("edu"):
            raise forms.ValidationError("This is not valid email.")
        return email