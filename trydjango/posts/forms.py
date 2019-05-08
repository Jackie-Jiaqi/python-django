from .models import Post

from django import forms


class PostForm(forms.ModelForm):
    image = forms.FileField(required=True,error_messages={"required":"Please Upload a image"})

    class Meta:
        model = Post
        fields = [
            #"title",
            "image",
            #"content",
        ]