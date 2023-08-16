from django.contrib import messages
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