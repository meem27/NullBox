from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# Create your models here.


class Post(models.Model):
	body = models.TextField()
	image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
	created_at = models.DateTimeField(default=datetime.datetime.now())
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
	tags = models.ManyToManyField('Tag', blank=True)

	def create_tags(self):
		for word in self.body.split():
			if (word[0] == '#'):
				tag = Tag.objects.filter(name=word[1:]).first()
				if tag:
					self.tags.add(tag.pk)
				else:
					tag = Tag(name=word[1:])
					tag.save()
					self.tags.add(tag.pk)
				self.save()


	class Meta:
		ordering = ['-created_at']



class Comment(models.Model):
	comment = models.TextField()
	created_at = models.DateTimeField(default=datetime.datetime.now())
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	tags = models.ManyToManyField('Tag', blank=True)

	def create_tags(self):
 		for word in self.comment.split():
 			if (word[0] == '#'):
 				tag = Tag.objects.get(name=word[1:])
 				if tag:
 					self.tags.add(tag.pk)
 				else:
 					tag = Tag(name=word[1:])
 					tag.save()
 					self.tags.add(tag.pk)
 				self.save()

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=30, blank=True, null=True)
	bio = models.TextField(max_length=500, blank=True, null=True)
	birth_date=models.DateField(null=True, blank=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.jpg', blank=True)
	followers = models.ManyToManyField(User, blank=True, related_name='followers')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class Notification(models.Model):
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	user_has_seen = models.BooleanField(default=False)

class Tag(models.Model):
	name = models.CharField(max_length=255)