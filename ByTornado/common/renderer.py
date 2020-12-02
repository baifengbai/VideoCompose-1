from loguru import logger
from rest_framework.renderers import JSONRenderer

class CustomerJsonRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context['response']
            code = msg = None
            code = 0 if int(response.status_code) == 200 else 1
            if isinstance(data, dict):
                msg = data.pop('msg', msg)
                code = data.pop('code', code)
                data = data.pop('data', data)
            if code != 0 and data:
                if response.status_code == 401:
                    code = 666
                    msg = "登录失效，重新登录"
                    data = {}
                elif response.status_code == 400:
                    msg = "用户名或密码错误"
                    data = {}
                else:
                    try:
                        msg = data.pop('detail', 'failed')
                    except:
                        pass
            response.status_code = 200
            res = {
                'code': code,
                'msg': msg,
                'data': [],
            }
            if len(data) != 0:
                res.update({
                    "data": data
                })
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)