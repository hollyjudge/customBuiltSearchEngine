from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def proxy():
    solr_host = 'localhost'
    solr_port = 8983
    solr_path = '/solr/documents2/select'

    query = request.args.get('q', '')

    solr_url = f'http://{solr_host}:{solr_port}{solr_path}?q={query}&wt=json'
    #solr_url = f'http://localhost:8983/solr/documents2/select?indent=true&q.op=OR&q=*%3A*&qt=hello&useParams='
    solr_response = requests.get(solr_url)

    if solr_response.status_code == 200:
        return jsonify(solr_response.json())
    else:
        return jsonify(error='Error searching Solr'), solr_response.status_code

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
