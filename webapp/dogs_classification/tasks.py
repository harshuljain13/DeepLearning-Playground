import time
import os
import random
from scipy.fftpack import fft
import numpy as np
from celery.decorators import task
from celery import current_task, shared_task, result

@task
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

def get_task_status(task_id):
    # If you have a task_id, this is how you query that task
    task = fft_random.AsyncResult(task_id)
    status = task.status
    if status == 'SUCCESS':
        result = task.result
        # result_data holds the data for the prediction
        result_data = "result.split(',')"
        process_percent = 100
        return {'status':status, 'process_percent':process_percent, 'result_data':result_data}
    if status == 'PROGRESS':
        process_percent = task.info['process_percent']
        return {'status':status, 'process_percent':process_percent}