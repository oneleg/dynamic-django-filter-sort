from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from .models import *
from .serializers import *
from .serializer_names import *
# Create your views here.


def parse_kwargs(obj, is_main, impermissibly_models=[]):
    objs = obj['objs']
    kwargs = obj['kwargs']
    keys = kwargs.keys()
    if len(objs) > 0:
        for key in keys:
            value = kwargs[key]
            if type(value) == str and 'obj_' in value:
                obj_index = value.replace('obj_', '')
                hold_obj = objs[int(obj_index)]
                result = parse_kwargs(hold_obj, False)
                kwargs[key] = result

    class_name = obj['class_name']
    app_name = obj['app_name']
    desc = obj['desc']
    is_func_sort = obj['is_func_sort']
    many = obj['many']
    sort_type = obj['sort_type']
    if sort_type == '':
        sort_type = 'id'

    model_obj = apps.get_model(app_name, class_name)
    if is_main:
        if class_name in impermissibly_models: ## cant access to this model for filter and fetch data from client
            return None
        if desc:
            if is_func_sort:
                items = sorted(model_obj.objects.filter(**kwargs), key=lambda a: -getattr(a, sort_type)())
            else:
                items = model_obj.objects.filter(**kwargs).order_by('-%s'%(sort_type))
        else:
            if is_func_sort:
                items = sorted(model_obj.objects.filter(**kwargs), key=lambda a: getattr(a, sort_type)())
            else:
                items = model_obj.objects.filter(**kwargs).order_by('%s'%(sort_type))

        if many == False:
            print(items)
            print(items)
            return items[0]
        else:
            page = obj['page']
            show_article_count = 12
            page = (page-1) * show_article_count
            page_until = page + show_article_count
            return items[page:page_until]

    else:
        if desc:
            if is_func_sort:
                items = sorted(model_obj.objects.filter(**kwargs), key=lambda a: -getattr(a, sort_type)())
            else:
                items = model_obj.objects.filter(**kwargs).order_by('-%s'%(sort_type))
        else:
            if is_func_sort:
                items = sorted(model_obj.objects.filter(**kwargs), key=lambda a: getattr(a, sort_type)())
            else:
                items = model_obj.objects.filter(**kwargs).order_by('%s'%(sort_type))

        if many == False:
            return items[0]
        else:
            return items

@csrf_exempt
def filter_sort(request):
    received_json = JSONParser().parse(request)
    result_is_html = received_json['result_is_html']
    
    impermissibly_models = [] # Enter the names of the models without search access !!
    items = parse_kwargs(received_json, True)
   
    if result_is_html:
        page_name = received_json['page_name']
        result = render_to_string('%s-items.html'%(page_name), {'items': items})
    else:
        class_name = received_json['class_name']
        many = received_json['many']
        result = serializer_list[class_name](items, many=many).data

    result = JsonResponse({
        'status': True,
        'message': '',
        'items': result,
    })
    return result
