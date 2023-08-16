from django.conf import settings
import re
from django.db import models


class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) # 외래키이기 때문에 on_delete-models.CASCADE 적용
  photo = models.ImageField(upload_to = "instagram/post/%Y/%m/%d")
  caption = models.TextField(max_length = 500)
  tag_set = models.ManyToManyField("Tag", blank = True)
  location = models.CharField(max_length = 100)
  
  def __str__(self):
    return self.caption
  
  def extract_tag_list(self):
    tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
    tag_list = []
    for tag_name in tag_name_list:
      tag, _ = Tag.objects.get_or_create(name=tag_name)
      tag_list.append(tag)
    return tag_list

  
  # def get_absolute_url(self):
  #     return reverse(" ", kwargs={"pk": self.pk})
  
  
class Tag(models.Model):
  name = models.CharField(max_length = 50, unique = True)
  
  def __str__(self):
    return self.name