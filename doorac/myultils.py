import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S',
                   )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split('.')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def door_open_request():
    mydata = {'control':'OPEN'}
    try:
        myreq = requests.post('http://192.168.0.11:8080/protect/cgi/opendoor.cgi', mydata)
    except requests.exceptions.RequestException as e:
        logging.debug(e)
        return 400
    return myreq.status_code

