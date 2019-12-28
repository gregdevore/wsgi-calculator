"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(sum(map(int,args)))

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    args = [int(arg) for arg in args]
    return str(args[0] - args[1])

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    args = [int(arg) for arg in args]
    return str(args[0] * args[1])

def divide(*args):
    """ Returns a STRING of the integer division of the arguments """
    args = [int(arg) for arg in args]
    return str(args[0] // args[1])

def home():
    """ Returns a formatted guide for how to use the website """
    body = """<h1>Here's how to use this page</h1>
    <p>This page serves as a basic calculator by parsing the URL typed by the user</p>
    <p>Examples:</p>
    <ul>
    <li>http://localhost:8080/multiply/3/5 displays a result of 15</li>
    <li>http://localhost:8080/add/23/42 displays a result of 65</li>
    <li>http://localhost:8080/subtract/23/42 displays a result of -19</li>
    <li>http://localhost:8080/divide/22/11 displays a result of 2</li>
    </ul>
    <p>Note that all inputs and outputs are integer type</p>
    """
    return body


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    functions = {'add': add,
                 'subtract': subtract,
                 'multiply': multiply,
                 'divide': divide,
                 '': home}
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    # Make sure two operands supplied if mathematical function called
    if func_name and len(args) != 2:
        raise ValueError
    try:
        func = functions[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type','text/html')]
    try:
        path = environ.get('PATH_INFO',None)
        if not path:
            raise NameError
        func, args = resolve_path(path)
        status = "200 OK"
        body = func(*args)
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Zero Division Error</h1>"
    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Incorrect Number of Arguments Provided</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length',str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
