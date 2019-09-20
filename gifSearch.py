import sys
import os
import time


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
    # import SQLAlchemy
    from flask_sqlalchemy import SQLAlchemy
    # flask enviornment variable
    os.environ['FLASK_ENV']
    # database path
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)  # app name
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # file age
    app.config[
        'SECRET_KEY'] = '\x04q\xb3\x08\xe0tn\xc1n\xa4\x90\x82\xd8\xf4\xe8\x87\xf0\x90\xe3bhI~\xd5'  # secret key encoding
    # data base URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'server.db')
    # creat database object with alchemy
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
    """ Cool index route.
    @GET:
        summary: index endpoint will render file 'index.html'
        description: Get
        responses:
            200:
                description: index.html returned
                schema: indexSchema
            404:
                description: index not found.
    @POST:
        summary:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
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
    # listen for GET request
    if request.method == 'GET':
        search_term = 'gary'
        apikey = os.getenv('API_KEY')
        lmt = 10
        rand = "https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (
            search_term, apikey, lmt)
        # check server response
        response = requests_retry_session().get(rand)
        # okay status code
        if response.status_code == 200:
            r = response  # response object
            data = r.json()
            gifs = []
            results = data['results']
            for item in results:
                gifs.append(item['media'][0]['gif']['url'])
            if not gifs:
                print('Called empty array')
                empty = "Did not find any gifs with that word please try again"
                return render_template('index.html', emtyp=empty)
            else:
                return render_template('index.html', gifs=gifs)

    # listen for POST request
    if request.method == 'POST':
        a = request.form['search']
        search_term = a
        key = os.environ['API_KEY']
        try:
            search = "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (
                search_term, key, 10)
            t0 = time.time()  # initial request time
            # check server response
            response = requests_retry_session().get(search)
            # okay status code
            if response.status_code == 200:
                r = response  # response object
                data = r.json()
                gifs = []
                results = data['results']
                for item in results:
                    gifs.append(item['media'][0]['gif']['url'])
                if not gifs:
                    empty = "Did not find any gifs with that word please try again"
                    return render_template('index.html', empty=empty)
                else:
                    return render_template('index.html', search_term=search_term, gifs=gifs)
        except requests.exceptions.Timeout:
            print('Session timeout')
        # maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            print('Too many redirects')
            # tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. we are fucked! bail!
            print(e)
            sys.exit(1)
        finally:
            t1 = time.time()  # end request time
            print('Took', t1 - t0, 'seconds')
        x = render_template('index.html')
        print(x)
    return render_template('index.html')


@app.route('/auto', methods=['POST'])
def receive():
    """ Cool index route.
    @GET:
        summary: index endpoint will render file 'index.html'
        description: Get
        responses:
            200:
                description: index.html returned
                schema: indexSchema
            404:
                description: index not found.
    @POST:
        summary:
        description:
        responses:
            200:
                description:
            400:
                description:
    """
    if request.method == 'POST':
        data = request.get_json(force=True)
        search_term = data['search_term']
        key = os.environ['API_KEY']
        try:
            search = "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (
                search_term, key, 10)
            t0 = time.time()  # initial request time
            # check server response
            response = requests_retry_session().get(search)
            # okay status code
            if response.status_code == 200:
                r = response  # response object
                data = r.json()
                gifs = []
                results = data['results']
                for item in results:
                    gifs.append(item['media'][0]['gif']['url'])
                if not gifs:
                    empty = "Did not find any gifs with that word please try again"
                    return jsonify(gifs)
                else:
                    return jsonify(gifs)
        except requests.exceptions.Timeout:
            print('Session timeout')
        # maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            print('Too many redirects')
            # tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. we are fucked! bail!
            print(e)
            sys.exit(1)
        finally:
            t1 = time.time()  # end request time
            print('Took', t1 - t0, 'seconds')


# test route for database
# @app.route('/countries')
# def countrydic():
#     res = Country.query.all()
#     list_countries = [r.as_dict() for r in res]
#     return jsonify(list_countries)

if __name__ == "__main__":
    app.run(debug=True, port=portnum)
