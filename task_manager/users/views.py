from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class CreateUserView(CreateView):
    template_name = 'users/create.html'
    form_class = UserCreationForm

class UserListView(ListView):
    pass