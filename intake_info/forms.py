from django import forms

class IntakeInfo(forms.Form):
    csv_file = forms.FileField(label="CSVファイル", required=True)
    delivery_cnt = forms.IntegerField(
    label='配信件数',
    widget=forms.NumberInput(attrs={'placeholder': '配信件数を入力'})
)
