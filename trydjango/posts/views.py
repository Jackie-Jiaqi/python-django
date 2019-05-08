from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post, Bugs
from django.contrib import messages
from .forms import PostForm
from .classification import Image_identify
import os
import cv2
import tflearn
import numpy as np
import tensorflow as tf
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import io
from MyQR import myqr
import os
import matplotlib.pyplot as plt
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
from django.contrib.auth.decorators import login_required
from IPython.display import Image
from django.views.decorators.csrf import csrf_exempt


# @login_required(login_url='/login/')
def post_home(request):
    # query_set_list = Post.objects.all()#.order_by("-timestamp")
    context = {
        # 'title': 'HOME PAGE',
        # 'Post_query': query_set,
    }
    return render(request, 'Home.html', context)


# @login_required(login_url='/login/')
def post_update(request,id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "successfully update")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": "Detail",
        "instance": instance,
        "form":form
    }
    return render(request, "forms.html", context)

# @login_required(login_url='/login/')
def post_create(request):
    extention_list= ['jpg','png','jpeg']
    form = PostForm(request.POST or None,request.FILES or None)
    try:
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.image.url[-3:] not in extention_list and instance.image.url[-4:] not in extention_list:
                return redirect("http://127.0.0.1:8000/create/")
            instance.save()
            messages.success(request,"successfully upload")
            return HttpResponseRedirect(instance.get_absolute_url())
    except():
        return render(request, 'forms.html', {
                     "form": form,
                     'error_message': "You did not select a chioce."})
    # else:
    #     messages.error(request,"Not successfully upload yet")
    text = "Please upload an image with jpg, png or jpeg extention"
    context = {
        "form": form,
        "text": text,
    }
    return render(request, "forms.html", context)


# @login_required(login_url='/login/')
def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    if (request.GET.get('mybtn')):
        return HttpResponseRedirect(instance.get_absolute_url_result())
    context = {
        "title": "Detail",
        "instance": instance
    }
    return render(request, "detail.html", context)

# @login_required(login_url='/login/')
def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "successfully delete")
    return redirect('posts:list')

# @login_required(login_url='/login/')
def classify_image(request, id=None):
    instance = get_object_or_404(Post, id=id)
    test_data = "./media"
    str_label=Image_identify.process_test_data(test_data)
    context={
        "instance": instance,
        "str_label": str_label
    }
    return render(request, "result.html", context)


def login(request):
    return render(request, 'login.html')


# @login_required(login_url='/login/')
def Home(request):
    return render(request, "Home.html", {})


# @login_required(login_url='/login/')
def bug_pic_gallery(request):

    return render(request, "bug_pic_gallery.html", {})


# @login_required(login_url='/login/')
def post_about(request):
    return render(request, "about.html", {})


# @login_required(login_url='/login/')
def post_cabbagewhitefly(request):
    return render(request, "Cabbage-Whitefly.html", {})


# @login_required(login_url='/login/')
def post_cabbagemoth(request):
    return render(request, "Cabbage_Moth.html", {})


# @login_required(login_url='/login/')
def post_cabbageworms(request):
    return render(request, "Cabbage_worms.html", {})


# @login_required(login_url='/login/')
def post_citrusleafminer(request):
    return render(request, "Citrus_Leafminer.html", {})


# @login_required(login_url='/login/')
def post_cutworm(request):
    return render(request, "cutworm.html", {})


# @login_required(login_url='/login/')
def post_europeanearwigs(request):
    return render(request, "European_Earwigs.html", {})


# @login_required(login_url='/login/')
def post_japanesebeetle(request):
    return render(request, "Japanese_Beetle.html", {})


# @login_required(login_url='/login/')
def post_mealybugs(request):
    return render(request, "Mealybugs.html", {})


# @login_required(login_url='/login/')
def post_psyllids(request):
    return render(request, "Psyllids.html", {})


# @login_required(login_url='/login/')
def post_slugs(request):
    return render(request, "Slugs.html", {})


# @login_required(login_url='/login/')
def post_yellowaphids(request):
    return render(request, "Yellow_Aphids.html", {})


# @login_required(login_url='/login/')
def search_bug_name(request):
    return render(request, "search_bugs_by_name.html", {})


# @login_required(login_url='/login/')
def managebugs(request):
    Bug = Bugs.objects.all()
    query = request.GET.get('commonname')
    if query:
        Bug = Bug.filter(commonname__icontains=query)
    else:
        pass
    context = {
         "Bug": Bug
    }
    return render(request,'search_bugs_by_category.html',context)

# @login_required(login_url='/login/')
def post_Banksia(request):
    return render(request, "Banksia.html", {})


# @login_required(login_url='/login/')
def post_Beech(request):
    return render(request, "Beech.html", {})


# @login_required(login_url='/login/')
def post_Eucalyptus(request):
    return render(request, "Eucalyptus.html", {})


# @login_required(login_url='/login/')
def post_Grevillea(request):
    return render(request, "Grevillea.html", {})


# @login_required(login_url='/login/')
def post_Illawarra(request):
    return render(request, "Illawarra.html", {})


# @login_required(login_url='/login/')
def post_Lilly(request):
    return render(request, "Lilly.html", {})


# @login_required(login_url='/login/')
def post_Moreton(request):
    return render(request, "Moreton.html", {})


# @login_required(login_url='/login/')
def post_Wattle(request):
    return render(request, "Wattle.html", {})


# @login_required(login_url='/login/')
def post_Willow(request):
    return render(request, "Willow.html", {})



# @login_required(login_url='/login/')
def leaf_pic_gallery(request):

    return render(request, "leaf_pic_gallery.html", {})



