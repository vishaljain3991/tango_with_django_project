from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query

# Create your views here.
def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response
def about(request):
	return render(request, 'rango/about.html', {})

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

# def register(request):
# 	registered =  False
# 	# if request.session.test_cookie_worked():
# 	# 	print ">>>> TEST COOKIE WORKED!"
# 	# 	request.session.delete_test_cookie()
    
# 	if request.method == 'POST':
# 		user_form = UserForm(data=request.POST)
# 		profile_form = UserProfileForm(data=request.POST)

# 		if user_form.is_valid() and profile_form.is_valid():
# 			user = user_form.save()
# 			#hasing password
# 			user.set_password(user.password)
# 			user.save()

# 			profile = profile_form.save(commit=False)
# 			profile.user = user

# 			if 'picture' in request.FILES:
# 				profile.picture = request.FILES['picture']

# 			profile.save()
# 			registered = True

# 		else:
# 			print user_form.errors, profile_form.errors

# 	else:
# 		user_form = UserForm()
# 		profile_form = UserProfileForm()

# 	return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# def user_login(request):
# 	if request.method == 'POST':
# 		username = request.POST['username']
# 		password = request.POST['password']

# 		user = authenticate(username=username, password=password)

# 		if user:
# 			if user.is_active:
# 				login(request, user)
# 				return HttpResponseRedirect('/rango/')
# 			else:
# 				return HttpResponse("Your rango account is disabled")

# 		else:
# 			print "Invalid login details: {0}, {1}" . format(username, password)
# 			return HttpResponse("Invalid login details supplied.")

# 	else:
# 		return render(request, 'rango/login.html', {})

# @login_required
# def restricted(request):
# 	return HttpResponse("Since you're logged in, you can see this")

# @login_required
# # def user_logout(request):
# # 	logout(request)
# # 	return HttpResponseRedirect('/rango/')

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})




@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)