from book.models import bookCategory, BookModel, BorrowModel, CommentModel
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = bookCategory
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ['book_name', 'category', 'description', 'image', 'book_quantity', 'borrow_price']

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_body']