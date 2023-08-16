from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostForm
from .models import Post


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
  
def user_page(request, username):
  page_user = get_object_or_404(get_user_model(), username = username, is_active = True)
  post_list = Post.objects.filter(author = page_user)
  post_list_count = post_list.count() # 실제 데이터베이스에 count 쿼리를 던지게 된다. post개수가 많아지게 되면 속도에서 차이가 날 수 있다.
  # len(post_list)  # post_list를 전체를 다 가져와서 메모리에 얹어서 메모리상의 리스트 개수를 반환
  return render(request, "instagram/user_page.html", {
    "page_user": page_user,
    "post_list": post_list,
    "post_list_count": post_list_count,
    })