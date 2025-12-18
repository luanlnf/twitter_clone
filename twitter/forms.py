from django import forms
from .models import Tweet, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Profile Extras Form
class ProfilePicForm(forms.ModelForm):
	profile_image = forms.ImageField(label="Profile Picture")
	
	profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
	homepage_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
	facebook_link =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
	instagram_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
	linkedin_link =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Linkedin Link'}))

	class Meta:
		model = Profile
		fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link',)

class TweetForm(forms.ModelForm):
	body = forms.CharField(required=True, 
		widget=forms.widgets.Textarea(
			attrs={
			"placeholder": "Escreva o que estiver em sua mente hoje!",
			"class":"form-control",
			}
			),
			label="",
		)

	class Meta:
		model = Tweet
		exclude = ("user", "likes",)

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Tweet your reply'
        })
    )

    class Meta:
        model = Comment
        fields = ('body',)


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primeiro Nome'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ultimo Nome'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Obrigatório. 150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Sua senha não pode ser muito semelhante às suas outras informações pessoais.</li><li>Sua senha deve conter pelo menos 8 caracteres.</li><li>Sua senha não pode ser uma senha de uso comum.</li><li>Sua senha não pode ser inteiramente numérica.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Digite a mesma senha de antes para verificação.</small></span>'

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        label="Primeiro Nome",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro Nome'})
    )
    last_name = forms.CharField(
        label="Ultimo Nome",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ultimo Nome'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
		
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image',
            'profile_bio',
            'homepage_link',
            'facebook_link',
            'instagram_link',
            'linkedin_link'
        ]