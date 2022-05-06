from functools import wraps

import orjson
from django.http import Http404
from ninja.renderers import BaseRenderer

from utils.error import CtudyException, not_found_error_return, server_error_return


def base_api(logger):
    def decorator(ori_func):
        @wraps(ori_func)
        def inner(request, **kwargs):
            try:
                return {'result': True, 'response': ori_func(request, **kwargs)}
            except Http404 as e:
                logger.error(e.__str__())
                raise CtudyException(404, not_found_error_return)
            except CtudyException as e:
                logger.error(e.message)
                raise CtudyException(e.code, e.message)
            except Exception as e:
                logger.error(e.__str__())
                raise CtudyException(500, server_error_return)
        return inner
    return decorator


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        if 'result' not in data:
            data = {
                'result': True,
                'response': data
            }

        return orjson.dumps(data)
