from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .forms import PostForm
from .models import Post


# 타임라인
@login_required
def index(request):
  timesince = timezone.now() - timedelta(days = 3)
  post_list = Post.objects.all().filter(Q(author = request.user) | Q(author__in = request.user.following_set.all())).filter(created_at__gte = timesince)
  suggested_user_list = get_user_model().objects.all().exclude(pk = request.user.pk).exclude(pk__in = request.user.following_set.all())[:3] # 처음 3명만
  
  return render(request, "instagram/index.html", {
    "post_list": post_list,
    "suggested_user_list": suggested_user_list,
  })

@login_required
def post_new(request):
  if request.method == "POST":
    form = PostForm (request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit = False)
      post.author = request.user
      post.save() # MTM방식이라 저장이 된 후에 
      post.tag_set.add(*post.extract_tag_list())
      messages .success(request, "포스트를 저장했습니다.")
      return redirect(post) # TODO: get_absolute_url 활용
  else:
    form = PostForm()
  return render(request, "instagram/post_form.html", {
    'form': form,
  })
  
def post_detail(request, pk):
  post = get_object_or_404(Post, pk = pk)
  return render(request, "instagram/post_detail.html", {
    "post": post
  })
  
@login_required
def post_like(request, pk):
  post = get_object_or_404(Post, pk = pk)
  post.like_user_set.add(request.user)
  messages.success(request, f"{post}를 좋아합니다.")
  redirect_url = request.META.get("HTTP_REFERER", "root")
  return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
  post = get_object_or_404(Post, pk = pk)
  post.like_user_set.remove(request.user)
  messages.success(request, f"{post}를 좋아요를 취소합니다.")
  redirect_url = request.META.get("HTTP_REFERER", "root")
  return redirect(redirect_url)
  
def user_page(request, username):
  page_user = get_object_or_404(get_user_model(), username = username, is_active = True)
  post_list = Post.objects.filter(author = page_user)
  post_list_count = post_list.count() # 실제 데이터베이스에 count 쿼리를 던지게 된다. post개수가 많아지게 되면 속도에서 차이가 날 수 있다.
  # len(post_list)  # post_list를 전체를 다 가져와서 메모리에 얹어서 메모리상의 리스트 개수를 반환
  
  if request.user.is_authenticated:
    is_follow = request.user.following_set.filter(pk = page_user.pk).exists() # login되어있으면 User객체, 안 되어있으면 AnonymousUser
  else:
    is_follow = False
  return render(request, "instagram/user_page.html", {
    "page_user": page_user,
    "post_list": post_list,
    "post_list_count": post_list_count,
    "is_follow": is_follow,
    })