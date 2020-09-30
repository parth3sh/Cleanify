
from django.shortcuts import render
from run import run

def index(request):
    return render(request,'index.html')

def clean(request):

    dirtyuri = request.POST.get('URI')
    cleanURI = run(dirtyuri)

    return render(request,'clean.html', {'cleanURI': cleanURI})

