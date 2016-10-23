from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rango.models import Page
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from rango.forms import CategoryForms, PageForm, UserForm, UserProfileForm, ContactForm, UpdateProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from rango.models import UserProfile, Post, Article
from django.utils import timezone
from django.contrib.auth.models import User
#importing templates for email
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
#from rango.bing_search import run_query
#importing the rango categories
from rango.models import Category
from django.contrib import messages
# Create your views here.
def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith=starts_with)
    else:
        cat_list = Category.objects.all()

    if max_results > 0:
        if (len(cat_list) > max_results):
            cat_list = cat_list[:max_results]

    for cat in cat_list:
        cat.url = encode_url(cat.name)

    return cat_list

def category(request, category_name_url):
    #request our context from the request passed to us.
    context = RequestContext(request)

    #Change underscores in the category name to space.
    #URLs don't handle spaces well, so we encode them as underscores.
    #we can then simply replace the underscores with spaces again to get the name.
    category_name = decode_url(category_name_url)

    #Create a context dictionary which we can pass to the template rendering engine.
    #We start by containing the name of category passed by the user.
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url }

    cat_list= get_category_list()
    context_dict['cat_list'] = cat_list

    try:
    # Can we find a category with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
     category = Category.objects.get(name__iexact=category_name)
     context_dict['category'] = category
    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
     pages = Page.objects.filter(category=category).order_by('-views')
    # Adds our results list to the template context under name pages.
     context_dict['pages'] = pages
    # We also add the category object from the database to the context dictionary.
    # We'll use this in the template to verify that the category exists.
     #context_dict['category'] = category

    except Category.DoesNotExist:
    # We get here if we didn't find the specified category.
    # Don't do anything - the template displays the "no category" message for us.
     pass

    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    # Go render the response and return it to the client.
    return render_to_response('rango/category.html', context_dict, context)
def index(request):
# Request the context of the request.
# The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    top_category_list = Category.objects.order_by()[:5]
# Construct a dictionary to pass to the template engine as its context.
# Note the key boldmessage is the same as {{ boldmessage }} in the template!
#    category_list = Category.objects.all()
#    context_dict = {'categories': category_list}
# Return a rendered response to send to the client.
# We make use of the shortcut function to make our lives easier.
# Note that the first parameter is the template we wish to use.
# The following two lines are new.
# We loop through each category returned, and create a URL attribute.
# This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in top_category_list:
      category.url = encode_url(category.name)

    context_dict = {'categories': top_category_list}

    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

 # Get the number of visits to the site.
 # We use the COOKIES.get() function to obtain the visits cookie.
 # If the cookie exists, the value returned is casted to an integer
 # Does the cookie last_visit exist?
    if request.session.get('last_visit'):
        # Yes it does! Get the cookie's value.
        last_visit_time = request.session.get('last_visit')
        #  If the cookie doesn't exist, we default to zero and cast that.
        visits = request.session.get('visits', 0)
        # Cast the value to a Python date/time object.
        #last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # If it's been more than a day since the last visit...
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())

    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    return render_to_response('rango/index.html', context_dict, context)



#def page(request):

#    return HttpResponse("Kadja Says: Here is the about page! <a href='/rango/'>index</a>")
def about(request):
    # Request the context.
    context = RequestContext(request)
    context_dict = {}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.

    count = request.session.get('visits',0)

    context_dict['visit_count'] = count

    # Return and render the response, ensuring the count is passed to the template engine.
    return render_to_response('rango/about.html', context_dict , context)

