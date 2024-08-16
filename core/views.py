from django.shortcuts import render
from book.models import BookModel, bookCategory

def HomeView(request, slug=None):
    books = BookModel.objects.all()
    categories = bookCategory.objects.all()
    
    if slug is not None:
        category = bookCategory.objects.get(slug=slug)
        books = BookModel.objects.filter(category=category)
    
    return render(request, 'homepage.html', {'books': books, 'categories': categories})