from django.contrib import admin
from django.urls import path
from task_manager.users.views import CreateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', CreateUserView.as_view(), name='create'),
]