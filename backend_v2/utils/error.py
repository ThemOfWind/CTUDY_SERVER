error_codes = frozenset({400, 401, 404, 500})

server_error_return = {'result': False, 'error': {'message': 'Internal Server Error'}}
param_error_return = {'result': False, 'error': {'message': 'parameter is not present'}}
auth_error_return = {'result': False, 'error': {'message': 'AuthenticationException'}}
active_error_return = {'result': False, 'error': {'message': 'User is not activated'}}
exist_error_return = {'result': False, 'error': {'message': 'Username exists'}}
not_found_error_return = {'result': False, 'error': {'message': 'Not found data'}}
data_conflict_error_return = {'result': False, 'error': {'message': 'Data conflict error'}}


class CtudyException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message
