from datetime import datetime

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

def new_years(year: int, month: int) -> tuple:
    """年をまたぐかを判定し3か月後の年・月を設定し返す."""
    if month < 10:
        month += 3
    else:
        year += 1
        month = (month + 3) % 12
    return year, month


