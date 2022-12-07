from django.db import models
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)

    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add= True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.title


from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver




# from chat.utils import find_or_create_private_chat
# from notification.models import Notification



from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

# def get_default_profile_image():
# 	return "codingwithmitch/logo_1080_1080.png"


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	# profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email				= models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# def get_profile_image_filename(self):
	# 	return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


class FriendList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends") 

	# set up the reverse relation to GenericForeignKey
	# notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add a new friend.
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			self.save()

			content_type = ContentType.objects.get_for_model(self)

			# Create notification
			# Can create this way if you want. Doesn't matter.
			# Notification(
			# 	target=self.user,
			# 	from_user=account,
			# 	redirect_url=f"{settings.BASE_URL}/account/{account.pk}/",
			# 	verb=f"You are now friends with {account.username}.",
			# 	content_type=content_type,
			# 	object_id=self.id,
			# ).save()

			self.notifications.create(
				target=self.user,
				from_user=account,
				redirect_url=f"{settings.BASE_URL}/account/{account.pk}/",
				verb=f"You are now friends with {account.username}.",
				content_type=content_type,
			)
			self.save()

			# Create a private chat (or activate an old one)
			chat = find_or_create_private_chat(self.user, account)
			if not chat.is_active:
				chat.is_active = True
				chat.save()

	def remove_friend(self, account):
		"""
		Remove a friend.
		"""
		if account in self.friends.all():
			self.friends.remove(account)

			# Deactivate the private chat between these two users
			chat = find_or_create_private_chat(self.user, account)
			if chat.is_active:
				chat.is_active = False
				chat.save()

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		remover_friends_list = self # person terminating the friendship

		# Remove friend from remover friend list
		remover_friends_list.remove_friend(removee)

		# Remove friend from removee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(remover_friends_list.user)

		content_type = ContentType.objects.get_for_model(self)

		# Create notification for removee
		friends_list.notifications.create(
			target=removee,
			from_user=self.user,
			redirect_url=f"{settings.BASE_URL}/account/{self.user.pk}/",
			verb=f"You are no longer friends with {self.user.username}.",
			content_type=content_type,
		)

		# Create notification for remover
		self.notifications.create(
			target=self.user,
			from_user=removee,
			redirect_url=f"{settings.BASE_URL}/account/{removee.pk}/",
			verb=f"You are no longer friends with {removee.username}.",
			content_type=content_type,
		)

	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FriendList"

	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		return False



class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
	receiver 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

	is_active			= models.BooleanField(blank=False, null=False, default=True)

	timestamp 			= models.DateTimeField(auto_now_add=True)

	# notifications		= GenericRelation(Notification)

	def __str__(self):
		return self.sender.username

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			content_type = ContentType.objects.get_for_model(self)

			# Update notification for RECEIVER
			receiver_notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
			receiver_notification.is_active = False
			receiver_notification.redirect_url = f"{settings.BASE_URL}/account/{self.sender.pk}/"
			receiver_notification.verb = f"You accepted {self.sender.username}'s friend request."
			receiver_notification.timestamp = timezone.now()
			receiver_notification.save()
			receiver_friend_list.add_friend(self.sender)

			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:

				# Create notification for SENDER
				self.notifications.create(
					target=self.sender,
					from_user=self.receiver,
					redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
					verb=f"{self.receiver.username} accepted your friend request.",
					content_type=content_type,
				)

				sender_friend_list.add_friend(self.receiver)
				# sender_friend_list.save()
				self.is_active = False
				self.save()
			return receiver_notification # we will need this later to update the realtime notifications


	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()

		content_type = ContentType.objects.get_for_model(self)

		# Update notification for RECEIVER
		notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
		notification.is_active = False
		notification.redirect_url = f"{settings.BASE_URL}/account/{self.sender.pk}/"
		notification.verb = f"You declined {self.sender}'s friend request."
		notification.from_user = self.sender
		notification.timestamp = timezone.now()
		notification.save()

		# Create notification for SENDER
		self.notifications.create(
			target=self.sender,
			verb=f"{self.receiver.username} declined your friend request.",
			from_user=self.receiver,
			redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
			content_type=content_type,
		)

		return notification


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()

		content_type = ContentType.objects.get_for_model(self)

		# Create notification for SENDER
		self.notifications.create(
			target=self.sender,
			verb=f"You cancelled the friend request to {self.receiver.username}.",
			from_user=self.receiver,
			redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
			content_type=content_type,
		)

		notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
		notification.verb = f"{self.sender.username} cancelled the friend request sent to you."
		#notification.timestamp = timezone.now()
		notification.read = False
		notification.save()

	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FriendRequest"


@receiver(post_save, sender=FriendRequest)
def create_notification(sender, instance, created, **kwargs):
	if created:
		instance.notifications.create(
			target=instance.receiver,
			from_user=instance.sender,
			redirect_url=f"{settings.BASE_URL}/account/{instance.sender.pk}/",
			verb=f"{instance.sender.username} sent you a friend request.",
			content_type=instance,
		)




