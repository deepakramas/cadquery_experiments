from flask import Flask
from flask import request
import os
from heat_profile import createCircleWithHoles
app = Flask(__name__)

@app.route("/")
def index():
    n = request.args.get("n")
    if not n:
	n = 2
    else:
	n = int(n)
    
    r = request.args.get("r")
    if not r:
	r = 1.1
    else:
	r = float(r)
    
    return createCircleWithHoles(n,r)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port,debug=True)
