from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Quote, Author


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(min_length=10, max_length=500, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=255, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
