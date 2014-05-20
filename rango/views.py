from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import  PageForm, UserForm, UserProfileForm

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

# Create your views here.

def index(request):
    #obtain the context from the Http
    context = RequestContext(request)
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    #Modify the index page to also include the top 5 most viewed pages.
    #got a list of page objects and added them to the context view
    page_list = Page.objects.order_by('-views')[:5]
    context_dict ['pages'] = page_list
    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = encode_url(category.name)

    return render_to_response('rango/index.html',context_dict, context)

def category(request, category_name_url):
    #request our context from the request passed to us
    context = RequestContext(request)
    #Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    category_name = decode_url(category_name_url)
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name,
                    'category_name_url':category_name_url}

    try:
        #Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)
        context_dict ['pages'] = pages
        #We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    return render_to_response('rango/category.html', context_dict, context)



def about(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am the about page"}
    return render_to_response('rango/about.html',context_dict, context)


def add_category(request):
    # get contect from request
    context = RequestContext(request)
    #A HTTP post
    if request.method == "POST":
        form = CategoryForm(request.POST)

        #Is the form valid
        if form.is_valid():
            form.save(commit=True)

            #Now call the index(view)
            #the user sees the homepage
            return index(request)
        else:
            #form had errors
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()
    #Bad form/details/no form supplied
    #redner the form with error messages
    return render_to_response('rango/add_category.html',{'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method =="POST":
        form = PageForm(request.POST)

        if form.is_valid():
             # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('rango/add_category.html', {}, context)
            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            #Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors

    else:
        form = PageForm()
    return render_to_response("rango/add_page.html",
        {"category_name_url":category_name_url,
         "category_name": category_name,
         "form":form}, context)

def register(request):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method =="POST":
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #check to see if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            #save the form
            user= user_form.save()
            #hash the password and update the user
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

            #save the UserProfile model instane
            profile.save()
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
    #not http POST so render blank forms
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #Render  the templates

    return render_to_response(
        'rango/register.html',
        {'user_form': user_form, 'profile_form':profile_form,
         "registered": registered},context)



