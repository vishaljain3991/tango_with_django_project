from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter category_name")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name', )

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter title of page")
	url = forms.URLField(max_length=200, help_text="Please enter the url")
	views = forms. IntegerField(widget=forms.HiddenInput(), initial=0)

	
	class Meta:
		model = Page
		fields = ('title', 'url', 'views')
