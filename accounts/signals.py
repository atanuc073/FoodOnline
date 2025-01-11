
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile
    
# receiver function
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender, instance,created,**kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile is created")

    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #Create Profile if not Exists
            UserProfile.objects.create(user=instance)
            print("User profile was not exists, Now Created")
        print("User Profile is Updated")


@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender,instance,**kwargs):
    print("Pre Save")
    print(instance)
    print(sender)


# If we dont use the decorator we have to write the below code
# post_save.connect(post_save_create_profile_receiver,sender=User)
