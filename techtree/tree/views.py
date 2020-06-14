from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'tree/index.html', {
    })

def treedict(request):
    
    
    return render(request, 'tree/treedict.html', {
        
    })