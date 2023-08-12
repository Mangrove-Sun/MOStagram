from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string


class User(AbstractUser):
  class GenderChices(models.TextChoices):
    # "M" DB에 저장되는 값, "남성" 보여지는 값
    MALE = "M", "남성"
    FEMAIL = "F", "여성"
    
  website_url = models.URLField(blank = True)
  bio = models.TextField(blank = True)
  phone_number = models.CharField(max_length=13, blank = True, validators = [RegexValidator(r"^010-?\d{4}-?\d{4}$")])
  gender = models.CharField(max_length = 1, blank = True, choices = GenderChices.choices)  # ,default = GenderChices.MALE) 기본값도 설정 가능 성별은 기본값 설정이 적절하지 않음.
  avatar = models.ImageField(blank = True, upload_to = "accounts/avatar/%Y/%m/%d", help_text = "48px * 48px 크기의 png/jpg 파일을 업로드해주세요.")

  def send_welcome_email(self):
    subject = render_to_string("accounts/welcome_email_subject.txt", {
      "user": self
    })
    content = render_to_string("accounts/welcome_email_content.txt", {
      "user": self
    })
    sender_email = settings.WELCOME_EMAIL_SENDER
    send_mail(subject, content, sender_email, [self.email], fail_silently=False)
    
    
    
# class Profile(models.Model):
#   pass