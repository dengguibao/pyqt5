import requests
import os
import time


class Api:
    """
    china mobile AND ops krkj Service api
    """
    response = None
    error = None
    debug = False

    session = requests.session()
    domain = 'http://183.215.60.23:7021'
    pic_file_name = 'data.jpg'
    headers = {
        'Host': '183.215.60.23:7021',
        # 'Content-Type': 'application/json',
        'Origin': 'file://',
        'Connection': 'keep-alive',
        'Accept': 'application/json,text/plain, */*',
        'User-Agent': 'Mozilla / 5.0(iPhone; CPU iPhone OS 13_4_1 like Mac OS X) \
            AppleWebKit / 605.1.15(KHTML, like Gecko) Mobile / 15E148',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate'
    }
    proxies = {
        # 'http': 'http://172.31.10.84:2345',
        # 'https': 'http://172.31.10.84:2345'
    }

    def __init__(self, pic_file_name=None):
        self.session.headers.update(self.headers)
        if self.proxies:
            self.session.proxies = self.proxies
        if pic_file_name:
            self.pic_file_name

    def get_userinfo_by_username(self, username):
        # return json
        # {
        #     "msg": "操作成功",
        #     "data": {
        #         "userId": "2210157",
        #         "empId": "259773",
        #         "userDept": null,
        #         "userName": "姜何",
        #         "resultCode": null,
        #         "userMobile": "15111421990",
        #         "userAccount": "csdw_jianghe",
        #         "resultDesc": null,
        #         "userCompany": null
        #     },
        #     "code": 0
        # }
        post_data = {
            'account': username
        }
        url = '%s/appirms/krkjService/krkj/userInfo.ilf' % self.domain
        self.response = self.session.post(
            url,
            json=post_data
        )
        return self.get_response_data()

    def get_task_list_by_area_name(self, area_name, empid):
        # return json
        # {
        #     "code": 0,
        #     "data": [
        #         {
        #             "id": 9459796,
        #             "sendMan": "系统自动处理",
        #             "version": "1.1.1",
        #             "activityinstname": "现场查勘",
        #             "flowId": 51590805676825,
        #             "sendManMobile": "11111111111",
        #             "workitemId": 24279615,
        #             "processinstname": "宁乡县资福七星村_长沙宁乡县资福乡七星村二期零58号杆旁\/GF09_分纤箱扩容_系统自动",
        #             "createTime": "2020\/05\/30 10:27",
        #             "processinstid": 6353760,
        #             "activityinstid": "41323388",
        #             "activitydefid": "xcck",
        #             "participantid": "259773",
        #             "flowNo": "HN1-16-200530-3029",
        #             "participantname": "姜何"
        #         },
        #         ...
        #     ],
        #     "totalPageNum": 6,
        #     "msg": "操作成功",
        #     "nextPage": true,
        #     "pageNum": 0
        # }
        post_data = {
            'theme': area_name,
            'partId': empid
        }
        url = '%s/appirms/krkjService/krkj/waitingTaskList.ilf' % self.domain
        self.response = self.session.post(
            url,
            json=post_data
        )
        return self.get_response_data()

    def upload_pic_to_server(self, empid, username, flowid, activitydefid):
        # {
        #     "msg": "操作成功",
        #     "data": {
        #         "flow_id": 51590808463380,
        #         "id": 7656339,
        #         "file_type": "pic",
        #         "file_path": "\/pic\/65f15f07-01fc-458d-b90b-654c862ea897.jpg",
        #         "file_size": "357214",
        #         "file_name": "f8c60d6d-e00d-40e0-ba3c-8526b8ae4c3e.jpg",
        #         "create_time": null,
        #         "creater_id": "259773",
        #         "creater_name": "姜何",
        #         "ht_name": "xcck"
        #     },
        #     "code": 0
        # }
        if not os.path.exists(self.pic_file_name):
            return None
        files = {
            'file': ('data.jpg', open(self.pic_file_name, 'rb'), 'image/jpeg')
        }
        post_data = {
            'fid': flowid,
            'htName': activitydefid,
            'uid': empid,
            'uname': username
        }
        url = '%s/appirms/krkjService/krkj/picInfoSubmit.ilf' % self.domain
        self.response = self.session.post(
            url,
            data=post_data,
            files=files
        )
        return self.get_response_data()

    def task_detail(self, flowid):
        # {
        #     "msg": "操作成功",
        #     "data": {
        #         "xlsg": null,
        #         "deptName": null,
        #         "workitemId": null,
        #         "replaceAction": null,
        #         "lastActHandleTime": "2020-05-30 03:14:23",
        #         "entrance": null,
        #         "id": 859854,
        #         "taskState": null,
        #         "kjHaveApplyed": null,
        #         "maintainManMobile": null,
        #         "toppid": null,
        #         "formUrl": null,
        #         "lastActName": "扩容扩建申请",
        #         "companyName": "长沙分公司",
        #         "isBack": null,
        #         "krkjcj": null,
        #         "activeName": null,
        #         "version": null,
        #         "flowId": 51590808463380,
        #         "acceptTime": null,
        #         "deptId": null,
        #         "prtFlowId": null,
        #         "parentHtName": null,
        #         "sfkykj": null,
        #         "remark": "系统自动",
        #         "dealPersons": null,
        #         "formInfoId": null,
        #         "startTime": "2020-05-30 11:14:23",
        #         "ownerName": "系统自动处理",
        #         "gdgdbh": null,
        #         "relationId": null,
        #         "resServiceIds": null,
        #         "activeDescribe": null,
        #         "lastActRemark": "发起工单",
        #         "countyId": null,
        #         "increaseProject": null,
        #         "lastActHandleMan": "系统自动处理",
        #         "increaseType": null,
        #         "processDefineId": null,
        #         "resIds": null,
        #         "companyId": 478,
        #         "resId": null,
        #         "replyTime": null,
        #         "dealTime": null,
        #         "krkjcjStr": null,
        #         "processDefName": null,
        #         "processinstDesc": null,
        #         "orderType": null,
        #         "activeInfoId": null,
        #         "sfkykjReason": null,
        #         "isShowAssign": null,
        #         "froPerPlat": null,
        #         "templateName": null,
        #         "activeId": null,
        #         "countyName": null,
        #         "currentstate": null,
        #         "formId": null,
        #         "setType": null,
        #         "viewForm": false,
        #         "flowTypeId": null,
        #         "formNo": "HN1-16-200530-6719",
        #         "endWF": null,
        #         "extend1": null,
        #         "kjReplyTime": null,
        #         "taskId": null,
        #         "zyqrjg": null,
        #         "zzgdh": null,
        #         "title": "宁乡县珊瑚村_长沙宁乡珊瑚村喻家亮旁\/GF11_分纤箱扩容_系统自动",
        #         "pid": 6357453,
        #         "currentAcceptTime": null,
        #         "ckjg": null,
        #         "customFormId": null,
        #         "currentLimitTime": null,
        #         "isCrm": null,
        #         "kjReplyResult": null,
        #         "state": 2,
        #         "sendType": null,
        #         "canSubmit": false,
        #         "handleManRole": null,
        #         "acceptEcho": null,
        #         "ownerId": 42484,
        #         "crmNo": null,
        #         "dealEmpIds": null,
        #         "sendId": null,
        #         "kxzxshjg": null,
        #         "cellPhone": null,
        #         "houseId": null,
        #         "maintainMan": null,
        #         "detailFrom": null
        #     },
        #     "code": 0
        # }
        post_data = {
            'flowId': flowid
        }
        url = '%s/appirms/krkjService/krkj/taskDetail.ilf' % self.domain
        self.response = self.session.post(
            url,
            json=post_data
        )
        return self.get_response_data()

    def task_submit(self, activitydefid, workitemId, ckjg, flowid, pid):
        # {
        #     "msg": "操作成功",
        #     "data": {
        #         "resultCode": "0",
        #         "resultDesc": "success"
        #     },
        #     "code": 0
        # }
        post_data = {
            'activeName': activitydefid,
            'workitemId': workitemId,
            'ckjg': ckjg,
            'flowId': flowid,
            'pid': pid,
            'remark': u'不需要扩建'
        }
        url = '%s/appirms/krkjService/krkj/taskSubmit.ilf' % self.domain
        self.response = self.session.post(
            url,
            json=post_data
        )
        return self.get_response_data()

    def get_response_data(self):
        print(self.response)
        if self.response is None:
            return None

        if self.debug:
            print(self.response.url, self.response.status_code, self.response.json())

        if self.response.status_code == 200:
            data = self.response.json()
        else:
            self.error = '%s error,status_code: %s' % (self.response.url, self.response.status_code)

        if self.response.status_code == 200 and data:
            self.response = None
            return data

        return None

    def start(self, area_name, username, delay=0, rdelay=0):
        data = {}
        userinfo = self.get_userinfo_by_username(username)
        if userinfo and userinfo['code'] == 0:
            data['empid'] = userinfo['data']['empId']
            data['userName'] = userinfo['data']['userName']
        else:
            return 1, 'error: get userinfo failed'

        task_list = self.get_task_list_by_area_name(area_name, data['empid'])

        completed_tasks = 0
        if task_list and task_list['code'] == 0 and len(task_list['data']) > 0:
            for i in task_list['data']:
                if delay+rdelay > 0:
                    time.sleep(delay+rdelay)
                data['workitemId'] = i['workitemId']
                data['flowId'] = i['flowId']
                data['activitydefid'] = i['activitydefid']
                data['flowNo'] = i['flowNo']
                data['pid'] = i['processinstid']
                data['ckjg'] = 'endWF'
                # upload picture
                pic_info = self.upload_pic_to_server(
                    data['empid'], data['userName'], data['flowId'], data['activitydefid']
                )
                # upload pic success
                if pic_info and pic_info['code'] == 0:
                    # submit order
                    submit_info = self.task_submit(
                        data['activitydefid'], data['workitemId'], data['ckjg'], data['flowId'], data['pid']
                    )
                    # submit order success
                    if submit_info and submit_info['code'] == 0:
                        completed_tasks += 1
                    else:
                        self.error = 'submit order failed, order id %s' % data['flowNo']
                else:
                    self.error = 'upload pic failed for order id %s' % data['flowNo']
            return 0, completed_tasks
        elif len(task_list['data']) == 0:
            return 0, completed_tasks
        else:
            return 1, 'error: get task list failed for username %s' % username

    def close(self):
        self.session.close()
