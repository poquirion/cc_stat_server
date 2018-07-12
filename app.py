from flask import Flask, Response
app = Flask(__name__)


from cc_stat_server import back

@app.route('/full')
def reports():
    return Response(back.reports(), mimetype="application/json")

@app.route('/pouet')
def pouet():
    return "Pouet\nPouet en effet!"



if __name__ == '__main__':
    app.run()
