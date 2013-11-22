from django import forms
from django.contrib.auth.models import User
from django.forms import Form, ModelForm

from models import Post, Category

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class PostForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), label="Categories", widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            title = 'Edit Post'
        else:
            title = 'New Post'

        self.helper = FormHelper()
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset(title, "categories", "heading", "content",),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )

        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('heading', 'content', 'categories',)


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Fieldset("Edit Comment", "heading", "content",),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn-primary')
            )
        )

        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('heading', 'content',)
