from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'tree/index.html', {
        'user_authenticated': request.user.is_authenticated,
    })

def treedict(request):
    
    
    return render(request, 'tree/treedict.html', {
        
    })