from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
# Create your views here.
def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	#context = {'boldmessage':"I am rango"}
	context = {'categories': category_list}
	return render(request, 'rango/index.html', context)
	#return HttpResponse("Rango says hello world<br/ <a href='rango/about'>About</a>")
def about(request):
	return HttpResponse("hELLO i am rango")

def category(request, category_name_slug):
	context = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		context['category_name'] = category.name 
		pages = Page.objects.filter(category=category)

		context['pages'] = pages
		context['category'] = category
		context['category_name_url'] = category_name_slug
	except Category.DoesNotExist:

		pass

	return render(request, 'rango/category.html', context)

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print form.errors
	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form':form} )

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)