import subprocess
import random
from flask import Flask, redirect, url_for, request, render_template, session
from flask_socketio import SocketIO, send, join_room, leave_room
import json

app = Flask(__name__)
socketio = SocketIO(app, manage_session=True)



# Secret key for session
app.secret_key = "".join([str(x) for x in random.sample(range(1000), 10)])
PASSWORD = "pw"  # Password (currently disabled)


@socketio.on('client_connected', namespace='/')
def handle_client_connect_event(json):
    print('received json: {0} with:{1}'.format(str(json), str(request.sid)))
    session["ioid"] = request.sid
    print(session["ioid"])
    print(json["data"])


@socketio.on('message', namespace='/')
def handle_submit_button(json):
    # it will forward the json to all clients.
    send(json, json=True)
    if "rasp" in str(json):
        room = "rasp"
        join_room(room)
        send(str(request.sid) + ' has entered the room.', room=room)



@socketio.on('disconnect', namespace='/')
def test_disconnect():
    leave_room("rasp")
    print('Client disconnected')

# App routes define the adresses used


@app.route('/')
def settings_mainpage():
    # Templates must be in the templates folder, and can be written
    # dynamically or static by python, too (if needed)
    return render_template('index.html')


@app.route('/rasp', methods=['GET'])
def rasplink():
    password = request.args.get('password')
    if password == "MASTERPASS":
        return ("""<script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
            <script type="text/javascript">
            socket = io.connect('http://' + document.domain + ':' + location.port);
            socket.send('{"message": "rasp"}');
            socket.on('message', function (data) {
              console.log('message form backend ' + data);
            });
            </script>""")
    else:
        return redirect(url_for("failed"))


@app.route('/moved_shade')
def moved():
    # if session["pw"]== PASSWORD:
    shades = session["shade"]
    print(shades)
    terminal = ""
    # Check which shade is called and run specific command in terminal
    # Or do whatever is needed to move the window
    if "shade1" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
        socketio.send("SHADE1", room="rasp")

    if "shade2" in shades:
        terminal += "<br>" + str(subprocess.check_output(['echo $HOME'], shell=True))
        socketio.send("SHADE2", room="rasp")

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
        if password == "MASTERPASS":
            global rid
            rid = session["ioid"]
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
