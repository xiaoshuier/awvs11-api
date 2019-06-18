#!/usr/bin/env python
# coding:utf-8

#-*-Thinking-*-

#coding=utf8

from burp import IBurpExtender

from burp import IHttpListener

from burp import IHttpRequestResponse

from burp import IResponseInfo

from burp import IRequestInfo

from burp import IHttpService

import re
import urllib2,urllib
from urlparse import urlparse

topRootDomain = (
        '.com', '.la', '.io', '.co', '.info', '.net', '.org', '.me', '.mobi',
        '.us', '.biz', '.xxx', '.ca', '.co.jp', '.com.cn', '.net.cn',
        '.org.cn', '.mx', '.tv', '.ws', '.ag', '.com.ag', '.net.ag',
        '.org.ag', '.am', '.asia', '.at', '.be', '.com.br', '.net.br',
        '.bz', '.com.bz', '.net.bz', '.cc', '.com.co', '.net.co',
        '.nom.co', '.de', '.es', '.com.es', '.nom.es', '.org.es',
        '.eu', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in', '.gen.in',
        '.ind.in', '.net.in', '.org.in', '.it', '.jobs', '.jp', '.ms',
        '.com.mx', '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz',
        '.se', '.tc', '.tk', '.tw', '.com.tw', '.idv.tw', '.org.tw',
        '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg', ".com.hk")

def get_domain_root(url):
    domain_root = ""
    try:
        ## 若不是 http或https开头，则补上方便正则匹配规则
        if len(url.split("://")) <= 1 and url[0:4] != "http" and url[0:5] != "https":
            url = "http://" + url

        reg = r'[^\.]+(' + '|'.join([h.replace('.', r'\.') for h in topRootDomain]) + ')$'
        pattern = re.compile(reg, re.IGNORECASE)

        parts = urlparse(url)
        #print(parts)
        host = parts.netloc
        m = pattern.search(host)
        res = m.group() if m else host
        domain_root = "-" if not res else res
    except Exception, ex:
        print("get_domain_root() -- error_msg: " , ex)
    return domain_root


