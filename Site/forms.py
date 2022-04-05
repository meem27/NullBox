from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
	required=False,
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'Say Something...'
            }))
    image = forms.ImageField(label='',required=False)

    class Meta:
        model = Post
        fields = ['body','image']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
	required=False,
        widget=forms.Textarea(
            attrs={'rows': '1',
                   'placeholder': 'Comment'}
        ))

    class Meta:
        model = Comment
        fields = ['comment']

class ExploreForm(forms.Form):
    query = forms.CharField(
        label='',
	required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Explore tags'
        })
    )