def add_category(request):
   # Get the context from the request.
   context = RequestContext(request)

   # A HTTP POST?
   if request.method == 'POST':
      form = CategoryForms(request.POST)

      # Have we been provided with a valid form?
      if form.is_valid():
         # Save the new category to the database.
         form.save(commit=True)
         # Now call the index() view.
         # The user will be shown the homepage.
         return index(request)
      else:
          # The supplied form contained errors - just print them to the terminal.
          print (form.errors)
   else:
      # If the request was not a POST, display the form to enter details.
      form = CategoryForms()
   # Bad form (or form details), no form supplied...
   # Render the form with error messages (if any).
   return render_to_response('rango/add_category.html', {'form': form}, context)
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
             page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
             cat = Category.objects.get(name=category_name)
             page.category = cat
            # Also, create a default value for the number of views.
             page.views = 0
            # With this, we can then save our new model instance.
             page.save()
            # Now that the page is saved, display the category instead.
             return category(request, category_name_url)
        else:
           print (form.errors)
    else:
        form = PageForm()
    return render_to_response( 'rango/add_page.html',
          {'category_name_url': category_name_url,
          'category_name': category_name, 'form': form},
           context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
         user_form = UserForm(data=request.POST)
         profile_form = UserProfileForm(data=request.POST)
        # If the two forms are valid...
         if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
           # Now we hash the password with the set_password method.
           # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
           # Now sort out the UserProfile instance.
           # Since we need to set the user attribute ourselves, we set commit=False.
           # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
           # Did the user provide a profile picture?
           # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
               profile.picture = request.FILES['picture']

               profile.save()
           # Update our variable to tell the template registration was successful.
               registered = True

            else:
                 print (user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
                       'rango/register.html',
                       {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                        context)


def user_login(request):
    # Obtain our request's context.
    context = RequestContext(request)
    #cat_list = get_category_list()
    context_dict = {}
    #context_dict['cat_list'] = cat_list

    # If HTTP POST, pull out form data and process it.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to log the user in with the supplied credentials.
        # A User object is returned if correct - None if not.
        user = authenticate(username=username, password=password)

        # A valid user logged in?
        if user is not None:
            messages.error(request, 'Invalid login credentials')
            # Check if the account is active (can be used).
            # If so, log the user in and redirect them to the homepage.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            # The account is inactive; tell by adding variable to the template context.
            else:
                context_dict['disabled_account'] = True
                return render_to_response('rango/login.html', context_dict, context)
        # Invalid login details supplied!
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            context_dict['bad_details'] = True
            return render_to_response('rango/login.html', context_dict, context)

    # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
    else:
        return render_to_response('rango/login.html', context_dict, context)
@login_required
def restricted(requuest):
    return HttpResponse("since you're logged, you can see this information")
 #use the login_required() decorator to ensure only those logged in can access the  view
@login_required
def user_logout(request):
    # since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)


    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('rango/profile.html', context_dict, context)

def get_category_list():
    cat_list = Category.objects.all()

    for cat in cat_list:
        cat.url = encode_url(cat.name)
    return cat_list

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response( 'rango/add_page.html',
                                          context_dict,
                                          context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print (form.errors)
    else:
        form = PageForm()

    context_dict['category_name_url']= category_name_url
    context_dict['category_name'] =  category_name
    context_dict['form'] = form

    return render_to_response( 'rango/add_page.html',
                               context_dict,
                               context)

def contact(request):
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
          # Email the profile with the
          # contact information
            template = get_template('rango/contact_template.txt')
            context_dict={}
            context = Context({
                             'contact_name': contact_name,
                             'contact_email': contact_email,
                             'form_content': form_content,
                              })
            content = template.render(context)
            email = EmailMessage(
                    "New contact form submission",
                    content,
                    'from@example.com',
                    ['to1@example.com'],
                    ['bcc@example.com'],
                    reply_to=['another@example.com'],
                    headers = {'Message-ID': contact_email}
                     )
            email.send(messages.success(request, 'Message sent successfully'))
            return redirect('contact')


    return render(request, 'rango/contact.html', {'form': form_class,})
@login_required
def update(request):
    try:
        user_profile=UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse("invalid user_profile!")

    if request.method == 'POST':
        form = UpdateProfile(data=request.POST or None, instance=request.user)
        update_profile_form= UserProfileForm(data=request.POST, instance=user_profile)
        if form.is_valid() and update_profile_form.is_valid:
            user=form.save()
            profile = update_profile_form.save(commit=False)
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

                profile.save()

            registered = True
        else:#user = request.user # #form = UpdateProfile(instance=user)
            print (form.errors, update_profile_form.errors)
    else:
        form= UpdateProfile(instance=request.user)
        update_profile_form= UserProfileForm(instance=user_profile)



    return render(request, 'rango/update_profile.html',{'form': form, 'update_profile_form': update_profile_form} )

def post_list(request):
    posts = Post.objects.all().order_by('published')
    return render (request, 'rango/list.html', {'posts': posts})

def post_detail (request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day,
                                   )
    return render(request, 'rango/detail.html', {'post': post})

def article(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'rango/article.html', {'posts': posts })