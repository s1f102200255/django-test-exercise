from django.db import models
from django.utils import timezone

# 論理削除のモデルマネージャー
class SoftDeletionManager(models.Manager):
    # 論理削除されていない(deleted_atがNone)クエリの取得
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

# カテゴリーモデル
class Category(models.Model):
    name = models.CharField(verbose_name="カテゴリ", max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  null=True, blank=True) # カテゴリーキー(外部キー)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True) # 削除日時の追加
    detail = models.CharField(max_length=1000, default="")

    objects = SoftDeletionManager() # 使うマネージャー

    # 論理削除メソッドの定義
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now() # Noneでなくなる
        self.save()


    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
