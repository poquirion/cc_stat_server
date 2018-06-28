from flask import Flask, Response
app = Flask(__name__)


from cc_stat_server import back

@app.route('/')
def reports():
    r = Response(back.reports())
    r.content_type = "text/plain"
    return r

@app.route('/pouet')
def pouet():
    r = Response(back.reports())
    r.content_type = "text/plain"
    return "Pouet\nPouet en effet!"



if __name__ == '__main__':
    app.run()
