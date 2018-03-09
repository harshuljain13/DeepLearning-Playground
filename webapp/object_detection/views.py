import tasks
import json
from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
# Create your views here.

def index(request):
    '''
    On GET request it simply loads the index.html
    on POST request it adds the fft_random task to the celery queue and sends the task id to the html page.
    html page then sends the ajax request to the url to get the status
    '''
    if request.method=='POST':
        #image_file = request.FILES['image_file']
        #image_file_name = image_file.name
        #fs = FileSystemStorage()
        #full_path_image_file = fs.save(image_file_name, image_file)
        task = tasks.fft_random.delay(10000) # changes required
        return render(request, template_name='object_detection/index.html', context={'task_id': task.id })
    if request.method=='GET':
        return render(request, template_name='object_detection/index.html')

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
    print json_data
    return HttpResponse(json_data, content_type='application/json')