from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class bookCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True,null=True, blank=True, )

    def __str__(self):
        return f'{self.name}'


class BookModel(models.Model):
    book_name = models.CharField(max_length=255)
    category = models.ForeignKey(bookCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='upload/book_images/', blank= True, null= True)
    book_quantity=models.IntegerField()
    borrow_book_quantity = models.IntegerField(default=0)
    borrow_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'{self.book_name}'
    

class BorrowModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE,null=True, blank=True)
    status=models.BooleanField(default=False)
    borrow_date = models.DateField(auto_now=True)
    # balance_after_transaction = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.book} borrowed by {self.user}'
    
class ReturnModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE,null=True, blank=True)
    status=models.BooleanField(default=False)
    return_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.book} returned by {self.user}'

class CommentModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='comment')
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, )
    comment_body = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comments by {self.name}'
