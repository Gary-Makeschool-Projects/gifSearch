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
    from flask import Flask, render_template, url_for, request, redirect, flash
    os.environ['FLASK_ENV']
    app = Flask(__name__)  # app name
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


@app.route('/')
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
        form = request.form.to_dict()
        search_term = form['search']
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
                data = json.loads(r.content)
                gifs = []
                results = data['results']
                for item in results:
                    gifs.append(item['media'][0]['gif']['url'])
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


if __name__ == "__main__":
    app.run(debug=True, port=portnum)
