from django import forms
class RegisterForm(forms.Form):
	 username = forms.CharField(label='UserName(*) ',max_length=100)
	 password = forms.CharField(label='PassWord(*) ',widget=forms.PasswordInput())
	 fullname = forms.CharField(label='Full Name(*) ',max_length=200)
	 email = forms.EmailField(label='Email(*) ',max_length=100)
	 #companyname = forms.CharField(label='Company Name :',max_length=200)
	 #country = forms.CharField(label='Country :',max_length=200)
	 #address = forms.CharField(label='Address :',max_length=200)
	 #city = forms.CharField(label='City :',max_length=200)
	 
	 #phonenumber = forms.CharField(label='Phonenumber:',max_length=50)

