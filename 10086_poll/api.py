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

    domain = "'https://eva.customer.10086.cn'"

    req_headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01,',
        'Connection': 'Keep-Alive',
        'Host': 'eva.customer.10086.cn',
        'Origin': domain,
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

    def validate_url(self, url):
        args = self.get_url_args(url)
        if 'token' in url:
            if 'questionnaireId' in args:
                if args['questionnaireId'] in ['2020011919401334501053001', '2020081910332938601051001']:
                    return {
                        'order_type': 'new',
                        'order_desc': '新装',
                        'data': args
                    }, None
                elif args['questionnaireId'] in ['2020081910351107201051001', '2019112714550104601052001']:
                    return {
                        'order_type': 'trouble',
                        'order_desc': '故障',
                        'data': args
                    }, None
                else:
                    return '%s 版本错误，需要更新' % url, True
            else:
                return '%s 无效链接,未找到问卷ID' % url, True
        else:
            return '%s 无效链接,未找到token' % url, True

    def submit_poll(self, url):
        r = self.s.get(url, verify=False)
        if '重复提交' in r.text:
            return '%s 链接已提交,请勿重复提交' % url
        if '请求超时' in r.text:
            return '%s 链接已失效超时' % url

        jump302_url = r.url
        d, err = self.validate_url(jump302_url)
        if err:
            return d
        else:
            args = d['data']

        new_score_data = [
            # version 1.0
            [{
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
            }],
            # version 1.1
            [{
                "score": 10,
                "questionId": "2020081910051109001051001",
                "questionTitle": "上门及时性",
                "answerOrder": 1,
                "surveyObjType": "3",
                "suggestion": "",
                "surveyLables": "上门快,上门准时,提前预约时间"
            }, {
                "score": 10,
                "questionId": "2020081910072766901052001",
                "questionTitle": "安装人员专业性",
                "answerOrder": 2,
                "surveyObjType": "2",
                "suggestion": "",
                "surveyLables": "装机快,设备调测快/专业"
            }, {
                "score": 10,
                "questionId": "2020081910102653801053001",
                "questionTitle": "安装人员服务",
                "answerOrder": 3,
                "surveyObjType": "2",
                "suggestion": "",
                "surveyLables": "服务态度好,答疑指导耐心,工装整洁大方"
            }, {
                "score": 10,
                "questionId": "2020081910154026401052001",
                "questionTitle": "安装结果",
                "answerOrder": 4,
                "surveyObjType": "2",
                "suggestion": "",
                "surveyLables": "网络质量好,布线美观,现场干净整洁"
            }]
        ]

        trouble_score_data = [
            # version 1.0
            [
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
            ],
            # version 1.1
            [
                {
                    "score": 10,
                    "questionId": "2020081910190618901051001",
                    "questionTitle": "上门及时性",
                    "answerOrder": 1,
                    "surveyObjType": "2",
                    "suggestion": "",
                    "surveyLables": "上门快,上门准时,提前预约时间"
                }, {
                    "score": 10,
                    "questionId": "2020081910265161101053001",
                    "questionTitle": "故障维修结果",
                    "answerOrder": 2,
                    "surveyObjType": "2",
                    "suggestion": "",
                    "surveyLables": "故障彻底解决,现场干净整洁"
                }, {
                    "score": 10,
                    "questionId": "2020081910285490901051001",
                    "questionTitle": "故障人员专业性",
                    "answerOrder": 3,
                    "surveyObjType": "2",
                    "suggestion": "",
                    "surveyLables": "故障解决快,设备调测专业/快"
                }, {
                    "score": 10,
                    "questionId": "2020081910311535201052001",
                    "questionTitle": "维修人员服务",
                    "answerOrder": 4,
                    "surveyObjType": "2",
                    "suggestion": "",
                    "surveyLables": "服务态度好,答疑指导耐心,工装整洁大方"
                }
            ]
        ]

        # new
        if d['order_type'] == 'new':
            # version 1.1
            if args['questionnaireId'] == '2020081910332938601051001':
                evaResult, questList = evaluateResult[2], new_score_data[1]
            # versoin 1.0
            if args['questionnaireId'] == '2020011919401334501053001':
                evaResult, questList = evaluateResult[0], new_score_data[0]
        # trouble
        if d['order_type'] == 'trouble':
            # version 1.1
            if args['questionnaireId'] == '2020081910351107201051001':
                evaResult, questList = evaluateResult[3], trouble_score_data[1]
            # version 1.0
            if args['questionnaireId'] == '2019112714550104601052001':
                evaResult, questList = evaluateResult[1], trouble_score_data[0]

        score_data = {
            "qnrSuggestion": "",
            "questionList": questList
        }

        post_data = {
            "questionList": json.dumps(score_data, ensure_ascii=False),
            "serNum": '',
            "channelId": '',
            "serType": '',
            "prvo": '',
            "servalue": '',
            "detailsUrl": '/survey/detailsofTomatoOrange.html?taskSheetId=',
            'qnrId': args['questionnaireId'],
            'h5PageUrlWeb': '%s/surv/QnrTomatoOrange.html?questionnaireId=%s' % (self.domain, args['questionnaireId']),
            'token': args['token'],
            'evaluateResult': evaResult

        }

        self.req_headers['Referer'] = jump302_url
        # requests lib default header
        self.req_headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        r = self.post_req(post_data)

        if r.status_code == 200:
            del self.req_headers['Referer']
            return 'msg:success, status_code:%s, url:%s, order_type:%s, return_text:%s' % (
                r.status_code, url, d['order_desc'], r.text
            )
        else:
            return 'msg:failed, status_code:%s, url:%s, order_type:%s, return_text:%s' % (
                r.status_code, url, d['order_desc'], r.text
            )

    @staticmethod
    def get_url_args(url):
        args = url.split('?')[1].replace('&&', '&').split('&')
        data = {}
        for i in args:
            x = i.split('=')
            data[x[0]] = x[1]
        return data

    def post_req(self, post_data):
        self.s.headers.update(self.req_headers)
        url = 'https://eva.customer.10086.cn/surveyH5Response/dynamicQuestion'
        return self.s.post(
            url,
            data=post_data,
            verify=False
        )

