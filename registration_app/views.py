from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import RegistrationForm, EventForm

from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from .models import Company
from django.contrib.auth.models import User

def registration_form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)  # Don't save immediately
            company.created_by = request.user  # Assign the logged-in user to 'created_by'

            # Process the bulleted_list field
            # bulleted_list = form.cleaned_data.get('bulleted_list', '')
            # processed_bullets = '\n'.join([line if line.startswith('*') else f'* {line}' for line in bulleted_list.splitlines() if line.strip()])
            # company.bulleted_list = processed_bullets

            company.save()  # Save the company instance

            messages.success(request, "Company registered successfully!")
            return redirect('new_index')  # Redirect after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Fetch the company using the provided email
            company = Company.objects.get(email=email)

            # Check if the company's status is 'approved'
            if company.status != 'approved':
                messages.error(request, "Your account is not approved yet.")
                return render(request, 'login.html')

            # Use check_password to validate the entered password against the hashed password
            if check_password(password, company.password):
                # Ensure the User object exists
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={'email': email},
                )

                # Log the user in
                auth_login(request, user)

                return redirect('landing')  # Redirect to landing page on success
            else:
                messages.error(request, "Invalid email or password.")  # Password mismatch
        except Company.DoesNotExist:
            messages.error(request, "No company found with that email.")  # Company not found

    return render(request, 'login.html')


from django.shortcuts import render
from .models import Company


def landing_page(request):
    company = None
    if request.user.is_authenticated:
        try:
            # Fetch the company for the logged-in user with status 'approved'
            company = Company.objects.filter(email=request.user.email, status='approved').first()
            if not company:
                print("No approved company found for this user.")
        except Company.DoesNotExist:
            print("No company found for this user.")
    return render(request, 'land_test.html', {'company': company})


def company_landing_page(request, company_id): 
    try:
        # Fetch the company by ID
        company = Company.objects.get(id=company_id, status='approved')
    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect('partners')  # Redirect back to the partners page if the company doesn't exist

    return render(request, 'landing.html', {'company': company})



def partners(request):
    # Query only approved companies
    companies = Company.objects.filter(status='approved')

    # for comp in companies:
    #     print(f"Company Name: {comp.name}, Status: {comp.status}")

    return render(request, 'partners.html', {'companies': companies})


def partners_copy(request):
    # Query only approved companies
    companies = Company.objects.filter(status='approved')

    # for comp in companies:
    #     print(f"Company Name: {comp.name}, Status: {comp.status}")

    return render(request, 'partners_copy.html', {'companies': companies})


# def index(request):
#     # Query only approved companies
#     companies = Company.objects.filter(status='approved')
#
#     # Debugging logs
#     print("Approved Companies for Index Page:")
#     for comp in companies:
#         print(f"Company Name: {comp.name}, Status: {comp.status}")
#
#     return render(request, 'index.html', {'companies': companies})
from django.shortcuts import render
from .models import Company, NewsUpload, Event


def index(request):
    # Query only approved companies
    companies = Company.objects.filter(status='approved')

    # Query all news articles ordered by publication date (most recent first)
    news_articles = NewsUpload.objects.order_by('-publication_date')

    # Query all events
    events = Event.objects.all()

    # Render the template and pass the context
    return render(request, 'index.html', {
        'companies': companies,
        'news_articles': news_articles[:11],  # Pass all news articles here
        'events': events[:11],  # Show only the first 3 events
    })


from django.shortcuts import render
from .models import Company  # Make sure to import the Company model


def land(request):
    company = None
    companies = Company.objects.all(status='approved')  # Fetch all companies
    print("All Companies:")
    for comp in companies:
        print(f"Company Name: {comp.name}")
        print(f"Email: {comp.email}")
        print(f"Status: {comp.status}")
        print(f"Description: {comp.description}")
        print(f"Logo: {comp.logo.url if comp.logo else 'No logo'}")
        print(f"Banner: {comp.banner.url if comp.banner else 'No banner'}")
        print(f"Created By: {comp.created_by.email}")
        print("-" * 30)  # Separator for readability

    if request.user.is_authenticated:
        print(f"Logged-in User: {request.user.email}")
        try:
            # Fetch the company where the company email matches the logged-in user's email
            company = Company.objects.get(email=request.user.email)
            print(f"Company Name: {company.name}")
            print(f"Email: {company.email}")
            print(f"Status: {company.status}")
            print(f"Description: {company.description}")
            print(f"Logo: {company.logo.url if company.logo else 'No logo'}")
            print(f"Banner: {company.banner.url if company.banner else 'No banner'}")
            print(f"Created By: {company.created_by.email}")
        except Company.DoesNotExist:
            print("No company found for the logged-in user.")

    return render(request, 'land_test.html', {'company': company})


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Company


