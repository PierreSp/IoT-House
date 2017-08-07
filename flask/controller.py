import subprocess
import random
from flask import Flask, redirect, url_for, request, render_template, session
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

# Secret key for session
app.secret_key = "".join([str(x) for x in random.sample(range(1000), 10)])
PASSWORD = "pw"  # Password (currently disabled)

# App routes define the adresses used


@app.route('/')
def settings_mainpage():
    # Templates must be in the templates folder, and can be written
    # dynamically or static by python, too (if needed)
    return render_template('index.html')



@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))
    send('message')


@socketio.on('message')
def handle_json_button(json):
    # it will forward the json to all clients.
    send(json, json=True)   


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@app.route('/moved_shade')
def moved():
    # if session["pw"]== PASSWORD:
    shades = session["shade"]
    terminal = ""
    # Check which shade is called and run specific command in terminal
    # Or do whatever is needed to move the window
    if "shade1" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
    if "shade2" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
    if "shade3" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
    socketio.send("CHANGED")
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
    # Set port for webserver and run it
    socketio.run(app, debug=True, port=3000, use_reloader=False)
