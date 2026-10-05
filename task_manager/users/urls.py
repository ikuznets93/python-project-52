from django.urls import path
from task_manager.users.views import CreateUserView, UserListView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete')
]