from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'categories'
        ]
