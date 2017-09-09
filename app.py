from flask import Flask, request, send_file, Response
import StringIO
import uuid
import json
from cassandra.cluster import Cluster
from identify_image import get_code

app = Flask(__name__)

KEY_SPACE = 'mnist'
CREATE_KEY_SPACE = "create keyspace if not exists %s with replication = {'class': 'SimpleStrategy', 'replication_factor': 1};" % KEY_SPACE
CREATE_TABLE = "create table if not exists picdatabase(uid text, filedata blob, answer int, primary key(uid));"
cluster = Cluster(["127.0.0.1"])

session = cluster.connect()
session.execute(CREATE_KEY_SPACE)
session.set_keyspace(KEY_SPACE)
session.execute(CREATE_TABLE)


@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.files['file']
    if data:
        file = data.read()
        answer = get_code(data)
        params = [str(uuid.uuid1()), bytearray(file), answer]
        session.execute("INSERT INTO picdatabase (uid,filedata,answer) VALUES (%s, %s, %s)", params)
        result = session.execute("SELECT * FROM picdatabase")
        for x in result:
            print (x.uid, x.answer)
        data = {
            "uid": params[0],
            "answer": answer
        }
        return Response(json.dumps(data), mimetype='application/json')
    return "no file"


@app.route('/download/<uid>', methods=['GET'])
def download_file(uid):
    print(uid)
    result = session.execute("SELECT * FROM picdatabase WHERE uid=%s", [uid])
    print(result[0])
    if result[0]:
        print result[0].filedata
        return send_file(
            StringIO.StringIO(result[0].filedata),
            attachment_filename="result.png",
            as_attachment=True)
    return "not found"


if __name__ == '__main__':
    app.run("0.0.0.0", port=9999)


# curl -F "file=@3.png" "http://localhost:9999/upload"
