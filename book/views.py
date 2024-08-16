from django.views import View
from django.shortcuts import render,redirect, get_object_or_404
from .models import BookModel, CommentModel, BorrowModel, ReturnModel
from librarians.models import UserProfile
from .forms import CommentForm
from django.views.generic import DetailView
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
    
class bookDetailsView(DetailView):
    model = BookModel
    template_name = "book_details.html"
    pk_url_kwarg = "pk"
    context_object_name = "book_details"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        requested_book = self.get_object()
        print(requested_book)
        if comment_form.is_valid():
            print("inside")
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.book = requested_book
            comment.save()
            print(comment)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        if self.request.user.is_authenticated:
            user = self.request.user
            flag = BorrowModel.objects.filter(
                user=user,
                book=book,
                status=True,
            ).exists()
            context["flag"] = flag
        comments = book.comment.all()
        context["comments"] = comments
        context["CommentForm"] = CommentForm()
        return context




# class DetailsBookView(DetailView):
#     model = BookModel
#     template_name = 'book_details.html'
#     pk_url_kwarg = 'id'
    
#     def post(self,request, *args, **kwargs):
#         comment_form = CommentForm(data=self.request.POST)
#         book = self.get_object()
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.user = request.user
#             new_comment.book = book
#             new_comment.save()
#             messages.success(request, "This comment has been saved successfully")
#         return self.get(request, *args, **kwargs)
        
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         book = self.object # book model er object ekhanre store korlam
#         comments = book.comments.all()
#         comment_form = CommentForm()
#         filter_result = BorrowModel.objects.filter(book_id=book.id, user_id=self.request.user.id)
#         # print(filter_result)
#         context['comments'] = comments
#         context['comment_form'] = comment_form
#         return context
    
    
def sendOrderemail(user, amount, book, subject):
    message = render_to_string(
        "borrow_email.html",
        {
            "user": user,
            "book": book,
            "amount": amount,
            "operation": subject,
        },
    )
    send_email = EmailMultiAlternatives(subject=subject, body="", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
    
def sendReturnemail(user, amount, book, subject):
    message = render_to_string(
        "return_email.html",
        {
            "user": user,
            "book": book,
            "amount": amount,
            "operation": subject,
        },
    )
    send_email = EmailMultiAlternatives(subject=subject, body="", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


# class BookBorrowView(View):
#     def post(self, request, *args, **kwargs):
#         book_id = kwargs.get('id')
#         requested_book = get_object_or_404(BookModel, id=book_id)
        
#         if requested_book.book_quantity <= 0:
#             messages.error(request, "Sorry, Out Of Stock!")
#             return redirect('book_details', id=book_id)
        
#         requested_book.book_quantity -= 1
#         requested_book.save() 

#         requested_user = get_object_or_404(UserProfile, id=request.user.id)
#         if requested_user.balance < requested_book.borrow_price:
#             messages.error(request, "You don't have enough balance to borrow this book.")
#             return redirect('book_details', id=book_id)
        
#         requested_user.balance -= requested_book.borrow_price
#         requested_user.save()
        
        

#         borrow_object = BorrowModel.objects.create(
#             user=request.user,
#             book=requested_book,
#             status=True,
#         )
#         borrow_object.save()
#         messages.success(request, f"You've successfully borrowed '{requested_book.book_name}'.")
#         return redirect('book_details', id=book_id)

def BookBorrowView(request, id):
    print(id)
    requested_book = BookModel.objects.get(id=id)
    print(requested_book)
    requested_user = UserProfile.objects.get(user=request.user)
    if requested_user.balance > requested_book.borrow_price:
        if  requested_book.book_quantity >= 0:
            requested_book.book_quantity -= 1
            requested_book.borrow_book_quantity += 1 
            requested_book.save()
            requested_user.balance -= requested_book.borrow_price
            sendOrderemail(
                request.user, requested_book.borrow_price, requested_book.book_name, "Borrow"
            )
            requested_user.save()
            borrow_object = BorrowModel.objects.create(
                user=request.user,
                book=requested_book,
                status=True,
            )
            borrow_object.save()
        else:
            messages.error(request, "Sorry, Out Of Stock!")
        return redirect('book_details', pk=id)
    else:
        messages.error(request, "You don't have enough balance to borrow this book.")
    return redirect('book_details', pk=id)

    # if requested_user.balance < requested_book.borrow_price:
    #         messages.error(request, "You don't have enough balance to borrow this book.")
    #         return redirect('book_details', pk=id)
    # if requested_book.book_quantity <= 0:
    #         messages.error(request, "Sorry, Out Of Stock!")
            #return redirect('book_details', pk=id)
    

def BookReturnView(request, id):
    if request.method=="POST":
        book_id = id
        print(book_id)
        requested_book = get_object_or_404(BookModel, id=book_id)
        requested_book.book_quantity += 1
        requested_book.borrow_book_quantity -= 1
        requested_book.save()
        
        requested_user = get_object_or_404(UserProfile, user=request.user)
        requested_user.balance += requested_book.borrow_price
        requested_user.save()
        
        sendReturnemail(
            request.user, requested_book.borrow_price, requested_book.book_name, "Return"
        )
        
        return_object = ReturnModel.objects.create(
            user=request.user,
            book=requested_book,
            status=True,
        )
        borrow_status = BorrowModel.objects.filter(book=requested_book, user=request.user).first()
        borrow_status.delete()
        borrow_status.save()
        return_object.save()
        messages.success(request, f'You have successfully returned "{requested_book.book_name}".')
        return redirect("book_details", pk=id)
