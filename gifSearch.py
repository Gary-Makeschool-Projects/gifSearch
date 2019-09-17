import sys
import os
import time
#import words


try:
    if '3' in sys.version[0]:
        sys.stdout.write(
            '\x1b[1;32m' + '[+] Running Python version: ' + sys.version + '\x1b[0m' + '\n')
except:
    sys.stderr.write(
        '\x1b[1;31m' + 'Run application with latest version of python' + '\x1b[0m')

try:
    # import flask module
    from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
    from flask_sqlalchemy import SQLAlchemy
    os.environ['FLASK_ENV']
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)  # app name
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['SECRET_KEY'] = '\x04q\xb3\x08\xe0tn\xc1n\xa4\x90\x82\xd8\xf4\xe8\x87\xf0\x90\xe3bhI~\xd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'server.db')
    db = SQLAlchemy(app)
    portnum = 8080  # run server on this port
except ImportError as error:
    sys.stderr.write(
        '\x1b[1;31m' + error + '\x1b[0m')
except:
    sys.stderr.write(
        '\x1b[1;31m' + 'Please set Flask enviornment variable {FLASK_ENV}' + '\x1b[0m')
try:
    import requests  # import requests module
    import json  # import json module
    from requests.adapters import HTTPAdapter  # import HTTPAdapter module
    from requests.packages.urllib3.util.retry import Retry  # import Retry module
except ImportError as error:
    sys.stderr.write(
        '\x1b[1;31m' + error + '\x1b[0m')


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None,):
    """Retry requesting session
    Keyword arguments:
        retries -- limit of retries before fatal error
        backoff_factor -- time limit before creating new request
        status_forcelist -- force retry request status code list
        session -- established connection between client and server
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,  # retry limit
        read=retries,  # retry limit again
        connect=retries,  # retry limit andddd again
        backoff_factor=backoff_factor,  # wait time
        status_forcelist=status_forcelist,  # status code auto retry list
    )
    adapter = HTTPAdapter(max_retries=retry)  # start reconnection
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    try:
        os.environ['API_KEY']
    except KeyError:
        sys.stderr.write(
            '\x1b[1;31m' + 'Please set enviornment variable API_KEY' + '\x1b[0m')
    except ImportError as error:
        sys.stderr.write(
            '\x1b[1;31m' + error + '\x1b[0m')
    except:
        sys.stderr.write(
            '\x1b[1;31m' + 'Unknown error occured' + '\x1b[0m')

    if request.method == 'POST':
        #data = request.get_json(force=True)
        a = request.form['search']
        # term = str(data['search_term'])
        form = request.form.to_dict()
        print("This is the search term")
        #search_term = data['search_term']
        search_term = a

        print(search_term)
        key = os.environ['API_KEY']

        try:

            search = "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (
                search_term, key, 1)
            t0 = time.time()  # initial request time
            # check server response
            response = requests_retry_session().get(search)
            # okay status code
            if response.status_code == 200:
                r = response  # response object
                data = json.loads(r.content)
                gifs = []
                results = data['results']
                for item in results:
                    gifs.append(item['media'][0]['gif']['url'])
                    print(item)
                if not gifs:
                    empty = "Did not find any gifs with that word please try again"
                    return render_template('index.html', empty=empty)
                else:
                    print('Test call')
                    return render_template('index.html', search_term=search_term, gifs=gifs)
        except requests.exceptions.Timeout:
            pass
        # maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            pass
            # tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. we are fucked! bail!
            print(e)
            sys.exit(1)
        finally:
            t1 = time.time()  # end request time
            print('Took', t1 - t0, 'seconds')

    return render_template('index.html')
# this is also another test route
@app.route('/countries')
def countrydic():
    res = Country.query.all()
    list_countries = [r.as_dict() for r in res]
    return jsonify(list_countries)
# this route was just meant for testing purposes ignore
# @app.route('/reciever', methods=['POST'])
# def receive():
#     data = request.get_json(force=True)
#     result = ''
#     print(data['search_term'])
#     # for item in data:
#     #     # loop over every row
#     #     result += item[0] + '\n'

#     return data


if __name__ == "__main__":
    app.run(debug=True, port=portnum)
