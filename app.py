from flask import Flask, Response
app = Flask(__name__)


from cc_stat_server import back


def cors_head():
    return {'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'OPTIONS, POST, GET, PUT, DELETE'}


@app.route('/full')
def reports():
    return Response(back.reports(), mimetype="application/json", headers=cors_head())

@app.route('/pouet')
def pouet():
    return "Pouet\nPouet en effet!"



if __name__ == '__main__':
    app.run()
