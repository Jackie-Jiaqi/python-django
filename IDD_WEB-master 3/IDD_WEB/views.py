from .mongodb import *
from .models import *
from .models import JSONForm
import json
from datetimewidget.widgets import DateTimeWidget
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from .models import Author


def admin(request):
    return redirect(request, 'admin')


def login(request):
    return render(request, 'login.html')


def index(request):
    # get the list of engagements:
    authors = Author.objects.all()

    # get dash content:
    # print(authors)

    context = {'authors': authors}

    return render(request, 'index.html', context=context)


def dashboard(request):
    return render(request, 'dashboard.html')


def charts(request):
    return render(request, 'charts.html')


def view_data(request):
    return render(request, 'view_data.html')


def new_mongo_connection(request):
    if request.method == "POST":
        form = MongoForm(request.POST)
        if form.is_valid():
            MongoConn = form.save(commit=False)
            MongoConn.dbname = form.cleaned_data.get('dbname')
            MongoConn.ip = form.cleaned_data.get('ip')
            MongoConn.port = form.cleaned_data.get('port')
            MongoConn.username = form.cleaned_data.get('username')
            MongoConn.password = form.cleaned_data.get('password')
            MongoConn.auth_collection = form.cleaned_data.get('auth_collection')
            conn = MongoConnect()
            if conn.auth(MongoConn.dbname, MongoConn.username, MongoConn.password) == 1:
                MongoConn.save()
                return redirect('view_data')
            else:
                form = MongoForm()
                return render(request, 'new_mongo_connection.html', {'form': form})
    else:
        form = MongoForm()
    return render(request, 'new_mongo_connection.html', {'form': form})


@csrf_exempt
def data_list(request):
    print("************************************************")
    print(request.GET.get('order[0][dir]'))
    draw = int(request.GET.get('draw'))
    length = int(request.GET.get('length'))
    start = int(request.GET.get('start'))
    # search_value = request.GET.get('search[value]', None)[0]
    order_column = request.GET.get('order[0][column]')
    order = request.GET.get('order[0][dir]')
    column_list = {"0": "Latitude",
                        "1": "Longitude",
                        "2": "Surface Temperature (kelvin)",
                        "3": "Datetime",
                        "4": "Power",
                        "5": "Date",
                        "6": "Surface Temperature (Celcius)"}
    column = column_list[order_column]
    print(length, type(length), start, type(start), column, type(column), order, type(order), type("xxx"))
    conn = MongoConnect()
    conn.auth("admin", "axicor", "abc123")
    data = conn.data_list("IoT", "fire", column, order, start, length)
    result = dict()
    result['data'] = data
    result['draw'] = draw
    result['recordsTotal'] = length
    result['recordsFiltered'] = length
    print(result)
    return HttpResponse(json.dumps(result), content_type='application/json')


def new_csv_connection(request):
    if request.method == "POST":
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            CSVConn = form.save(commit=False)
            CSVConn.filename = form.cleaned_data.get('filename')
            CSVConn.document_upload_date = timezone.now()
            CSVConn.save()
            return redirect('index')
    else:
        form = CSVForm()
    return render(request, 'new_csv_connection.html', {'form': form})


def new_json_connection(request):
    if request.method == "POST":
        form = JSONForm(request.POST, request.FILES)
        if form.is_valid():
            JSONConn = form.save(commit=False)
            JSONConn.filename = form.cleaned_data.get('filename')
            JSONConn.document_upload_date = timezone.now()
            JSONConn.save()
            return redirect('index')
    else:
        form = JSONForm()
    return render(request, 'new_json_connection.html', {'form': form})


def new_excel_connection(request):
    if request.method == "POST":
        form = EXCELForm(request.POST, request.FILES)
        if form.is_valid():
            EXCELConn = form.save(commit=False)
            EXCELConn.filename = form.cleaned_data.get('filename')
            EXCELConn.document_upload_date = timezone.now()
            EXCELConn.save()
            return redirect('index')
    else:
        form = EXCELForm()
    return render(request, 'new_excel_connection.html', {'form': form})