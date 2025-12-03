from django.db import connection
import os, django

# Django環境でtruncate.pyを読み込む為の設定
# modelを読み込む前にこの設定しないとプロジェクトのsettings.pyのINSTALLED_APPを見に行きエラーとなる。
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PlatformRateGraph_app.settings")
django.setup()


from common.models import  (
    WorkSeason,
    Staffs,
    Works,
    PlatformInfo
)


def truncate():
    """tableのデータを全て削除するスクリプト（py truncate.pyで削除実行）"""
    # モデルクラス → テーブル名に変換
    table_names = [WorkSeason._meta.db_table,
                   PlatformInfo._meta.db_table,
                   Works._meta.db_table,
                   Staffs._meta.db_table]
    for table_name in table_names:
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table_name};')
            # 次に挿入されるIDが 1から再スタート します
            cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{table_name}";')
        print((f'Table {table_name} truncated successfully.'))


if __name__ == "__main__":
    truncate()