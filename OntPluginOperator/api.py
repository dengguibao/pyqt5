import requests


class Api:

    def __init__(self):
        self.s = requests.session()
        # self.url = 'http://10.229.17.4:8080'
        self.url = 'http://127.0.0.1:8080'
        self.username = "hn_qinshiquan"
        self.__token = None
        self.__login_data = None

        self.s.headers.update({
            'Host': '%s' % self.url[7:],
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) \
                            AppleWebKit/537.36(KHTML, like Gecko) Chrome/84.0.4147.135 \
                            Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': '%s' % self.url,
            'Sec-Fetch-Site': 'same - origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': '%s/dhmp/index.html' % self.url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en - US, en;q = 0.9'
        })

    def user_login(self):
        """
        user login
        :return: api server return json data
        """
        post_url = '%s/dhmp/login/submit' % self.url
        post_data = {
            "userName": "686E5F71696E7368697175616E",
            "passWord": "524D5340313233343536",
            "loginId": False,
            "token": False,
            "loginName": "",
            "tickID": "",
            "strTic": ""
        }
        res = self.s.post(post_url, json=post_data)
        if res.status_code == 200:
            self.__login_data = res.json()
            return self.__login_data['message']
        else:
            return

    def build_token(self):
        """
        build query token
        :return:
        """
        if not self.__login_data:
            return
        else:
            self.__login_data['userName'] = self.username
            self.__login_data['sysConfigure'] = '{%22isDesensitization%22:false}'

        self.__token = 'sidebarStatus=0; token={token}; \
        loginId={loginId}; \
        userName={userName}; \
        sysConfigure={sysConfigure}; \
        sidebarStatus=0'.format(**self.__login_data)

        self.s.headers.update({
            'Cookie': self.__token
        })

    def query_dev_list(self, sn):
        if not sn or not self.__token:
            return

        post_url = '%s/dhmp/equipment/queryList' % self.url

        post_data = {
            "devType": "",
            "simpleQuery": False,
            "fromWorkFlow": False,
            "queryType": "0",
            "queryValue": sn,
            "infoType": 1,
            "advancedQuery": False,
            "page": {
                "pageSize": 10,
                "totalSize": 0,
                "currentPageNo": 1,
                "data": []
            },
            "loginId": self.__login_data['loginId'],
            "token": self.__login_data['token'],
            "loginName": self.__login_data['userName'],
            "tickID": "",
            "strTic": "",
            "logicID": "",
            "devSNo": "",
            "devPPPoE": "",
            "regionAreaId": "0",
            "devVendorName": "",
            "devVendorOUI": "",
            "devTypeName": "",
            "devHardVersion": "",
            "typeAndVerName": "",
            "devStatus": "",
            "devIp": "",
            "devRegStatus": "",
            "devOnline": "",
            "clientName": "",
            "onServiceOperation": "",
            "sustainOperation": ""
        }

        res = self.s.post(post_url, json=post_data)
        if res.status_code == 200:
            return res.json()
        else:
            return

    def query_plugin_list(self, mac):
        if not mac or not self.__token:
            return

        post_url = '%s/dhmp/equipmentOperation/getNotifyPluginList' % self.url

        post_data = {
            "devId": "",
            "devSnoCom": "",
            "mac": mac,
            "pluginId": "",
            "pluginName": "",
            "versionTo": "",
            "enable": "",
            "loginId": self.__login_data['loginId'],
            "token": self.__login_data['token'],
            "loginName": self.__login_data['userName'],
            "tickID": "",
            "strTic": ""
        }

        res = self.s.post(post_url, json=post_data)
        if res.status_code == 200:
            return res.json()
        else:
            return

    def check_plugin_exist(self, args):
        if not args or not self.__token:
            return

        post_url = '%s/dhmp/equipmentOperation/checkPluginExist' % self.url

        post_data = {
            "devId": args['devId'],
            "devSnoCom": args['sn'],
            "mac": args['mac'],
            "pluginId": "",
            "pluginName": args['pluginName'],
            "versionTo": args['pluginVersion'],
            "enable": "",
            "loginId": self.__login_data['loginId'],
            "token": self.__login_data['token'],
            "loginName": self.__login_data['userName'],
            "tickID": "",
            "strTic": ""
        }

        res = self.s.post(post_url, json=post_data)
        if res.status_code == 200:
            return res.json()
        else:
            return

    def plugin_opt(self, args, url_arg):
        if not args or not self.__token:
            return

        post_url = '%s/dhmp/equipmentOperation/plugin%s' % (self.url, url_arg)

        post_data = {
            "devId": args['devId'],
            "devSnoCom": args['sn'],
            "mac": args['mac'],
            "pluginId": args['pluginId'],
            "pluginName": args['pluginName'],
            "versionTo": args['pluginVersion'],
            "enable": "",
            "loginId": self.__login_data['loginId'],
            "token": self.__login_data['token'],
            "loginName": self.__login_data['userName'],
            "tickID": "",
            "strTic": ""
        }

        res = self.s.post(post_url, json=post_data)
        if res.status_code == 200:
            return res.json()
        else:
            return

    def plugin_uninstall(self, args):
        return self.plugin_opt(args, 'UnInstall')

    def plugin_install(self, args):
        return self.plugin_opt(args, 'Install')
