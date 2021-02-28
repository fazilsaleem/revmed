from django.urls import path
from website.views import (
    LandingPageView,

)

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing-page"),

]