def reset_password(request, uidb64, token):
    try:
        # Decode user id from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Process the password reset form
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                # Save the new password to the User model
                form.save()

                # Also update the password in the Company model
                # Find the corresponding Company record
                try:
                    company = Company.objects.get(created_by=user)
                    company.password = make_password(form.cleaned_data['new_password1'])
                    company.save()
                    messages.success(request, "Your password has been reset successfully.")
                except Company.DoesNotExist:
                    messages.error(request, "Company associated with this user not found.")

                return redirect('login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or expired.")
        return redirect('forgot_password')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Company

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Company

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Company

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Company


def forgot_password(request):
    if request.method == 'POST':
        # Step 1: Get email from the form
        email = request.POST.get('email')
        print(f"POST request received. Email entered: {email}")

        # Check if email is empty
        if not email:
            print("No email provided.")
            messages.error(request, "Please provide an email address.")
            return redirect('forgot_password')  # Redirect back to the form

        try:
            # Step 2: Fetch the company using the provided email
            company = Company.objects.get(email=email)
            print(f"Company found. Company email: {company.email}")

            # Step 3: Compare emails
            print(f"User typed email: {email}")
            print(f"Company stored email: {company.email}")

            if email == company.email:
                print("Emails match!")  # This should show in the logs if emails match

                # Step 4: Check if new password is being submitted
                if 'new_password' in request.POST:
                    new_password = request.POST.get('new_password')
                    print(f"New password received: {new_password}")

                    # Step 5: Hash the new password and save it
                    company.password = make_password(new_password)
                    company.save()
                    print("Password updated successfully.")

                    messages.success(request, "Password updated successfully.")
                    return redirect('login')  # Redirect to login page after updating password

                # Step 6: Render the form to enter new password
                print("Rendering new password form.")
                return render(request, 'forgot_password.html', {'email': email, 'step': 'new_password'})

            else:
                print("Emails do not match!")  # Debugging mismatch (though unlikely)

        except Company.DoesNotExist:
            print(f"No company found with email: {email}")
            messages.error(request, "No company found with that email.")
            return redirect('forgot_password')

    # If the method is GET or the user is still on the first step, show the email form
    print("GET request or initial POST request, rendering email input form.")
    return render(request, 'forgot_password.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from .forms import CompanyForm
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def superuser_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('admin_page')
        else:
            messages.error(request, "Invalid credentials or not a superuser.")
    return render(request, 'admin_login.html')  # Custom login template


from django.contrib.auth.decorators import login_required, user_passes_test


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})


@login_required
@user_passes_test(is_superuser)
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Company created successfully!")
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'add_new_company.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CompanyForm
from .models import Company


# @login_required
# @user_passes_test(is_superuser)
# def company_update(request, pk):
#     company = get_object_or_404(Company, pk=pk)
#
#     if request.method == 'POST':
#         form = CompanyForm(request.POST, request.FILES, instance=company)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Company updated successfully!")
#             return redirect('company_list')  # Redirect after successful update
#         else:
#             messages.error(request, "There was an error with the form. Please check your input.")
#
#     else:
#         form = CompanyForm(instance=company)
#
#     return render(request, 'company_form.html', {'form': form, 'company': company})
@login_required
@user_passes_test(is_superuser)
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.method == 'POST':
        print("🔧 POST request received")
        form = CompanyForm(request.POST, request.FILES, instance=company)

        if form.is_valid():
            print("✅ Form is valid")
            updated_company = form.save(commit=False)

            # Debug print each field
            for field in form.cleaned_data:
                print(f"{field}: {form.cleaned_data[field]}")

            updated_company.save()
            messages.success(request, "Company updated successfully!")
            return redirect('company_list')

        else:
            print("❌ Form is invalid")
            print(form.errors)  # show validation errors in console
            messages.error(request, "There was an error with the form. Please check your input.")
    else:
        print("ℹ️ GET request - loading form")
        form = CompanyForm(instance=company)

    return render(request, 'company_form.html', {'form': form, 'company': company})


@login_required
@user_passes_test(is_superuser)
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, "Company deleted successfully!")
        return redirect('company_list')
    return render(request, 'company_confirm_delete.html', {'company': company})


# Newly added Lines

from .models import NewsUpload, Event
from .forms import NewsForm


def news_list(request):
    news_articles = NewsUpload.objects.order_by('-publication_date')  # Latest news first
    return render(request, 'news_list.html', {'news_articles': news_articles})


def create_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form})


