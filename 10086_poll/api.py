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
        data = {
            '2020011919401334501053001': {
                'order_desc': '装机',
                'version': 1.0,
                'url_args': args,
                'data': {
                    'eva': evaluateResult['2020011919401334501053001']['eva'],
                    'score': evaluateResult['2020011919401334501053001']['post'],
                }
            },
            '2020081910332938601051001': {
                'order_desc': '装机',
                'version': 1.1,
                'url_args': args,
                'data': {
                    'eva': evaluateResult['2020081910332938601051001']['eva'],
                    'score': evaluateResult['2020081910332938601051001']['post'],
                }
            },
            '2020081910351107201051001': {
                'order_desc': '故障',
                'version': 1.1,
                'url_args': args,
                'data': {
                    'eva': evaluateResult['2020081910351107201051001']['eva'],
                    'score': evaluateResult['2020081910351107201051001']['post'],
                }
            },
            '2019112714550104601052001': {
                'order_desc': '故障',
                'version': 1.0,
                'url_args': args,
                'data': {
                    'eva': evaluateResult['2019112714550104601052001']['eva'],
                    'score': evaluateResult['2019112714550104601052001']['post'],
                }
            }
        }
        if 'token' in url and 'questionnaireId' in args and args['questionnaireId'] in data:
            return data[args['questionnaireId']], None
        else:
            return '%s 无效链接,未找到token或者问卷ID' % url, True

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

        post_data = {
            "questionList": json.dumps(
                {
                    "qnrSuggestion": "",
                    "questionList": d['data']['score']
                }, ensure_ascii=False
            ),
            "serNum": '',
            "channelId": '',
            "serType": '',
            "prvo": '',
            "servalue": '',
            "detailsUrl": '/survey/detailsofTomatoOrange.html?taskSheetId=',
            'qnrId': d['url_args']['questionnaireId'],
            'h5PageUrlWeb': '%s/surv/QnrTomatoOrange.html?questionnaireId=%s' % (self.domain, d['url_args']['questionnaireId']),
            'token': d['url_args']['token'],
            'evaluateResult': json.dumps(d['data']['eva'], ensure_ascii=False)
        }

        # print(post_data)
        # return 'aaaa'
        self.req_headers['Referer'] = jump302_url
        # requests lib default header
        # self.req_headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        r = self.post_req(post_data)

        tmp_str = 'url:%s, order_type:%s, version:%s' % (url, d['order_desc'], d['version'])
        if r.status_code == 200:
            return 'msg:success, status_code:%s, %s, return_text:%s' % (
                r.status_code, tmp_str, r.text
            )
        else:
            return 'msg:failed, status_code:%s, %s, return_text:%s' % (
                r.status_code, tmp_str, r.text
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
