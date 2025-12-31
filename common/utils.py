from datetime import datetime, date

def get_sysdate() -> list:
    """現在の年月日を取得"""
    date = datetime.now()
    return [date.year, date.month, date.day]


def get_season(month: int) -> str:
    """
    月（1〜12)に応じて季節を判定して返す.
    """
    if month in (4, 5, 6): return "春"
    elif month in (7, 8, 9): return "夏"
    elif month in (10, 11 ,12): return "秋"
    else: return "冬"

def get_current_batch_key(today: date) -> str:
    """バッチキーを動的に作成"""
    year = today.year
    quarter = (today.month - 1) // 3 + 1
    return f"{year}Q{quarter}"


