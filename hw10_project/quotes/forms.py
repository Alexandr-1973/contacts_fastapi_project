from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, widget=TextInput())
    born_date = CharField(max_length=50, widget=TextInput())
    born_location = CharField(max_length=150, widget=TextInput())
    description = CharField(widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        exclude = ['created_at']

class QuoteForm(ModelForm):
    quote = CharField(widget=TextInput())
    tags = CharField(widget=TextInput())
    author = CharField(widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['tags', 'author', 'created_at']