from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'tree/index.html', {
        'user_authenticated': request.user.is_authenticated,
    })

def login(request):
    return render(request, 'tree/login.html', {})