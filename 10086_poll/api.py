import json
import urllib3
import requests
from evaluateResult import evaluateResult
urllib3.disable_warnings()


class Poll:
    proxies = {
        # 'http': 'http://172.31.10.84:2345',
        # 'https': 'http://172.31.10.84:2345'
    }

    req_headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01,',
        'Connection': 'Keep-Alive',
        'Host': 'eva.customer.10086.cn',
        'Origin': 'https://eva.customer.10086.cn',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/79.0.3945.130 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    s = None

    def __init__(self):
        s = requests.session()
        s.headers.update(self.req_headers)

        if not len(self.proxies):
            s.proxies = self.proxies
        self.s = s

    def submit_poll(self, url):
        r = self.s.get(url, verify=False)
        if '重复提交' in r.text:
            return '%s 链接已提交,请勿重复提交' % url
        if '请求超时' in r.text:
            return '%s 链接已失效超时' % url

        args = {}
        jump302_url = r.url
        if 'token' in jump302_url:
            args = self.get_url_args(jump302_url)

        if 'questionnaireId' in args and args['questionnaireId'] == '2020011919401334501053001':
            poll_type = True
            order_type = '新装'
        elif 'questionnaireId' in args and args['questionnaireId'] == '2019112714550104601052001':
            poll_type = False
            order_type = '故障'
        else:
            return '%s 无效链接' % url

        new_score_data = [
            {
                "score": 10,
                "questionId": "2019112612330061201052001",
                "questionTitle": "装机整体满意度",
                "answerOrder": 1,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": ""
            },
            {
                "score": 10,
                "questionId": "2020011919364267101052001",
                "questionTitle": "上门及时性",
                "answerOrder": 2,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "上门快,上门准时,提前预约时间"
            },
            {
                "score": 10,
                "questionId": "2019112614320298901052001",
                "questionTitle": "安装专业性",
                "answerOrder": 3,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "装机快,布线美观,现场干净整洁"
            },
            {
                "score": 10,
                "questionId": "2019112614355544701052001",
                "questionTitle": "安装人员服务",
                "answerOrder": 4,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "服务态度好,答疑指导耐心,工装整洁大方"
            },
            {
                "score": "",
                "questionId": "2019112614363640001053001",
                "questionTitle": "装机完成后是否测速",
                "suggestion": "",
                "surveyLables": "是",
                "surveyObjType": "0",
                "answerOrder": 5
            }
        ]

        trouble_score_data = [
            {
                "score": 10,
                "questionId": "2019112714221718701051001",
                "questionTitle": "故障维修整体满意度",
                "answerOrder": 1,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": ""
            },
            {
                "score": 10,
                "questionId": "2019112714472810201052001",
                "questionTitle": "上门及时性",
                "answerOrder": 2,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "上门快,上门准时,有提前预约时间"
            },
            {
                "score": 10,
                "questionId": "2019112714481805801051001",
                "questionTitle": "故障解决专业性",
                "answerOrder": 3,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "故障解决快,现场干净整洁"
            },
            {
                "score": 10,
                "questionId": "2019112714504311401052001",
                "questionTitle": "维修人员服务",
                "answerOrder": 4,
                "surveyObjType": "0",
                "suggestion": "",
                "surveyLables": "服务态度好,答疑指导耐心,工装整洁大方"
            },
            {
                "score": "",
                "questionId": "2019112714514659501053001",
                "questionTitle": "维修完成后是否测速",
                "suggestion": "",
                "surveyLables": "是",
                "surveyObjType": "0",
                "answerOrder": 5
            }
        ]

        score_data = {
            "qnrSuggestion": "",
            "questionList": new_score_data if poll_type else trouble_score_data
        }
        # print(score_data)
        # 0新装　１故障
        eva_result = evaluateResult[0] if poll_type else evaluateResult[1]
        eva_result['qnrId'] = args['questionnaireId']
        post_data = {
            "questionList": json.dumps(score_data, ensure_ascii=False),
            "serNum": '',
            "channelId": '',
            "serType": '',
            "prvo": '',
            "servalue": '',
            "detailsUrl": '/survey/detailsofTomatoOrange.html?taskSheetId=',
            'qnrId': args['questionnaireId'],
            'h5PageUrlWeb': 'https://eva.customer.10086.cn/surv/QnrTomatoOrange.html?questionnaireId=%s' % args[
                'questionnaireId'],
            'token': args['token'],
            'evaluateResult': eva_result
        }

        self.req_headers['Referer'] = jump302_url
        self.s.headers.update(self.req_headers)
        r = self.s.post(
            'https://eva.customer.10086.cn/surveyH5Response/dynamicQuestion',
            data=post_data,
            verify=False
        )
        if r.status_code == 200:
            del self.req_headers['Referer']
            return 'msg:success, status_code:%s, url:%s, order_type:%s, return_text:%s' % (
                r.status_code, url, order_type, r.text
            )
        else:
            return 'msg:failed, status_code:%s, url:%s, order_type:%s, return_text:%s' % (
                r.status_code, url, order_type, r.text
            )

    def get_url_args(self, url):
        args = url.split('?')[1].replace('&&', '&').split('&')
        data = {}
        for i in args:
            x = i.split('=')
            data[x[0]] = x[1]
        return data
