# intake_info/forms.py
from django import forms

class IntakeInfoForm(forms.Form):
    """サーバーサイド側の検証チェッククラス"""
    season_delivery_cnt = forms.IntegerField(
        required=True, # 未入力チェック
        widget=forms.NumberInput(attrs={
            'placeholder': '配信件数を入力',
            'id': 'season_delivery_cnt',
        })
    )

    csv_file = forms.FileField(
        label='CSVファイルを選択',
        required=True, # 未入力チェック
        widget=forms.ClearableFileInput(attrs={
            'id': 'csv-file',
            'accept': '.csv',
            'class': 'file-input'
        })
    )
