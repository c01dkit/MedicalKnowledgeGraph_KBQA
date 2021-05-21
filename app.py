from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import json
import web_server

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')

@app.route('/answer', methods=["POST", 'OPTIONS'])
@cross_origin()
def answer():
    req = request.data.decode('utf-8')
    query = json.loads(req)['question']
    es = web_server.medical_query(query)
    with open('log.txt', 'a+', encoding="utf-8") as f:
        print(query,es,file=f)
    ans = {'answer': es}
    return json.dumps(ans)


if __name__ == '__main__':
    with open('log.txt','a+', encoding="utf-8") as f :
        f.write("YES!")
    app.run(host='0.0.0.0')
