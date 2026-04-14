from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    collaborators_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type usernames separated by commas e.g. john, jane',
            'id': 'collaborators-input',
        }),
        label='Collaborators (usernames)'
    )

    class Meta:
        model = Post
        fields = ('title', 'description', 'tech_stack', 'live_link', 'github_repo', 'image')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Title',
                'maxlength': '200',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project: what it does, how you built it, challenges you overcame...',
            }),
            'tech_stack': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'React, Django, PostgreSQL, AWS...',
            }),
            'live_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://your-project.com',
            }),
            'github_repo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername/repo',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

    def clean_live_link(self):
        url = self.cleaned_data.get('live_link')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            raise forms.ValidationError("Live link must be a valid URL starting with http:// or https://")
        return url


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add a comment...',
                'id': 'comment-input',
            }),
        }
