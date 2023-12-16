from django.urls import path
from .views import *

# from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path("taskpage/", taskpage.as_view(), name="add_task"),
    path("taskadd/", taskadd.as_view(), name="add_task"),
    path("", tasklist.as_view(), name="all_tasks"),
    path("taskdetail/<int:id>/", taskdetail.as_view(), name="get_task_by_id"),
    path("taskupdate/<int:id>/", taskupdate.as_view(), name="update_task"),
    path("taskdelete/<int:id>/", taskdelete.as_view(), name="delete_task"),

]
