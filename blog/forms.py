from django import forms
from django.contrib.auth import get_user

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['readonly'] = True

    def clean(self):

        slug = self.cleaned_data.get('slug')

        if self.instance.id:
            if Post.objects.filter(slug=slug).exclude(id=self.instance.id).exists():
                self.add_error('title', "Same title can use once in a month")

        else:
            if Post.objects.filter(slug=slug).exists():
                self.add_error('title', "Same title can use once in a month")

        return self.cleaned_data

    def save(self, request, commit=True):
        post = super().save(commit=False)
        if not post.pk:
            post.author = get_user(request)
        if commit:
            post.save()
            self.save_m2m()
        return post
