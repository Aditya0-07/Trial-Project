from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count
from accounts.models import CustomUser
from django.contrib import messages
import json

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')  
            return redirect('dashboard')  
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def admin_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html', {'user': request.user})

@staff_member_required
def admin_dashboard(request):
    
    selected_country = request.GET.get('country', 'all')

    countries = CustomUser.objects.values_list('country', flat=True).distinct()

    
    if selected_country != 'all':
        users = CustomUser.objects.filter(country=selected_country)
    else:
        users = CustomUser.objects.all()

   
    paginator = Paginator(users, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   
    user_distribution = CustomUser.objects.values('country').annotate(user_count=Count('country'))
    user_distribution_json = json.dumps(list(user_distribution))

   
    return render(request, 'admin_dashboard.html', {
        'page_obj': page_obj,
        'countries': countries,
        'selected_country': selected_country,  
        'user_distribution': user_distribution_json,
    })

@user_passes_test(lambda u: u.is_staff)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, f'User {user.username} has been deleted successfully.')
    return redirect('admin_dashboard')
