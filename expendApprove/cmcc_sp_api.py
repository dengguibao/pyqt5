import os
import requests
import base64
import time
import datetime


class ReadConfig:

    def __init__(self,config_file=None):
        self.config_file = 'config.conf'
        if config_file:
            self.config_file=config_file

    def get_user_and_pwd(self):
        if not os.path.exists(self.config_file):
            return None

        with(open(self.config_file, 'r', encoding='utf-8')) as f:
            content = f.read()

        user = pwd = None
        for line in content.split('\n'):
            if line.strip()[0:1] == '#' or line == '':
                continue
            if 'username=' in line:
                user = line.split('=')[1].strip()
            if 'password=' in line:
                pwd = line.split('=')[1].strip()
            if user and pwd:
                return user, pwd

        return None


class Api:
    response = None
    error = None

    session = requests.session()
    domain = 'http://183.215.181.246:7000'
    headers = {
        'Host': '183.215.181.246:7000',
        # 'Content-Type': 'application/json',
        #'Origin': 'file://',
        'Connection': 'keep-alive',
        'Accept': 'application/json,text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://183.215.181.246:7000/irms/login.ilf'
    }
    proxies = {
        # 'http': 'http://172.31.10.84:2345',
        # 'https': 'http://172.31.10.84:2345'
    }

    def __init__(self, proxies=None):
        self.session.headers.update(self.headers)
        if proxies:
            self.session.proxies = self.proxies

    def login(self, user, pwd):
        url = '%s/irms/CtrlUser.action'
        cookie = self.get_cookie_session()
        if not cookie:
            self.error = 'not found session cookie'
            return None
        self.headers['Cookie'] = cookie
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Origin'] = '%s' % self.domain
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.session.headers.update(self.headers)

        post_data = {
            'action': 'login',
            'surl': 'jsp/home/main.jsp',
            'furl': 'jsp/login.jsp',
            'enCodePwd': base64.b64encode(user),
            'enCodeAcc': base64.b64encode(pwd),
            'useraccount': user,
            'password': pwd,
        }
        res = self.session.post(url, json=post_data)
        if res.status_code in (200, 302):
            return res.content
        else:
            self.error = 'login failed,response status code is %s' % res.status_code
        return None

    def query_order(self, order_no):
        fmt = '%Y-%m-%d %H:%M:%S'
        now_time = time.strftime(fmt, time.localtime())
        yes_dt = datetime.datetime.now()-datetime.timedelta(days=1)
        yes_time = yes_dt.strftime(fmt)

        url = '%s/irms/cmtTasklistAction!waitedTaskAJAX.ilf' % self.domain
        self.headers['Referer'] = '%s/irms/cmtTasklistAction!waitedTask.ilf?template_type=9&PageStyle=1' % self.domain
        self.headers['Accept'] = 'text/html,application/xhtml+xml,*/*'
        self.session.headers.update(self.headers)

        post_data = {
            'start': 0,
            'limit': 50,
            'template_type': 9,
            'template_display_name': '',
            'PageStyle': 1,
            'psform_no': '',
            'processEnName': '',
            'orderType': '',
            'startTime': yes_time,
            'endTime': now_time,
            'form_no': order_no,
            'queryflag': 'true',
            'processinstname': '',
            'formType': '',
            'formModel': '',
            'userid': ''
        }

        res = self.session.post(url, json=post_data)
        if res.status_code == 200:
            return res.json()
        else:
            self.error = 'query order failed, order_no:%s' % order_no
        return None

    def submit(self, order_data):
        url = '%s/irms/cellIncreaseV2ZyzzqrAction!submit.ilf' % self.domain
        self.headers['Referer'] = '%s/irms/wfCommonAction!taskMain.ilf' % self.domain
        self.session.headers(self.headers)
        now_dt = datetime.datetime.now()
        accept_dt = now_dt+datetime.timedelta(days=2)
        reply_dt = now_dt+datetime.timedelta(days=4)
        krkj_end_dt = now_dt + datetime.timedelta(days=180)

        fmt = '%Y-%m-%d %H:%M:%S'

        post_data = {
            'activeName': order_data['ACTIVITYDEFID'],
            'flowId': order_data['FLOW_ID'],
            'processDefName': order_data['PROCESSDEFNAME'],
            'workitemId': order_data['WORKITEMID'],
            'noNeedKREdTime': krkj_end_dt.strftime(fmt),
            'ckjg': 'endWF',
            'remark': '',
            'finalDealTime': '',
            'replyTime': reply_dt.strftime(fmt),
            'acceptTime': accept_dt.strftime(fmt),
            'dealTime': now_dt.strftime(fmt),
            'deptName': '家客流程',
            'cellPhone': '18874729377',
            'currentAcceptTime': order_data['ACCEPT_TIME'],
            'currentLimitTime': order_data['LIMIT_TIME'],
            'froPerPlat': '',
            'handleManRole': '',
            'companyName': order_data['COMPANYNAME'],
            'companyId': order_data['SEND_COMPANYID'],
            'deptId': '2742',
            'ownerId': order_data['PARTICIPANTID'],
            'formUrl': 'cellIncreaseV2ZyzzqrAction',
            'version': order_data['VERSION'],
            'toppid': order_data['TOPPROCESSINSTID'],
            'currentstate': order_data['CURRENT_STATE'],
            'formInfoId': order_data['FLOW_NO'],
            'title':  order_data['PROCESSINSTNAME'],
            'formNo': order_data['FLOW_NO'],
            'activeId': order_data['ACTIVITYINSTID'],
            'pid': order_data['PROCESSINSTID'],
            'activeDescribe': order_data['ACTIVITYINSTNAME'],
            'ownerName': order_data['PARTICIPANTNAME']
        }
        res = self.session.post(url, json=post_data)
        if res.status_code in (302, 200):
            print(res.content)
            return 0, 1
        else:
            return 1, 'submit failed order_no:%s' % order_data['FLOW_ID']

    def get_cookie_session(self):
        url = '%s/irms/jsp/login.jsp' % self.domain
        response = self.session.get(url)
        if response.status_code == 200:
            return response.headers['Set-Cookie'].split(';')[0]
        else:
            self.error = 'open login page failed,url:' % url
        return None

    # def start(self, user, pwd, order_no):
    #     self.login(user, pwd)
    #     order_data = self.query_order(order_no)
    #     if order_data['totalCount'] > 0:
    #         self.submit(order_data['root'][0])