print 'Thinking\'s find sqli  Bui~'
class BurpExtender(IBurpExtender, IHttpListener):
   def registerExtenderCallbacks(self, callbacks):
       self._callbacks = callbacks
       self._helpers = callbacks.getHelpers()
       self._callbacks.setExtensionName("find sqli")
       callbacks.registerHttpListener(self)

   def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
       if toolFlag == 64 or toolFlag == 16 or toolFlag == 8 or toolFlag == 4: #if tool is Proxy Tab or repeater
           if not messageIsRequest:#only handle responses
               #获取服务信息
               httpService = messageInfo.getHttpService()
               port = httpService.getPort()
               host = httpService.getHost()
               domain=get_domain_root(host) #匹配跟域名
               if self.black_domain(domain):
                   # 获取请求包的数据
                   resquest = messageInfo.getRequest()
                   analyzedRequest = self._helpers.analyzeResponse(resquest)
                   request_header = analyzedRequest.getHeaders()
                   #print request_header
                   request_bodys = resquest[analyzedRequest.getBodyOffset():].tostring()
                   #print request_bodys
                   # 获取响应包的数据
                   response = messageInfo.getResponse()
                   analyzedResponse = self._helpers.analyzeResponse(response)
                   response_headers = analyzedResponse.getHeaders()
                   response_bodys = response[analyzedResponse.getBodyOffset():].tostring()
                   response_StatusCode = analyzedResponse.getStatusCode()

                   #重新发送请求包
                   palyload_list=["' or sleep(5) and '1'='1",
                                  '" or sleep(5) and "1"="1',
                                  ') or sleep(5) and (',
                                  '+or sleep(5)#--+-']
                   print(request_header[0])

                   if request_header[0].startswith(u'GET'):
                       all_parms=request_header[0].split(u' ')[1]
                       if all_parms.find("?")>0:
                           try:
                               parms=all_parms.split('?')[1]
                               if parms>0:
                                   parm=parms.split('&')
                                   for i in parm:
                                       for payload in palyload_list:
                                           key=i[:-1]+payload
                                           print(key)
                           except Exception as e:
                               print e

                       else:
                           pass

                   if request_header[0].startswith(u'POST'):
                       all_get_parms = request_header[0].split(u' ')[1]
                       try:
                           all_get_parms.index("?")
                           parms = all_get_parms.split('?')[1]
                           if parms>0:
                               parm = parms.split('&')
                               for i in parm:
                                   for payload in palyload_list:
                                       key = i[:-1] + payload
                                       print key
                           else:
                               parm=request_bodys.split('&')
                               for i in parm:
                                   for payload in palyload_list:
                                       key = i[:-1] + payload
                                       print(key)
                       except ValueError as e:
                           parm = request_bodys.split('&')
                           for i in parm:
                               for payload in palyload_list:
                                   key = i[:-1] + payload
                                   print(key)


                   #if request_header[0][:-1]:
                       #print(request_header[0][:-1])
                   #new_headers[0] = new_headers[0][:-9] + '?callback=BuiBui'
                   #request_new = self._helpers.buildHttpMessage(new_headers, request_bodys)
                   #reponse_new = self._callbacks.makeHttpRequest(host, port, ishttps, req)

                   #新的请求请求包
                   #analyzedreq = self._helpers.analyzeResponse(rep)
                   #req_headers = analyzedreq.getHeaders()
                   #req_bodys = rep[analyzedreq.getBodyOffset():].tostring()

                   #新的请求响应包
                   #analyzedrep = self._helpers.analyzeResponse(rep)
                  # rep_headers = analyzedrep.getHeaders()
                   #rep_bodys = rep[analyzedrep.getBodyOffset():].tostring()


               else :
                   return





   def black_domain(self,url):
        black_domain=['google.com','whatruns.com','shodan.io','cnzz.com','gravatar.com','gstatic.com']
        try:
            if black_domain.index(url):
                return False
        except ValueError as e:
            return True





               #第一种情况：url中带有callback,且返回的是json数据。

               # expressionA = r'.*(callback).*'
               #
               # expressionB = r'.*(application/json|application/javascript).*'
               #
               # expressionC = r'.*(text/html|application/javascript).*'
               #
               # for rqheader in request_header:
               #
               #     if rqheader.startswith("Host"):
               #
               #         rqhost = rqheader
               #
               #         break
               #
               # ishtml = 0
               #
               # for rpheader in response_headers:
               #
               #     if rpheader.startswith("Content-Type:")  and re.match(expressionC,rpheader):
               #
               #         ishtml = 1
               #
               #     if rpheader.startswith("Content-Type:")  and  re.match(expressionB,rpheader):
               #
               #         if re.match(expressionA,request_header[0]):
               #
               #             print '='*10,'[success|有callback且返回json数据]','='*10,'\n\n[Host]',rqhost,port,'\n\n[URI]',request_header[0],'\n\n[ResponseBody]',response_bodys[0:30],'\n\n\n'
               #
               #             break
               #
               # #第二种情况：url中没有带callback,但是通过添加callback参数后，便返回了带方法名的json数据。
               #
               # if not re.match(expressionA,request_header[0]):
               #
               #     new_headers = request_header
               #
               #     if '?' in new_headers[0]:
               #
               #         new_headers[0] = new_headers[0].replace('?','?callback=BuiBui&')
               #
               #     else:
               #
               #         new_headers[0] = new_headers[0][:-9] +'?callback=BuiBui'
               #
               #     req = self._helpers.buildHttpMessage(new_headers, request_bodys)
               #
               #     ishttps = False
               #
               #     if port == 443:
               #
               #         ishttps = True
               #
               #     if response_StatusCode == 200 and ishtml == 1:
               #
               #         rep = self._callbacks.makeHttpRequest(host, port, ishttps, req)
               #
               #         #TODO 在某些情况下makeHttpRequest时候会出现一些bug,得到的结果但是取不到response,很奇怪(已经解决,404页面取不到正文返回包)
               #
               #         #新的请求请求包
               #
               #         analyzedreq = self._helpers.analyzeResponse(rep)
               #
               #         req_headers = analyzedreq.getHeaders()
               #
               #         req_bodys = rep[analyzedreq.getBodyOffset():].tostring()
               #
               #         #新的请求响应包
               #
               #         analyzedrep = self._helpers.analyzeResponse(rep)
               #
               #         rep_headers = analyzedrep.getHeaders()
               #
               #         rep_bodys = rep[analyzedrep.getBodyOffset():].tostring()
               #
               #         if 'BuiBui' in rep_bodys:
               #
               #             for repheader in rep_headers:
               #
               #                 if repheader.startswith("Content-Type:")  and  re.match(expressionB,repheader):
               #
               #                     print '='*10,'[success|发现隐藏callback且返回json数据]','='*10,'\n\n[Host]',rqhost,port,'\n\n[URI]',req_headers[0],'\n\n[ResponseBody]',rep_bodys[0:30],'\n\n\n'
               #
               #                     break