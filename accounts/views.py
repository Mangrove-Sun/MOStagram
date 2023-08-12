from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, logout_then_login
from django.shortcuts import redirect, render
from .forms import SignupForm


login = LoginView.as_view(template_name = 'accounts/login_form.html')

def logout(request):
  messages.success(request, '로그아웃되었습니다.')
  return logout_then_login(request)

def signup(request):
  if request.method == "POST":
    form = SignupForm(request.POST)
    if form.is_valid():
      signed_user = form.save()
      auth_login(request, signed_user) # 회원가입 후 바로 로그인되는 기능 login as auth_login
      messages.success(request, "회원가입 환영합니다.")
      signed_user.send_welcome_email() # FIXME: Celey로 처리하는 것을 추천.
      # request에서 GET인자에서 'next'가 없으면 '/'로 설정을 하겠다.
      next_url = request.GET.get('next', '/')
      return redirect(next_url)
  else:
    form = SignupForm()
  return render(request, "accounts/signup_form.html", {
    'form': form,
  })
  