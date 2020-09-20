import urllib3
import requests
from evaluateResult import evaluateResult
urllib3.disable_warnings()


class Poll:
    proxies = {
        # 'http': 'http://172.31.10.84:2345',
        # 'https': 'http://172.31.10.84:2345'
    }

    domain = "https://eva.customer.10086.cn"

    req_headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json, text/javascript, */*; q=0.01,',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'Keep-Alive',
        'Host': 'eva.customer.10086.cn',
        'Origin': domain,
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'X-Requested-With': 'XMLHttpRequest'
    }
    s = None

    def __init__(self):
        s = requests.session()
        s.headers.update(self.req_headers)

        if not len(self.proxies):
            s.proxies = self.proxies
        self.s = s

    def build_post_data(self, url):
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
    
    def cookie_and_jumpurl(self, url):
        r = self.s.get(url, verify=False, allow_redirects=False)

        if (r.status_code == 200 or r.status_code == 302) and 'Location' in r.headers:
            self.req_headers['Cookie'] = r.headers['Set-Cookie']
            self.s.headers.update(self.req_headers)
            return r.headers['Location']
        else:
            return None
    
    # def verify_link_is_invalid(self, url):
    #     r = self.s.get(url, verify=False)

    #     if r.status_code == 200:
    #         if '重复提交' in r.text:
    #             return '%s 链接已提交,请勿重复提交' % url
    #         if '请求超时' in r.text:
    #             return '%s 链接已失效超时' % url
    #     else:
    #         return None

    def submit_poll(self, url):
        # jumpurl = self.cookie_and_jumpurl(url)       

        # if not jumpurl:
        #     return '%s 链接提交' % url
        
        # r = self.verify_link_is_invalid(jumpurl)
        # if r:
        #     return r

        jumpurl = 'https://eva.customer.10086.cn/survey/QnrTomatoOrange.html?token=cPhrRI769943&&questionnaireId=2020081910351107201051001&&tokenflag=926ca3b1'
        
        d, err = self.build_post_data(jumpurl)
        if err:
            return d

        post_data = {
            "questionList": d['data']['score'],
            'token': d['url_args']['token'],
            "serNum": '',
            "channelId": '',
            "serType": '',
            "prvo": '',
            'qnrId': d['url_args']['questionnaireId'],
            'h5PageUrlWeb': '%s/surv/QnrTomatoOrange.html?questionnaireId=%s' % (self.domain, d['url_args']['questionnaireId']),
            "servalue": '',
            'evaluateResult': d['data']['eva'],
            "detailsUrl": '/survey/detailsofTomatoOrange.html?taskSheetId=',
        }


        # print(post_data)
        self.req_headers['Referer'] = jumpurl
        # requests lib default header
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
        del self.req_headers['Cookie']

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
        url = '%s/surveyH5Response/dynamicQuestion' % self.domain
        url = 'http://127.0.0.1:8000/test'

        return self.s.post(
            url,
            data=post_data,
            verify=False
        )
