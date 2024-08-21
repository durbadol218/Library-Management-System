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
        user = request.user
        
        if not BorrowModel.objects.filter(user=user, book=requested_book, status=True).exists():
            messages.error(request, "You can review it if you must have borrowed this book before")
            return self.get(request, *args, **kwargs)

        if comment_form.is_valid():
            print("inside")
            try:
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.book = requested_book
                comment.save()
                messages.success(request, "Your review has been submitted successfully.")
            except IntegrityError:
                messages.error(request, "There was an error submitting your review. Please try again.")
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


def BookReturnView(request, id):
    if request.method == "POST":
        book_id = id
        print(book_id)

        requested_book = get_object_or_404(BookModel, id=book_id)
        requested_user_profile = get_object_or_404(UserProfile, user=request.user)
        
        borrow_record = BorrowModel.objects.filter(user=request.user, book=requested_book, status=True).first()
        
        if borrow_record:
            requested_book.book_quantity += 1
            requested_book.borrow_book_quantity -= 1
            requested_book.save()
            
            requested_user_profile.balance += requested_book.borrow_price
            requested_user_profile.save()
            
            borrow_record.delete()
            
            ReturnModel.objects.create(
                user=request.user,
                book=requested_book,
                status=True,
            )
            
            sendReturnemail(
                request.user, requested_book.borrow_price, requested_book.book_name, "Return"
            )
            messages.success(request, f'You have successfully returned "{requested_book.book_name}".')
        else:
            messages.error(request, "You haven't borrowed this book, so you cannot return it.")
        return redirect("book_details", pk=id)
