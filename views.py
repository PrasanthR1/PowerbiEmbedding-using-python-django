from django.shortcuts import render,redirect
# import adal
import json
import requests
import logging


def get_token(request):
    data = {
        'grant_type': 'password',
        'scope': 'openid',
        'resource': r'https://analysis.windows.net/powerbi/api',
        'client_id': '{client id from auzre reg app}',
        'username': '{your powerbi acc}',
        'password': '{powerbi acc password}'
    }
    response = requests.post('https://login.microsoftonline.com/common/oauth2/token', data=data)
    print(response)
    access_token = response.json().get('access_token')
    print(access_token)

    headers = {'Authorization': 'Bearer ' + access_token}
    res = requests.get('https://api.powerbi.com/v1.0/myorg/groups', headers=headers)
    bi_groups = json.loads(res.text)['value']

    d = {
        'WORKSPACE_NAME': 'your_workspace_name',
    }

    group_id = ""
    if d['WORKSPACE_NAME']:
        for gid in bi_groups:
            if gid['name'] == d['WORKSPACE_NAME']:
                group_id = gid['id']

    if group_id == "":
        logging.log.warn("Workspace name is set but there is no such workspace: " + d["WORKSPACE_NAME"])
        group_id = bi_groups[0]['id']

    response = requests.get('https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports', headers=headers)
    bi_reports = json.loads(response.text)['value']

    reportId = embedUrl = ""
    rep = []
    for rid in bi_reports:
        reportId = rid['id']
        embedUrl = rid['embedUrl']

        if reportId == "":
            logging.log.warn("Report name is set but there is no such report: " + d["REPORT_NAME"])
            reportId = bi_reports[0]['id']
            embedUrl = bi_reports[0]['embedUrl']

        post_data = post_data = \
            """
                {
                    "accessLevel": "View"
                }
            """

        headers.update({'Content-type': 'application/json'})

        response = requests.post('https://api.powerbi.com/v1.0/myorg/groups/' + group_id + \
                                 '/reports/' + reportId + '/GenerateToken', data=post_data, headers=headers)
        print(json.loads(response.text))
        report_token = json.loads(response.text)['token']

        j = '{{\
                "embedToken": "{:s}",\
                "embedUrl": "{:s}",\
                "reportId": "{:s}"\
            }}'.format(report_token, embedUrl, reportId)
        json_data = json.loads(j)
        rep.append(json_data)

    return render(request, 'index.html', {'json_data': rep})
