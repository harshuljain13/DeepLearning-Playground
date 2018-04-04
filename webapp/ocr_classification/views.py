from . import tasks
import json
from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.

def index(request):
    '''
    On GET request it simply loads the index.html
    on POST request it adds the fft_random task to the celery queue and sends the task id to the html page.
    html page then sends the ajax request to the url to get the status
    '''
    if request.method=='POST':
        try:
            image_file = request.FILES['file']
            image_file_name = image_file.name
        except:
            image_file_name = request.POST['img_upload'].split('/')[-1]
            print('Image file is :',image_file_name)
            image_file = open((static('ocr_classification/images/' + image_file_name))[1:])
        fs = FileSystemStorage()
        file_ = fs.save(image_file_name, image_file)
        print 'Input File is :', file_
        task = tasks.predict_char.delay(file_)
        #task = tasks.fft_random.delay(1000) # changes required
        return render(request, template_name='ocr_classification/index.html',
         context={'task_id': task.id, 'filename':file_})
    if request.method=='GET':
        return render(request, template_name='ocr_classification/index.html')

def poll_state(request):
    '''
    Gets the status of the task from tasks.get_task_status and returns to the ajax query
    '''
    status_data='Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            status_data = tasks.get_task_status(task_id)
        else:
            status_data = 'No task_id in the request'
    else:
        status_data = 'This is not ajax request'

    json_data = json.dumps(status_data)
    return HttpResponse(json_data, content_type='application/json')