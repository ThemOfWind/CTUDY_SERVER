from functools import wraps

from django.http import Http404

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
            except Exception as e:
                logger.error(e.__str__())
                raise CtudyException(500, server_error_return)
        return inner
    return decorator
