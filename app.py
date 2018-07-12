from flask import Flask, Response
import json
app = Flask(__name__)


from cc_stat_server import back

@app.route('/full')
def reports():
    r = Response(json.dumps(back.reports()))
    r.content_type = "application/json"
    return r

@app.route('/pouet')
def pouet():
    return "Pouet\nPouet en effet!"



if __name__ == '__main__':
    app.run()
