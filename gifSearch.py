import sys
import os

try:
    if '3' in sys.version[0]:
        sys.stdout.write(
            '\x1b[1;32m' + '[+] Running Python version: ' + sys.version + '\x1b[0m' + '\n')
except:
    sys.stderr.write(
        '\x1b[1;31m' + 'Error occured' + '\x1b[0m')

try:
    from flask import Flask, render_template, url_for, request, redirect, flash
    os.environ['FLASK_ENV']
except ImportError as error:
    sys.stderr.write(
        '\x1b[1;31m' + error + '\x1b[0m')
except:
    sys.stderr.write(
        '\x1b[1;31m' + 'Please set Flask enviornment variable {FLASK_ENV}' + '\x1b[0m')

app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    try:
        import requests
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
            import json
        except ImportError as error:
            print(error)
        except:
            sys.stderr.write(
                '\x1b[1;31m' + 'Unknown error occured' + '\x1b[0m')
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, key, 20))
        if r.status_code == 200:
            data = json.loads(r.content)
            gifs = []
            results = data['results']
            for item in results:
                gifs.append(item['media'][0]['gif']['url'])
            return render_template('index.html', search_term=search_term, gifs=gifs)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
