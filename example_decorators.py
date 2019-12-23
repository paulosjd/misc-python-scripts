import json
from collections import namedtuple
from datetime import datetime

# Example 1: Injecting New Arguments


def add_current_time(f):
    def wrapped(*args, **kwargs):
        return f(datetime.utcnow(), *args, **kwargs)
    return wrapped


@add_current_time
def test(time, a, b):
    print('I received arguments', a, b, 'at', time)


test(1, 2)

# Example 2: Altering the Return Value of a Function


def to_json(f):
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, (dict, list)):
            # response = jsonify(response)
            response = json.dumps(response)
        return response
    return wrapped

# @app.route('/')
@to_json
def index():
    return {'hello': 'world'}


print(index())


# Example 3: Validation

ADMIN_TOKEN = 'fheje3$93m*fe!'
Request = namedtuple('request', 'headers')
request1 = Request({})
request2 = Request({'X-Auth-Token': ADMIN_TOKEN})


def only_admins(f):
    def wrapped(*args, **kwargs):
        token = args[0].headers.get('X-Auth-Token')
        if token != ADMIN_TOKEN:
            return 'raise something'
            # abort(401)
        return f(*args, **kwargs)
    return wrapped


@only_admins
def admin_route(request):
    return "only admins can access this route!"


print(admin_route(request1))
print(admin_route(request2))


def my_example_decorator(f):
    def wrapped(*args, **kwargs):
        # ...
        # insert code that runs before the decorated function
        # (and optionally decide to not call that function)
        # ...
        response = f(*args, **kwargs)
        # ...
        # insert code that runs after the decorated function
        # (and optionally decide to change the response)
        # ...
        return response
    return wrapped


"""
>>> @my_decorator
... def my_function(a, b):
...     return a + b
...
decorating <function my_function at 0x10ae241e0>
>>> my_function(1, 2)
3
>>>
Note how the printed output appears when the function is defined, not when it is invoked.
This is because Python calls the decorator function at the time the decorated function is declared.
"""