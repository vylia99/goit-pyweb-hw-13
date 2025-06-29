from django.shortcuts import render, redirect, get_object_or_404
from .models import Tag, Quote

from .forms import TagForm, QuoteForm, AuthorForm


def main(request):
    return render(request, 'quoteapp/index.html', {"quotes": Quote.objects.all()})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


def quote(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)

            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect('quoteapp:main')
        else:
            return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quoteapp/quote.html', {"tags": tags, 'form': QuoteForm()})


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoteapp/detail.html', {"quote": quote})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quoteapp:main')
    else:
        form = AuthorForm()
    return render(request, 'quoteapp/author.html', {"form": form})
