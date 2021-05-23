from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import json
import web_server

app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')


@app.route('/answer', methods=["POST", 'OPTIONS'])
@cross_origin()
def answer():
    req = request.get_data(as_text=True)
    query = json.loads(req)['question']
    res = web_server.medical_query(query)
    with open('backend.txt', 'a+', encoding="utf-8") as f:
        print("ANSWER: ", query, res, file=f)
    ans = {'answer': res}
    return json.dumps(ans)


@app.route('/diseases', methods=["POST", 'OPTIONS'])
@cross_origin()
def get_diseases():
    req = request.data.decode('utf-8')
    query = json.loads(req)['contains']
    res = web_server.preparse(query)
    ans = {'diseases': res}
    with open('backend.txt', 'a+', encoding="utf-8") as f:
        print("GET_DISEASES: ", query, res, file=f)
    return json.dumps(ans)


if __name__ == '__main__':
    with open('backend.txt', 'a+', encoding="utf-8") as f:
        f.write("YES!")
    app.run(host='0.0.0.0')
