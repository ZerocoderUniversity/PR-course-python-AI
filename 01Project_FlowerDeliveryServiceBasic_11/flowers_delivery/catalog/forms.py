from django import forms
from .models import Flower


class FlowerForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, label='Upload Image')

    class Meta:
        model = Flower
        fields = ['name', 'description', 'price', 'image_upload']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['image_upload']:
            instance.image = self.cleaned_data['image_upload'].read()
        if commit:
            instance.save()
        return instance
