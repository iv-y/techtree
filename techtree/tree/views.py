from django.shortcuts import render

from django.db.models import Count

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
                [al.full_name, al.num_likes] for al in x.alias_set.annotate(num_likes=Count('liked_users')).order_by('-num_likes')[:3]
            ],
            'best_prerequisites': [
                {'parent_code': pr_data.parent_course.course_code} for pr_data in x.prerequisite_dataset_as_child.annotate(num_likes=Count('liked_users')).order_by('-num_likes')[:3]
            ],
        }), selected_department_obj.course_set.all()))
        
        render_dict['course_dataset'] = courses
        
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
        code_set = [ (x['course_code'] , str(x['best_prerequisites'][0]['parent_code'] if x['best_prerequisites'] else "")) for x in courses]
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
            _trad = "".join([course['course_code'], "<br>", course['full_name'], f'''
                <br>
                { "".join(map( (lambda x: '"%s", '%str(x[0])) ,course['best_aliases']))[0:-2] if course['best_aliases'] else "별칭 미등록" }
            '''])
            tree_param[course['course_code']] = dict(trad = _trad)
        
        render_dict['tree_param'] = json.dumps(tree_param)
            
    render_dict['departments'] = json.dumps(departments)
    render_dict['selected_department'] = json.dumps(selected_department)
    
    return render(request, 'tree/treedict.html', render_dict)
