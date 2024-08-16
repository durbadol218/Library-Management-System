from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from .models import UserProfile
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from book.models import BookModel, BorrowModel, ReturnModel
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'userRegistration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request,user)
        print(user)
        return super().form_valid(form) #automatically call korar jonno ai line lekhlam...jodi sobthik thaake tobe automatically kaaj korbe!
    

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('user_login')

class UserProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        
        borrowed_books = BorrowModel.objects.filter(user=user, status=True)
        
        book_return_dates = []    
        context = {
            'user': user,
            'user_profile': user_profile,
            'books': borrowed_books,
        }
        return render(request, self.template_name, context)