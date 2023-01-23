from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    def save(self, commit=True):
        user = super().save(commit=True)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user