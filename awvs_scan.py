#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import json,time
import requests
import requests.packages.urllib3
'''
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
 
or 
 
pip install requests[security]
'''
requests.packages.urllib3.disable_warnings()
 
tarurl = "https://192.168.51.202:3443/"
apikey="1986ad8c0a5b3df4d7028d5f3c06e936c2a31232e73cf4735aff3c9d8f03da061"
headers = {"X-Auth":apikey,"content-type": "application/json"}
 
def addtask(url):
    #添加任务
    data = {"address":url,"description":url,"criticality":"10"}
    try:
        response = requests.post(tarurl+"/api/v1/targets",data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        return result['target_id']
    except Exception as e:
        print(str(e))
        return
 
def startscan(url):
    # 先获取全部的任务.避免重复
    # 添加任务获取target_id
    # 开始扫描
    targets = getscan()
    if url in targets:
        return "repeat"
    else:
        target_id = addtask(url)
        data = {"target_id":target_id,"profile_id":"11111111-1111-1111-1111-111111111111","schedule": {"disable": False,"start_date":None,"time_sensitive": False}}
        try:
            response = requests.post(tarurl+"/api/v1/scans",data=json.dumps(data),headers=headers,timeout=30,verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(str(e))
            return
 
def getstatus(scan_id):
    # 获取scan_id的扫描状况
    try:
        response = requests.get(tarurl+"/api/v1/scans/"+str(scan_id),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        status = result['current_session']['status']
        #如果是completed 表示结束.可以生成报告
        if status == "completed":
            return getreports(scan_id)
        else:
            return result['current_session']['status']
    except Exception as e:
        print(str(e))
        return
 
def getreports(scan_id):
    # 获取scan_id的扫描报告
    data = {"template_id":"11111111-1111-1111-1111-111111111111","source":{"list_type":"scans","id_list":[scan_id]}}
    try:
        response = requests.post(tarurl+"/api/v1/reports",data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = response.headers
        report = result['Location'].replace('/api/v1/reports/','/reports/download/')
        return tarurl.rstrip('/')+report
    except Exception as e:
        print(str(e))
        return
 
def getscan():
    #获取全部的扫描状态
    targets = []
    try:
        response = requests.get(tarurl+"/api/v1/scans",headers=headers,timeout=30,verify=False)
        results = json.loads(response.content)
        for result in results['scans']:
            targets.append(result['target']['address'])
            print result['scan_id'],result['target']['address'],getstatus(result['scan_id'])#,result['target_id']
        return list(set(targets))
    except Exception as e:
        raise e
 
if __name__ == '__main__':
    with open("url.txt") as f:
        for url in f.readlines():
            url=url.strip()
            print url
            startscan(url)
            
            
         
     
            
    
