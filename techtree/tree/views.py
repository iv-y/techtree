from django.shortcuts import render
import json

from .models import *

# Create your views here.
def index(request):
    return render(request, 'tree/index.html', {})

def treedict(request, department_code=None):
    
    departments = list(map((lambda x: {
        'full_name': x.full_name,
        'short_name': x.short_name,
        'alpha_code': x.alphabet_short_name,
    }), Department.objects.all()))
    
    selected_department = 0
    selected_department_obj = None
    if department_code:
        for x in departments:
            if x['alpha_code'] == department_code:
                selected_department = x
                selected_department_obj = Department.objects.filter(alphabet_short_name=department_code)[0]
                break
                
    if selected_department: # found corresponding department
        courses = list(map((lambda x: {
            'full_name': x.full_name,
            'course_type_full': x.course_type.full_name,
            'course_type_short': x.course_type.short_name,
            'department_full': x.department.full_name,
            'department_short': x.department.short_name,
            'department_code': x.department.alphabet_short_name,
            'description': x.description,
            'course_code': x.course_code,
        }), selected_department_obj.course_set.all()))
        
        selected_department['course_set'] = courses
    
    return render(request, 'tree/treedict.html', {
        'departments': json.dumps(departments),
        'selected_department': json.dumps(selected_department),
    })