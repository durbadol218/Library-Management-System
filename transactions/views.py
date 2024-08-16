from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TransactionModel
from .forms import DepositForm, WithdrawForm
from .constants import DEPOSIT, WITHDRAWAL
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.views import View
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

def sendTransactionEmail(user, amount, subject,template):
    message = render_to_string(template,{
        'user': user,
        'amount': amount
    })
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'transaction_form.html'
    model = TransactionModel
    title = ''
    success_url = reverse_lazy('transaction_report')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account, 
        })
        return kwargs
    
    #This method is used to populate a dictionary to use as the template context. 
    # You will probably be overriding this method most often to add things to display in your templates.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit' # built-in keyword na
    success_url = reverse_lazy('home')
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    # if form.is_valid(): 
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        
        messages.success(self.request,f"{amount} $ was deposited to your account successfully!")
        
        sendTransactionEmail(self.request.user,amount,"Deposit Message",'deposit_email.html')
        
        return super().form_valid(form)
    
class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money' # built-in keyword na
    
    # Backend theke dekha jabe initially
    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial
    
    # if form.is_valid(): 
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance -= amount
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request,f"{amount} $ was withdrawn from your account successfully!")
        
        sendTransactionEmail(self.request.user,amount,"Withdrawal Message",'withdrawal_email.html')
        
        return super().form_valid(form)