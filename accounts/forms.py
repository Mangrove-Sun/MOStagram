from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['email'].required = True
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True
    
  class Meta(UserCreationForm.Meta):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']

  # 중복 이메일 막기
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if email:
      qs = User.objects.filter(email = email)
      if qs.exists():
        raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
    return email
        
  # 중복 사용자이름 막기 ** clean_필드명 으로 해야 적용됨 **
  # def clean_username(self):
  #   username = self.cleaned_data.get('username')
  #   if username:
  #     qs = User.objects.filter(username = username)
  #     if qs.exists():
  #       raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
  #   return username
        
class ProfileForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['avatar', 'first_name', 'last_name', 'website_url', 'bio', 'phone_number', 'gender']