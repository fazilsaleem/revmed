from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import generic
from usermanagement.models import UserProfile
from utils.messages import UserMessages
from usermanagement.forms import UserProfileForm
from django.contrib import messages 
from utils.utilities import id_generator
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from _functools import reduce
import operator
from django.views.generic.detail import DetailView

# Create your views here.

class DashboardView(TemplateView):
    template_name = "usermanagement/dashboard.html"

class StaffListView(generic.ListView):
    template_name = "usermanagement/staff-list.html"
    model = UserProfile
    ordering = '-id'
    context_object_name = 'staff_list'
    paginated_by = 20
    msg_obj = UserMessages()

    def get_queryset(self):
        search_query = self.request.GET.get('search_key', '')
        filter_items = [Q(is_active=True, is_staff=True)]
        if search_query:
            filter_items.append(Q(Q(first_name__icontains=search_query)) | 
                                Q(Q(last_name__icontains=search_query))  |
                                Q(Q(email__icontains=search_query)) 
                                )
        staff_list = self.model.objects.filter(reduce(operator.and_, filter_items))
        print(f'staff list' , staff_list)
        return staff_list




class CreateStaffView(generic.FormView):
    template_name = 'usermanagement/create-staff.html'
    model = UserProfile
    message = UserMessages()
    form_class = UserProfileForm
    success_url = 'staff-users'

    def get_context_data(self,**kwargs):
        context_data = generic.FormView.get_context_data(self, **kwargs)
        if 'form' in kwargs:
            context_data['form'] = self.form_class
        print(context_data)
        return context_data

    def form_invalid(self, staff_form):
        kwargs = {}
        kwargs['form'] = staff_form
        return render(self.request, self.template_name, {"form":staff_form})

    def form_valid(self, staff_form):
        email = staff_form.cleaned_data['email']
        phone_number = staff_form.cleaned_data['phone_number']
        if UserProfile.objects.filter(email=email).exists():
            kwargs = {}
            kwargs['form'] = staff_form
            print(staff_form)
            messages.error(self.request, self.message.email_already_exist)
            return render(self.request, self.template_name, {"form":staff_form})
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            kwargs = {}
            kwargs['form'] = staff_form
            messages.error(self.request, self.message.phone_already_exist)
            return render(self.request, self.template_name,  {"form":staff_form})

        profile_obj = staff_form.save(commit=False)
        user_uid = id_generator()
        while User.objects.filter(username=user_uid).exists():
            user_uid = id_generator()
        user_ob = User.objects._create_user(user_uid, email, id_generator())
        profile_obj.user = user_ob
        profile_obj.is_active = True  
        profile_obj.is_staff = True  
        profile_obj.save()
        messages.success(self.request, self.message.staff_user_creation_success)
        #Todo Send email here...
        return redirect(self.success_url)


class UserProfileView(DetailView):
    template_name = 'usermanagement/user-profile.html'
    model = UserProfile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



