from django.shortcuts import render
from .models import Category,Project,ProjectImage
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import ContactForm

# Create your views here.

# def categories(request):
#     return{"categories": Category.objects.all()}

# def category_list(request,category_id):
#     category = get_object_or_404(Category,id=category_id)
#     return render(request,'work/category_list.html',{'categories':categories})

def demo_view(request):
    projects=Project.objects.all()
    return render(request, 'work/home.html',{'projects':projects})

def work(request):
    categories = Category.objects.all()
    projects = Project.objects.all()
    return render(request, 'work/work.html', {'categories': categories,'projects': projects},)




def project_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    projects = category.projects.all()  # Uses the related_name 'projects'
    return render(request, 'work/category_detail.html', {'category': category, 'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    images = project.images.all()  # Uses the related_name 'images'
    return render(request, 'work/project_detail.html', {'project': project, 'images': images})

def services(request):
    return render(request, 'work/services.html')
def about(request):
    return render(request, 'work/about.html')
def contact(request):
    return render(request, 'work/contact.html')
def start(request):
    return render(request, 'work/start.html')

def contactc(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('work:success')  # Redirect to a success page or message
    else:
        form = ContactForm()
    
    return render(request, 'work/start.html', {'form': form})

def success(request):
    return render(request, 'work/success.html')

