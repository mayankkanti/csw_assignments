from django import forms

from .models import Comment


class ArticleShareForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    recipient_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
