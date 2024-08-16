from django.urls import path
from .views import bookDetailsView,BookBorrowView,BookReturnView

urlpatterns = [
    path('book_details/<int:pk>/',bookDetailsView.as_view(),name='book_details'),
    path('borrow/<int:id>/',BookBorrowView,name='book_borrow'),
    path("return/<int:id>/",BookReturnView,name='return'),
]