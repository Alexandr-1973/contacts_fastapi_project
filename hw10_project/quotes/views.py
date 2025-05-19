from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Count
from .forms import AuthorForm, QuoteForm
from .utils import get_mongodb
from django.core.paginator import Paginator
from .models import Quote, Author, Tag


# Create your views here.

def main(request, page=1):
    quotes = Quote.objects.all()
    authors_dict = {author.id: author.fullname for author in Author.objects.all()}
    for quote in quotes:
        quote.author_name = authors_dict.get(quote.author_id)
    per_page=10
    paginator=Paginator(quotes, per_page)
    quotes_on_page=paginator.page(page)

    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[:10]

    return render(request, "quotes/index.html", context={"quotes":quotes_on_page, "top_tags": top_tags})


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author_form.html', {'form': form})

    return render(request, 'quotes/add_author_form.html', {'form': AuthorForm()})

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author']
            print(author_name)
            print(Author.objects.filter(fullname=author_name).first())
            author = Author.objects.filter(fullname=author_name).first()

            tags_str = form.cleaned_data['tags']
            tag_names = [tag.strip() for tag in tags_str.split(',')]

            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)  # Если нет - создаёт
                tags.append(tag)

            quote = form.save(commit=False)
            quote.author = author
            quote.save()

            quote.tags.set(tags)

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote_form.html', {'form': form})

    return render(request, 'quotes/add_quote_form.html', {'form': QuoteForm()})

def author(request, author_fullname):
    author=get_object_or_404(Author, fullname=author_fullname)
    return render(request, "quotes/author.html", {"author":author})

def tag(request, tag, page=1):
    tag_quotes = get_list_or_404(Quote, tags__name=tag)
    per_page=10
    paginator=Paginator(tag_quotes, per_page)
    quotes_on_page=paginator.page(page)
    return render(request, "quotes/tag.html", {"quotes":quotes_on_page, "tag":tag})


