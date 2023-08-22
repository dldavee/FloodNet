from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageForm,UserForm
from .models import ImageModel,Imageclassfication
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from random import randint
from django.db.models import Count
import openpyxl
from django.http import HttpResponse


def dashboard_login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            if user.is_superuser :
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password', extra_tags='login-error')  # Send an alert message
    return render(request, 'login.html')


def dashboard_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        print(user_form.is_valid())
        if user_form.is_valid():
            signup = user_form.save()
            signup.password = make_password(user_form.cleaned_data['password'])
            signup.save()
            messages.success(request, 'user created successfully')  # Send an alert message
        
    return render(request, 'register.html')

def dashboard_logout(request):
    logout(request)
    return redirect('home')

def get_random_image(user_id):
    all_images = ImageModel.objects.filter(count__lt=3)
    classified_images = Imageclassfication.objects.filter(user=user_id).values_list('image', flat=True)
    print(classified_images)
    unclassified_images = all_images.exclude(id__in=classified_images).aggregate(total=Count('id'))['total']

    if unclassified_images > 0:
        random_index = randint(0, unclassified_images - 1)

        # Retrieve the random image using the random index
        random_image =all_images.exclude(id__in=classified_images).order_by('?')[random_index]
        return random_image
    return None

@login_required
def image_classification(request):
    user = request.user.id
    user_id = User.objects.get(id=user)
    if request.method == 'POST':
        floodstatus = request.POST.get('flood_status')
        image = request.POST.get('image_id')
        image_id = ImageModel.objects.get(id=image)
        count = int(image_id.count)+1
        ImageModel.objects.filter(id=image_id.id).update(count=count)
        Imageclassfication.objects.create(user=user_id,image=image_id,is_flooded=floodstatus)
    
    images = get_random_image(user_id)

    return render(request, 'classification.html', {'images': images})

@login_required
def dashboard(request):
    count = ImageModel.objects.all().count()
    users = User.objects.all().count()
    return render(request, 'dashboard.html',context={"imagecount":count,"users":users})
@login_required
def user_dashboard(request):
    return render(request, 'userdashboard.html')

@login_required
def image_upload(request):
    print('Uploading',request.method)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            for image in request.FILES.getlist('image'):
                img = ImageModel.objects.create(image=image)
                messages.success(request, 'Images uploaded successfully!')
    return render(request, 'imageupload.html')


@login_required
def list_images(request):
    data = Imageclassfication.objects.all()
    return render(request, 'listimages.html',context={'images':data})



def download_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    column_names = ['Image Name', 'User Name','Is_Flooded']
    sheet.append(column_names)
    queryset = Imageclassfication.objects.all().values('image__image_name','user__username','is_flooded')
    for instance in queryset:
        row_data = [instance['image__image_name'],instance['user__username'],instance['is_flooded']]
        sheet.append(row_data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=classification_data.xlsx'
    workbook.save(response)
    
    return response