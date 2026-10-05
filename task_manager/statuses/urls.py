from django.urls import path
from task_manager.statuses.views import CreateStatusView, StatusListView, UpdateStatusView, DeleteStatusView

urlpatterns = [
    path('', StatusListView.as_view(), name='statuses'),
    path('create/', CreateStatusView.as_view(), name='create_status'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name='update_status'),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name='delete_status')
]