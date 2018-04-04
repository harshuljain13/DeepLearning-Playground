import time
import os
import random
import ocr_classification
import numpy as np
from scipy.fftpack import fft
from celery.decorators import task
from celery import current_task, shared_task, result
from django.conf import settings
import cv2
img_size = 128

@shared_task
def fft_random(n):
    """
    Brainless number crunching just to have a substantial task:
    """
    for i in range(n):
        x = np.random.normal(0, 0.1, 2000)
        y = fft(x)
        if(i%10 == 0):
            process_percent = int(100 * float(i) / float(n))
            fft_random.update_state(state='PROGRESS',
                    meta={'process_percent': process_percent})
    return random.random()

@task
def predict_char(file_name):
    current_task.update_state(state='PROGRESS', meta={'process_percent':0})
    media_root = settings.MEDIA_ROOT
    current_task.update_state(state='PROGRESS', meta={'process_percent':2})
    full_file_path = os.path.join(media_root, file_name)
    image_np = cv2.imread(full_file_path)
    current_task.update_state(state='PROGRESS', meta={'process_percent':10})
    image_np = cv2.resize(image_np, (img_size, img_size), interpolation = cv2.INTER_AREA)
    current_task.update_state(state='PROGRESS', meta={'process_percent':70})
    char_= ocr_classification.get_predictions(image_np)
    return 'The Character is: ' + char_

def get_task_status(task_id):
    # If you have a task_id, this is how you query that task
    task = predict_breed.AsyncResult(task_id)
    status = task.status
    if status == 'SUCCESS':
        result = task.result
        # result_data holds the data for the prediction
        result_data = result
        process_percent = 100
        return {'status':status, 'process_percent':process_percent, 'result_data':result_data}
    if status == 'PROGRESS':
        process_percent = task.info['process_percent']
        return {'status':status, 'process_percent':process_percent}