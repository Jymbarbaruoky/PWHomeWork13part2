from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, ModelMultipleChoiceField

from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.none())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.none())

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()
        self.fields['tags'].queryset = Tag.objects.all()
