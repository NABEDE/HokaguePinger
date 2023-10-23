from flask import Flask, request, render_template
from ping3 import ping

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Remplacez 'your_secret_key' par une clé secrète

from flask_bootstrap import Bootstrap
Bootstrap(app)

def ping_host(host):
    response_time = ping(host)
    if response_time is not None:
        return True  # Le point d'accès est fonctionnel
    else:
        return False  # Le point d'accès ne répond pas

@app.route('/', methods=['GET', 'POST'])
def index():
    
    results = []
    if request.method == 'POST':
        hosts = request.form.get('hosts').split(',')
        for host in hosts:
            host = host.strip()
            result = ping_host(host)
            results.append({'host': host, 'result': result})
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
