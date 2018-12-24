from django import forms
from .models import Paper, Admin
from .search_func import get_num

class paperForm(forms.ModelForm):
    paper_id, court_id = get_num()
    paper_id += 1
    id = forms.IntegerField(
        widget=forms.Textarea(
            attrs={'rows':1, 'cols':4, 'placeholder':paper_id}
        )   
    )
    title = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '文书标题'}
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 8, 'cols':70,'placeholder': '文书内容'}
        ),
    )

    time = forms.DateField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': "输入格式：'2018-12-23'"}
        ),
    )

    case_type = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '案件类型'}
        )
    )
    title = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '文书标题'}
        )
    )
    plaintiff = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '原告'}
        )
    )
    defendant = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '被告'}
        )
    )
    term = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '审理程序'}
        )
    )
    paper_type = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols':30, 'placeholder': '文书类型'}
        )
    )
    class Meta:
        model = Paper
        fields = ('id','title','time','court','case_type',
        'plaintiff', 'defendant', 'term', 'paper_type', 'content')


class loginForm(forms.ModelForm):

    class Meta:
        model = Admin
        fields = ('username','password',)
