from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'tree/index.html', {
        'testdata': (['django', 'vue.js', 'using', 'together'])
    })