from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,userName,email,password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        if not userName:
            raise ValueError("User must have an username")

        user =self.model(
            email = self.normalize_email(email),
            userName = userName,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,userName,email,password=None):
        user=self.create_user(first_name=first_name,
                              last_name=last_name,
                              userName=userName,
                              email=self.normalize_email(email),password=password)
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)

        return user     

class User(AbstractUser):
    RESTURANT=1
    CUSTOMER=2
    ROLE_CHOICE=(
        (RESTURANT, "Resturant"),
        (CUSTOMER,"Customer"),
    )
    first_name =models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    userName = models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=12,blank=True)
    role =models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    # required fields
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    modified_date=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS=["userName","first_name","last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm, obj =None):
        return self. is_admin
    
    def has_module_perms(self,app_label):
        return True

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture=models.ImageField(upload_to="users/profile_pictures",blank=True,null=True)
    cover_photo=models.ImageField(upload_to="users/cover_photos",blank=True,null=True)
    address_line_1=models.CharField(max_length=100,blank=True,null=True)
    address_line_2=models.CharField(max_length=100,blank=True, null=True)
    country=models.CharField(max_length=20,blank=True,null=True)
    state=models.CharField(max_length=20,blank=True,null=True)
    city=models.CharField(max_length=20,blank=True,null=True)
    pin_code=models.CharField(max_length=6,blank=True,null=True)
    latitude=models.FloatField(blank=True,null=True)
    longitude=models.FloatField(blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email
