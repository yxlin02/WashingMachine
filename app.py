from flask import Flask
from flask import render_template
from flask import request
import deal_with
import threading
import sendEmail
import time
from flask import session


class MyThreading(threading.Thread):
    def __init__(self, id, sleep_time):
        threading.Thread.__init__(self)
        self.id = id
        self.sleep_time = sleep_time

    def run(self):
        time.sleep(self.sleep_time)
        sendEmail.send_email(self.id)


app = Flask(__name__)
app.config["SECRET_KEY"] = "renyizifuchuan"


@app.route('/')
def hello_world():
    return render_template("login.html", tmp=False)


@app.route('/login', methods=['post'])
def login():
    user_name = request.form['user_name']
    password = request.form['password']
    result, washingID = deal_with.login_deal_with(user_name, password)
    if result:
        session["user"] = user_name
        session["washingID"] = washingID
        time_, id, k_x, user_id = deal_with.select_washing()
        return render_template("index.html", time_=time_, idx=id, k_x=k_x, user_id=user_id)
    else:
        return render_template("login.html", tmp=True)


@app.route('/subscribe', methods=['post'])
def subscribe():
    subscribe_time = request.form['startTime']
    time_array = time.strptime(subscribe_time, "%Y-%m-%d %H:%M:%S")
    now = int(time.time())
    time_stamp = int(time.mktime(time_array))
    thread = MyThreading(session.get("user"), time_stamp - now)
    thread.start()
    time_, id, k_x, user_id = deal_with.select_washing()
    return render_template("index.html", time_=time_, idx=id, k_x=k_x, user_id=user_id)


@app.route("/borrow")
def borrow():
    # 借
    washing_id = int(request.args.get("id"))
    deal_with.borrow(washing_id, session.get("user"))
    # 洗衣时间
    thread = MyThreading(session.get("user"), 1 * 10)
    thread.start()
    session["washingID"] = washing_id
    time_, id, k_x, user_id = deal_with.select_washing()
    # time_[washing_id - 1] = 360
    return render_template("index.html", time_=time_, idx=id, k_x=k_x, user_id=user_id)


@app.route("/still")
def still():
    washing_id = int(request.args.get("id"))
    deal_with.still(washing_id, session.get("user"))
    session["washingID"] = 0
    time_, id, k_x, user_id = deal_with.select_washing()
    return render_template("index.html", time_=time_, idx=id, k_x=k_x, user_id=user_id)


@app.route('/subscribe_', methods=['get'])
def subscribe_():
    return render_template("subscribe.html")


@app.route('/exit', methods=['get'])
def exit():
    session.clear()
    return render_template("login.html", tmp=False)


if __name__ == '__main__':
    app.run(host="192.168.6.36", debug=True, port=8080)
