from django.db import models


class Timestamp(models.Model):
    created_at = models.DateTimeField("생성 일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정 일자", auto_now=True)
    deleted_at = models.DateTimeField("삭제 일자", null=True)

    class Meta:
        abstract = True
