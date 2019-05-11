from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Author
from .dash_server import dash_dispatcher, clean_dash_content
from django.views.decorators.csrf import csrf_exempt
from .data_generator import insert_data

def index(request):

    # get the list of engagements:
    authors = Author.objects.all()

    # get dash content:
    #print(authors)

    context = {'authors': authors}

    return render(request, 'index.html', context=context)

def test(request):
    return render(request,'test.html',context={})

@csrf_exempt
def dash_ajax(request, **kwargs):
    #print('Function: dash_ajax')
    return HttpResponse(dash_dispatcher(request,), content_type='application/json')


def dashboard1(request, author_id):
    authors = Author.objects.all()

    # get the django context:
    #author = get_object_or_404(Author, pk=author_id)

    # print("Function: dash_django_page(): Getting 'dash_content'")
    dash_content = HttpResponse(dash_dispatcher(request,), content_type='application/json').getvalue()

    # clean the dash html content (the content contains lots of unnecessary characters like '\n')
    dash_content = clean_dash_content(dash_content)
    context = {'authors': authors, 'dash_content': dash_content}

    return render(request, 'dash.html', context=context)


def dashboard2(request, author_id):
    authors = Author.objects.all()

   # context = {'authors': authors[0]}

    # get the django context:
   # author = get_object_or_404(Author, pk=author_id)

    # print("Function: dash_django_page(): Getting 'dash_content'")
    dash_content = HttpResponse(dash_dispatcher(request,), content_type='application/json').getvalue()

    # clean the dash html content (the content contains lots of unnecessary characters like '\n')
    dash_content = clean_dash_content(dash_content)
    context = {'authors': authors, 'dash_content': dash_content}

    return render(request, 'dash.html', context=context)

def dashboard3(request, author_id):
    authors = Author.objects.all()

   # context = {'authors': authors[0]}

    # get the django context:
   # author = get_object_or_404(Author, pk=author_id)

    # print("Function: dash_django_page(): Getting 'dash_content'")
    dash_content = HttpResponse(dash_dispatcher(request,), content_type='application/json').getvalue()

    # clean the dash html content (the content contains lots of unnecessary characters like '\n')
    dash_content = clean_dash_content(dash_content)
    context = {'authors': authors, 'dash_content': dash_content}

    return render(request, 'body.html', context=context)


def dashboard4(request, author_id):
    authors = Author.objects.all()

   # context = {'authors': authors[0]}

    # get the django context:
   # author = get_object_or_404(Author, pk=author_id)

    # print("Function: dash_django_page(): Getting 'dash_content'")
    dash_content = HttpResponse(dash_dispatcher(request,), content_type='application/json').getvalue()

    # clean the dash html content (the content contains lots of unnecessary characters like '\n')
    dash_content = clean_dash_content(dash_content)
    context = {'authors': authors, 'dash_content': dash_content}

    return render(request, 'playerload.html', context=context)


@csrf_exempt
def livingstream(request):
    if request.is_ajax():
        # print("check,check")
        insert_data()

    return HttpResponse('success')