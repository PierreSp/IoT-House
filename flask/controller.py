import subprocess
import random
from flask import Flask, redirect, url_for, request, render_template, session
app = Flask(__name__)

# Secret key for session
app.secret_key = "".join([str(x) for x in random.sample(range(1000), 10)])
PASSWORD = "pw"

# App routes define the adresses used


@app.route('/')
def settings_mainpage():
    # Templates must be in the templates folder, and can be written
    # dynamically or static by python, too (if needed)
    return render_template('index.html')


@app.route('/moved_shade')
def moved():
    # if session["pw"]== PASSWORD:
    shades = session["shade"]
    terminal = ""
    if "shade1" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
    if "shade2" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
    if "shade3" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
    # Or do whatever is needed to move the window
    # shade or to controll the light
    return("""The shade was moved. Return: {} Shades selected: {} """.format(terminal, shades))


@app.route('/wrong_password')
def failed():
    return("The password was not correct")


@app.route('/move_shade', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':  # If submit button is used
        password = request.form['password']
        session["shade"] = request.form.getlist("shade")
        session["pw"] = password
        #return ("{}".format(sel_shades))
        if password == PASSWORD or 1:
            return redirect(url_for('moved'))
        else:
            return redirect(url_for("failed"))
    else:
        password = request.args.get('password')  # If we use get request
        if password == PASSWORD or 1:
            return redirect(url_for('moved'))
        else:
            return redirect(url_for("failed"))


if __name__ == '__main__':
    # Set port for webserver
    app.run(debug=True, port=3000)
