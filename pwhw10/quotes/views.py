from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Author, Quote

# from .utils import get_mongodb


# def main(request, page=1):
#     db = get_mongodb()
#     quotes = db.quotes.find()
#     per_page = 10
#     paginator = Paginator(list(quotes), per_page)
#     quotes_on_page = paginator.page(page)
#     return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def main(request, page=1):
    quotes = Quote.objects.all().order_by('-id')
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, "title": "Quotes"})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
    return render(request, 'quotes/add_author.html', {"form": AuthorForm()})


def author(request, author: str):
    return render(request, 'quotes/author.html', context={"author": Author.objects.get(fullname=author)})


@login_required
def quote(request):

    if request.method == 'POST':
        form = QuoteForm(request.POST)

        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.save()
            form.save_m2m()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', {'form': form})
    return render(request, 'quotes/add_quote.html', {"form": QuoteForm()})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_tag.html', {'form': form})

    return render(request, 'quotes/add_tag.html', {'form': TagForm()})
