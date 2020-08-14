# Dynamic Filter And Sort In Django (have happy code :)

#### Sort and filter your models with just one function (any type of filter and sort) *-^
#### you can do any type of filter and sort you doed in django do here with one function
## Description

tow type of return result exist in this function html or json
for json we need create serializer and create a list of serializer_names.py side models.py
and in this file we create a object with name of model and value for this item is serializer models we created in serializers.py

our function is in core.views.py with filter_sort name 

in this project we need rest_framework first install that and after that add to Installed_app in setting.py 

for install all libraries just run this code
```bash
pip3 install -r requirements.txt
```

#### for more information see example project folder

## Usage
run project in example folder and in Postman call this url as POST "http://localhost:8000/filter_sort" 

simple body for filter_sort is like this (body type is raw->json)
```JSON
{
    "result_is_html": true,
    "page_name": "result1",
    "class_name": "Course",
    "app_name": "core",
    "desc": true,
    "sort_type": "lessons_count",
    "is_func_sort": true,
    "many": true,
    "page": 1,
    "objs": [],
    "kwargs": {"id__gte": 0, "name__icontains": " 1"}
}
```
### body fields description
#### result_is_html: 
if we want our result rendred in html set this field true else set false to recive filtred data as json.

#### page_name:     
if you want render data as html page set html page name in this field (end of html page must be like this '-items.html' for example in our project we have a page with 'result1-items.html' name and in body we just write result1 (I do this becuse i dont want user see my html page name :/ )
#### class_name:
name of our model to filter and sort

#### app_name:
our mode app name here is 'core'

#### desc:
sorting desc or asc

#### sort_type:

The name of the field or function of your model that we want to sort

#### is_func_sort
we sort on field or function if sorting with model function set true else set false

#### many 
want to result be a array of our object set this field true else set false to get one object in result

#### page
enter page of the items (for pagintation item)

#### objs
if we want to use inner join in our filter set other model information in this field. example of body with this field:
```JSON
{
    "result_is_html": false,
    "page_name": "",
    "class_name": "Course",
    "app_name": "core",
    "desc": true,
    "sort_type": "lessons_count",
    "is_func_sort": true,
    "many": true,
    "page": 1,
    "objs": [
        {
            "class_name": "Lesson",
            "app_name": "core",
            "desc": true,
            "sort_type": "id",
            "is_func_sort": false,
            "many": false,
            "objs": [],
            "kwargs": {"id": 2}
        }
    ],
    "kwargs": {"lessons": "obj_0"}
}
```
this body return Course object if course lessons include lesson with id 2
any obj in objs array have body fields special to that obj

#### kwargs:
this is object with our filter item
##### like
```JSON
{"id": 2, "name__icontain": "ali"}
```
anything in objects.model in django you can add to kwargs