def news_page(request, news_id):
    try:
        news = NewsUpload.objects.get(id=news_id)
    except NewsUpload.DoesNotExist:
        messages.error(request, "News not found.")
        return redirect('news_list')  # Redirect back to the partners page if the company doesn't exist

    return render(request, 'news_content.html', {'news': news})


# method for event creation
def event_list(request):
    events = Event.objects.order_by('-date')  # Latest Event first
    return render(request, 'events.html', {'events': events})


def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save()
            return redirect('event_list')
    else:
        event_form = EventForm()
    return render(request, 'create_event.html', {'event_form': event_form})


def event_page(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event_list')  # Redirect back to the partners page if the company doesn't exist

    return render(request, 'news_content.html', {'event': event})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import NewsUpload
from .forms import NewsForm


# Create
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "News article created successfully.")
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news_create.html', {'form': form})


# Read (list all news)
# def news_list(request):
#     news_list = NewsUpload.objects.all().order_by('-publication_date')
#     return render(request, 'news_list.html', {'news_list': news_list})

# Update
def news_update(request, news_id):
    news = get_object_or_404(NewsUpload, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, "News article updated successfully.")
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_update.html', {'form': form, 'news': news})


# Delete
def news_delete(request, news_id):
    news = get_object_or_404(NewsUpload, id=news_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, "News article deleted successfully.")
        return redirect('news_list')
    return render(request, 'news_delete.html', {'news': news})


# events
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Event
from .forms import EventForm
from django.contrib import messages


# View to display all events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


# View to create a new event
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})


# View to display a single event's details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


# View to update an event
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})


# View to delete an event
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})


# Simple view for the news list page
def admin_page(request):
    return render(request, 'admin_page.html')


# method for event creation
def event_list1(request):
    events = Event.objects.order_by('-date')  # Latest Event first
    return render(request, 'events.html', {'events': events})

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def new_index1(request):
    companies = Company.objects.filter(status='approved')
    news_articles = NewsUpload.objects.order_by('-publication_date')
    events = Event.objects.all()
    if request.method == 'POST':
        try:
            # Extract form data safely with .get()
            message = request.POST.get('message', '').strip()
            email = request.POST.get('email', '').strip()
            name = request.POST.get('name', '').strip()
            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Invalid email format.')
                return render(request, 'new_index.html')

            # Send the email
            send_mail(
                'Contact Form',  # Subject of the email
                message,  # Body of the email
                settings.EMAIL_HOST_USER,  # From email (configured in settings.py)
                [email],  # To email (from the form)
                fail_silently=False,  # Raise errors if email can't be sent
            )

            # If successful, send a success message
            messages.success(request, 'Your message has been sent!')

        except Exception as e:
            # General exception handler if anything unexpected occurs
            messages.error(request, f'There was an error sending your message: {str(e)}')
    return render(request, 'new_index.html', {
        'companies': companies,
        'news_articles': news_articles[:11],  # Pass all news articles here
        'events': events[:11], })


def meetings(request):
    return render(request, 'meetings.html')


#     Newly Added Lines
def about(request):
    return render(request, 'about.html')


def home2(request):
    return render(request, 'home.html')


# def events(request):
#     return render(request, 'events_news.html')


def l1(request):
    company = None
    if request.user.is_authenticated:
        try:
            # Fetch the company for the logged-in user with status 'approved'
            company = Company.objects.filter(email=request.user.email, status='approved').first()
            if not company:
                print("No approved company found for this user.")
        except Company.DoesNotExist:
            print("No company found for this user.")
    return render(request, 'landing.html', {'company': company})

def events(request):
    events = Event.objects.order_by('-date')  # Latest Event first
    return render(request, 'events_news.html', {'events': events})

def news_new(request):
    news_articles = NewsUpload.objects.order_by('-publication_date')
    return render(request, 'events_news.html', {'news_articles': news_articles})


from django.db.models import Q
import re


def partners_new(request):
    query = request.GET.get('search', '').strip()
    cleaned_query = re.sub(r'[^\w\s]', '', query)

    # Base query
    if query:
        companies = Company.objects.filter(
            Q(status='approved') &
            (Q(name__icontains=cleaned_query) | Q(services__icontains=cleaned_query))
        )
    else:
        companies = Company.objects.filter(status='approved')

    # Order: Premium first, and among them by when they became premium (oldest first)
    companies = companies.order_by('-user_type')


    # Fix encoding issues
    for company in companies:
        try:
            company.name.encode('utf-8').decode('utf-8')
            company.services.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            company.name = company.name.encode().decode('latin1', errors='replace')
            company.services = company.services.encode().decode('latin1', errors='replace')

    return render(request, 'events_news.html', {'companies': companies, 'query': query})
