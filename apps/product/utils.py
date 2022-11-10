from datetime import datetime

def get_time():
    format = '%Y_%m_%d_%M_%s'
    return datetime.now().strftime(format)