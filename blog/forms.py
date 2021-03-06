from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # input text type field 
    name = forms.CharField(max_length=25)
    # 'email' and 'to' fields require valid email addresses
    email = forms.EmailField()
    to = forms.EmailField()
    # comment field is optional to get validation
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
