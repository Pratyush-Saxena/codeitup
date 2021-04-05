from django.shortcuts import render
import json,requests
import re
import urllib
CODE_EVALUATION_URL = u'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
CLIENT_SECRET = 'cf55078cf9ef83a79640d79aa24be9bb6e329417'

def execute(source,input_file,lang):
    callback = "https://client.com/callback/"

    data = {    
        'source': source,
        'lang': 'CPP11',
        'time_limit': 5,
        'memory_limit': 246323,
        'input': input_file,
        'callback' : callback,
        'id': "client-001"
    }
    headers = {"client-secret": CLIENT_SECRET}
    resp = requests.post(CODE_EVALUATION_URL, data=data, headers=headers)
    compile_resp = json.loads(resp.text)
    GET_STATUS_URL=compile_resp['status_update_url']
    resp_confirm=requests.get(GET_STATUS_URL, headers=headers)
    status_resp = json.loads(resp_confirm.text)
    while(status_resp['result']['run_status']['status']=='NA'):
        resp_confirm=requests.get(GET_STATUS_URL, headers=headers)
        status_resp = json.loads(resp_confirm.text)
        continue
    link=status_resp['result']['run_status']['output']
    if(link!=None):
        output_file=urllib.request.urlopen(link)
        my_output=""
        for line in output_file:
            my_output+=line.decode("utf-8")
    status=status_resp['result']['run_status']['status']
    status_detail=status_resp['result']['run_status']['status_detail']
    time_used=status_resp['result']['run_status']['time_used']
    memory_used=status_resp['result']['run_status']['memory_used']
    my_result={'output':my_output,'status':status,'status_detail':status_detail,'memory_used':memory_used,'time_used':time_used}
    return my_result

def index(requests):
    if requests.method=='POST':
        source_code=requests.FILES['source_code'].read()
        try:
            usr_input=requests.FILES['usr_input'].read()
            is_input=True
        except:
            is_input=False
        lang=requests.POST.get('lang')
        if not is_input:
            usr_input=None
        data=execute(source_code,usr_input,lang)
        if is_input:
            data['usr_input']=usr_input.decode("utf-8")
        else:
            data['usr_input']=None
        data['source_code']=source_code.decode("utf-8")

        return render(requests,'compiler/index.html',data)
    return render(requests,'compiler/index.html')
