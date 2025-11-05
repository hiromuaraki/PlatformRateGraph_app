from django.db import models

# Create your models here.
class BaseModel(models.Model):
     """全モデルで共通して使用する基本クラス"""
     created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時") # 登録日時 登録時に一度だけ設定
     updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時") # 更新日時 

     class Meta:
        abstract = True  # 継承専用モデル（DBテーブルを作らない）


# 以下に各テーブルを定義
class PlatForms(BaseModel):
    """配信プラットフォーム"""
    name = models.CharField(max_length=100, unique=True, verbose_name="配信プラットフォーム名", null=False)
    url = models.URLField(verbose_name="公式URL", null=False)
    
    class Meta:
        db_table = "platforms"
        verbose_name = "配信プラットフォーム"
        verbose_name_plural = "配信プラットフォーム一覧"
    

    def __str__(self):
        return self.name

class Staffs(BaseModel):
    """制作会社情報"""
    organization_name = models.CharField(max_length=100, unique=True, verbose_name="制作会社", null=False) 

    class Meta:
        db_table = "staffs" # dbを固定
        # 管理画面で表示
        verbose_name = "制作会社" # される単数形
        verbose_name_plural = "制作会社一覧" # 複数形

    def __str__(self):
        return self.organization_name


class Works(BaseModel):
    """アニメ作品情報"""
    staff = models.ForeignKey(
        Staffs,
        on_delete=models.CASCADE, # 親が削除された子も削除
        verbose_name="制作会社",
        related_name="works" # Staffs から逆参照できるように
    )
    title = models.CharField(max_length=100, unique=True, verbose_name="アニメタイトル", null=False)
    official_url = models.URLField(verbose_name="公式URL")

    class Meta:
        db_table = "works" # dbを固定
        # 管理画面で表示
        verbose_name = "作品" # 単数形
        verbose_name_plural = "作品一覧" # 複数形

    def __str__(self):
        return self.title


class WorkSeason(BaseModel):
    """作品シーズン情報"""
    season_delivery_cnt = models.IntegerField(verbose_name="シーズン配信件数", blank=False, null=False, default=0)
    year = models.CharField(max_length=4, verbose_name="放送年", null=False)
    season = models.CharField(max_length=2, verbose_name="シーズン", null=False) # ex: '春', '夏', '秋', '冬'
    
    class Meta:
        db_table = "work_season" # dbを固定
        # 管理画面で表示
        verbose_name = "作品シーズン" # 単数形
        verbose_name_plural = "作品シーズン一覧" # 複数形
        unique_together = ("year", "season") # 同一作品・年・シーズンの重複防止


class PlatformInfo(BaseModel):
    """配信情報一覧"""
    platform = models.ForeignKey(
        PlatForms,
        on_delete=models.CASCADE, # 親が削除された子も削除
        verbose_name="配信プラットフォーム",
        related_name="platform_infos"
    )
    work_season = models.ForeignKey(
        WorkSeason,
        on_delete=models.CASCADE, # 親が削除された子も削除
        verbose_name="作品シーズン",
        related_name="platform_infos"
    )
    delivery_start = models.DateField(verbose_name="配信開始日", null=True)
    delivery_end = models.DateField(verbose_name="配信終了日", null=True)
    delivery_count = models.IntegerField(verbose_name="配信件数", default=0)
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")

    class Meta:
        db_table = "platform_info" # dbを固定
        # 管理画面で表示
        verbose_name = "配信情報" # 単数形
        verbose_name_plural = "配信情報一覧" # 複数形
        unique_together = ("platform", "work_season")