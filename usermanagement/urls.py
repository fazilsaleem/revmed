from django.urls import path
from usermanagement.views import (
    DashboardView, CreateStaffView, StaffListView, UserProfileView

)

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('create-staff/', CreateStaffView.as_view(), name="create-staff"),
    path('staff-users/', StaffListView.as_view(), name="staff-users"),
    path('user-profile/<int:pk>', UserProfileView.as_view(), name="user-profile"),

]