# @login_required(login_url='/login/')
def post_prevent(request):
    return render(request, "prevention.html", {})




# @login_required(login_url='/login/')
def prevent(request):
    return render(request, "prevention.html", {})

# @login_required(login_url='/login/')
def test(request,id=None):
    IMG_SIZE = 50
    LR = 1e-3
    MODEL_NAME = 'dwij28leafdiseasedetection-{}-{}.model'.format(LR, '2conv-basic')
    tf.logging.set_verbosity(tf.logging.ERROR)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    verifying_data = []
    instance = get_object_or_404(Post, id=id)
    filepath = instance.image.url
    filepath = '.'+filepath
    img_name = filepath.split('.')[:2]
    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    verifying_data = [np.array(img), img_name]

    np.save('verify_data.npy', verifying_data)
    verify_data = verifying_data

    str_label = "Cannot make a prediction."
    status = "Error"

    tf.reset_default_graph()

    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 4, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')

    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        #print ('Model loaded successfully.')
    else:
        #print ('Error: Create a model using neural_network.py first.')
        pass
    img_data, img_name = verify_data[0], verify_data[1]
    orig = img_data
    data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)

    model_out = model.predict([data])[0]
    if np.argmax(model_out) == 0: str_label = 'Healthy'
    elif np.argmax(model_out) == 1: str_label = 'Bacterial'
    elif np.argmax(model_out) == 2: str_label = 'Viral'
    elif np.argmax(model_out) == 3: str_label = 'Late blight'

    if str_label =='Healthy': status = 'Healthy'
    else: status = 'Unhealthy'
    print(status)
    # result = 'Status: ' + status + '.'
    result = ''

    if (str_label != 'Healthy'): result = '\nDisease: ' + str_label + '.'


    credentials = service_account.Credentials.from_service_account_file('./posts/apikey.json')
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)
    file_name = filepath
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    print(labels)
    leaf_identify=''
    leaf_condition=''
    for label in labels:
        if label.description == 'leaf':
            leaf_identify = 'It is a leaf'
            break

    if leaf_identify != 'It is a leaf':
        leaf_identify = 'It seems not a leaf picture, If you want to challenge me, COME ON ^_^'
        context = {
            "leaf_indentify": leaf_identify,
            "instance": instance,
        }
        return render(request, "re_notleaf.html", context)
    tips = 'It is an Unhealthy leaf, but I can not identify its possible disease, Please try another image with different angle of view'
    if leaf_identify == 'It is a leaf':
        for i in labels:
            if i.description == 'plant pathology':
                leaf_condition = 'Status : Unhealthy'
                break
        if leaf_condition == 'Status : Unhealthy' and status == 'Healthy':
            print('a')
            context = {
                "leaf_indentify": leaf_identify,
                "instance": instance,
                "leaf_condition": leaf_condition,
                "tips": tips,
            }
            return render(request, "re_Unidentify.html", context)
        elif leaf_condition == 'Status : Unhealthy' and status == 'Unhealthy':
            print('b')
            context = {
                "leaf_indentify": leaf_identify,
                "instance": instance,
                "leaf_condition":leaf_condition,
                "result": result,
            }
            if str_label == "Bacterial":
                return render(request, "re_bacteria.html", context)
            if str_label == "Viral":
                return render(request, "re_viral.html", context)
            if str_label == "Late blight":
                return render(request, "re_lateblight.html", context)
        elif leaf_condition != 'Status : Unhealthy' and status == 'Unhealthy':
            print('c')
            text = "It seems a healthy leaf's picture"
            context = {
                "leaf_indentify": leaf_identify,
                "instance": instance,
                "text":text,
                "leaf_condition":leaf_condition
            }
            return render(request, "re_healthleaf.html", context)
        elif leaf_condition != 'Status : Unhealthy' and status == 'Healthy':
            print('d')
            context = {
                "leaf_indentify": leaf_identify,
                "instance": instance,
                "leaf_condition":leaf_condition
            }
            return render(request, "re_healthleaf.html", context)



# @login_required(login_url='/login/')
def post_create2(request):
    form = PostForm(request.POST or None,request.FILES or None)
    try:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,"successfully upload")
            return HttpResponseRedirect(instance.get_absolute_url_QR())
    except():
        return render(request, 'forms2.html', {
                     "form": form,
                     'error_message': "You did not select a chioce."})
    context = {
        "form": form
    }
    return render(request, "forms2.html", context)


# @login_required(login_url='/login/')
def post_detail2(request, id=None):
    instance = get_object_or_404(Post, id=id)
    if (request.GET.get('mybtn1')):
        return HttpResponseRedirect(instance.get_absolute_url_QRresult())
    context = {
        "title": "Detail",
        "instance": instance
    }
    return render(request, "QR.html", context)


# @login_required(login_url='/login/')
def share(request,id=None):
    instance = get_object_or_404(Post, id=id)
    filepath = instance.image.url
    filepath = '.' + filepath
    print(filepath)
    words = "gardenpests.tk"
    version, level, qr_name = myqr.run(
        words,
        version=3,
        level='H',
        picture=filepath,
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name='lu'+filepath[8:-3]+'png',
        save_dir="./posts/static/img"
    )
    path='/static/img/lu' + filepath[8:-3] + 'png'
    print(path)
    context = {
        'path':path
    }
    return render(request, "QRresult.html", context)


# @login_required(login_url='/login/')
def map(request):
    html = TemplateResponse(request, 'treemap.html')
    return HttpResponse(html.render())


# @login_required(login_url='/login/')
def pic_solution(request):
    context = {}
    return render(request, '', context)