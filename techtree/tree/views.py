from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.db.models import Count

import json

from .models import *

# Create your views here.
def index(request):
    return render(request, 'tree/index.html', {})

def treedict_alias_toggle(request, c_code, a_id, uncheck):
    
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    course = get_object_or_404(Course, course_code=c_code)
    try:
        selected_alias = course.alias_set.get(pk=a_id)
    except (KeyError, Alias.DoesNotExist):
        raise Http404('There is no such alias.')
    else:
        if uncheck:
            selected_alias.liked_users.filter(id=request.user.id).delete()
        else:
            selected_alias.liked_users.add(request.user)
        selected_alias.save()
        return HttpResponse("");

def treedict_alias_create(request, c_code, a_full_name):
    if not request.user.is_authenticated:
        raise PermissionDenied
    course = get_object_or_404(Course, course_code=c_code)
    Alias.objects.create(full_name=a_full_name, course=course, author=request.user)

    
@login_required
def treedict_prerequisite_toggle(request, c_code):
    course = get_object_or_404(Course, course_code=c_code)
    try:
        selected_alias = course.alias_set.get(pk=request.POST['id'])
    except (KeyError, Alias.DoesNotExist):
        raise Http404('There is no such alias.')
    else:
        if request.POST['unchecked']:
            selected_alias.liked_users.filter(id=request.user.id).delete()
        else:
            selected_alias.liked_users.add(request.user)
        selected_alias.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tree_dict', args=(course.department.alphabet_short_name,)))

@login_required
def treedict_prerequisite_create(request, c_code):
    course = get_object_or_404(Course, course_code=c_code)
    Alias.objects.create(full_name=request.POST['full_name'], course=course, author=request.user)
    
    
    
    
    
    
    

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
                
    render_dict = dict()
    render_dict['tree_structure'] = json.dumps(0)
    render_dict['tree_param'] = json.dumps(0)
    render_dict['course_dataset'] = json.dumps(0)
                
    if selected_department: # found corresponding department
        courses = list(map((lambda x: {
            'full_name': x.full_name,
            'course_type_full': x.course_type.full_name,
            'course_type_short': x.course_type.short_name,
            'department_full': x.department.full_name,
            'department_short': x.department.short_name,
            'department_code': x.department.alphabet_short_name,
            'description': x.description,
            'course_code': str(x.course_code),
            'best_aliases': [
                [
                    al.full_name, 
                    al.num_likes,
                    al.author.username if al.author.username else "(Unknown)",
                    1 if al.liked_users.filter(id=request.user.id).exists() else 0,
                    al.id,
                ] for al in x.alias_set.annotate(num_likes=Count('liked_users')).order_by('-num_likes')[:]
            ],
            'best_prerequisites': [
                [
                    pr_data.parent_course.course_code,
                    pr_data.num_likes,
                    pr_data.author.username if pr_data.author.username else "(Unknown)",
                    1 if pr_data.liked_users.filter(id=request.user.id).exists() else 0,
                    pr_data.id,
                ] for pr_data in x.prerequisite_dataset_as_child.annotate(num_likes=Count('liked_users')).order_by('-num_likes')[:]
            ],
            'best_children': [
                [
                    pr_data.parent_course.course_code,
                    pr_data.num_likes,
                    pr_data.author.username if pr_data.author.username else "(Unknown)",
                    1 if pr_data.liked_users.filter(id=request.user.id).exists() else 0,
                ] for pr_data in x.prerequisite_dataset_as_parent.annotate(num_likes=Count('liked_users')).order_by('-num_likes')[:]
            ],
        }), selected_department_obj.course_set.all()))
        
        render_dict['course_dataset'] = json.dumps(courses)
        
        # Build tree structure.
        
        tree_st = dict()
        
        def iter_tree(tree_point_name, tree_point):
            li = list()
            li.append((tree_point_name, tree_point))
            for child_key, child_val in tree_point.items():
                li.extend(iter_tree(child_key, child_val))                
            return li
        
        def iter_codetree():
            return iter_tree("", tree_st)
        
        flag = 0
        first_loop = True
        code_set = [ (x['course_code'] , str(x['best_prerequisites'][0][0] if x['best_prerequisites'] else "")) for x in courses]
        # (child, parent)
        mias = dict()
        
        for x, parent in code_set:
            
            x_dict = dict()
            #try to find other mias
            #mia: (selfcode, parentcode, child_dict)
            for index, mia in enumerate(mias):
                if mia[1] == x:
                    x_dict[mia[0]] = mia[2]
                    mias.pop(index)
            
            # something feels strange to say 'if not parent', but this is just piece of code X(
            # parent is "", direct child of root
            if not parent:
                tree_st[x] = x_dict
                continue
            
            # parent can be already on the tree, or not.
            for tree_object_tuple in iter_codetree():
                if tree_object_tuple[0] == parent:
                    # Found x's parent! add x to its parent
                    tree_object_tuple[1][x] = x_dict
                    flag = 1
                    break
            
            if flag == 1:
                flag = 0
                continue
                
            #Failed to find x's parent... X(
            mias.append((x, parent, x_dict))
            
        tree_root_id = "".join([str(selected_department['alpha_code'])])
        render_dict['tree_structure'] = json.dumps({tree_root_id: tree_st});
        
        tree_param = {tree_root_id: {'trad':str(selected_department['full_name'])}}
        for course in courses:
            _trad = "".join([
                course['course_code'], 
                "<br>", 
                course['full_name'], 
                "<br>", 
                ( "".join(map( (lambda x: '"%s", '%str(x[0])),
                              course['best_aliases'][:3]))[0:-2] if course['best_aliases'] else "별칭 미등록" ), 
            ])
            
            tree_param[course['course_code']] = dict(trad = _trad)
        
        render_dict['tree_param'] = json.dumps(tree_param)
            
    render_dict['departments'] = json.dumps(departments)
    render_dict['selected_department'] = json.dumps(selected_department)
    
    return render(request, 'tree/treedict.html', render_dict)
