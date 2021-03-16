from django.db import models
from django.contrib.auth.models import User

class CommonInfo(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class MenuMaster(CommonInfo):
    menu_name = models.CharField(max_length = 100)
    menu_url = models.CharField(max_length = 200)
    is_active = models.BooleanField(default=True)
    is_submneu = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    parent_menu = models.ForeignKey("usermanagement.MenuMaster",  on_delete=models.SET_NULL, null=True, blank=True)
    menu_icon = models.CharField(max_length = 100, blank=True, null=True)

    def __str__(self):
        return self.menu_name

class UserRole(models.Model):
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  
    menu = models.ManyToManyField(MenuMaster, blank=True, related_name='access_role')
    staff_role = models.BooleanField(default=False)
    user_level = models.BooleanField(default=True)

    def __str__(self):
        return self.role 

class Organization(CommonInfo):
    name = models.CharField(max_length=200)
    address  = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    email =models.CharField(max_length=200,null=True, blank=True)
    phone_number =models.CharField(max_length=200,null=True, blank=True)
    country_code=models.CharField(max_length=20, default="+1",null=True,blank=True)
    logo = models.ImageField(upload_to = "org_logo", null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(CommonInfo):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    first_name = models.CharField( max_length=50,null=True, blank=True)
    last_name = models.CharField( max_length=50,null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone_number=models.CharField(max_length=20)
    country_code=models.CharField(max_length=20, default="+1",null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    organization = models.ForeignKey(Organization,on_delete = models.SET_NULL, null=True, blank=True, related_name='user_organization')
    Address=models.TextField(null=True, blank=True)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    email_verified=models.BooleanField(default=False)
    phone_verified=models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to = "profile_images", null=True, blank=True)
    user_role = models.ForeignKey(UserRole, related_name= "user_role", null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email
