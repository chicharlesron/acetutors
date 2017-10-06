from django import forms
from django.contrib.auth.models import User
from .models import Information1, Song, UserProfileInfo


your_course = [
    ('', '--------------------'),
    ('algebra', 'College Algebra'),
    ('integral', 'Integral Calculus'),
    ('diffcal', 'Differential Calculus'),
    ('differential ', 'Differentail Equation'),
    ]


types = [
    ('', '--------------------------------'),
    ('tutor', 'Tutor'),
    ('tutee', 'Tutee')
]


class DetailForm(forms.ModelForm):
    course = forms.CharField(widget=forms.Select(choices=your_course))

    class Meta:
        model = Information1
        fields = ['full_name', 'email', 'course', 'picture_topic', 'tutorial_date', 'tutorial_start', 'tutorial_end']
        widgets = {
            'tutorial_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'id': "tutorial_date"}),
            'tutorial_start': forms.TimeInput(attrs={'placeholder': 'HH:MM', 'id': "tutorial_start"}),
            'tutorial_end': forms.TimeInput(attrs={'placeholder': 'HH:MM', 'id': "tutorial_end"}),
        }


class InfoForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['info_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class UserProfileInfoForm(forms.ModelForm):
    type = forms.CharField(widget=forms.Select(choices=types))

    class Meta:
        model = UserProfileInfo
        fields = ['type', 'contact_number']

















