import speedtest
from flask import Flask, render_template, url_for, redirect
import wtforms
from flask_wtf import FlaskForm
import ujson as json

app = Flask(__name__)
st = speedtest.Speedtest()

app.config["SECRET_KEY"] = "h"


@app.route("/redirect")
def redirect_to():
    return render_template("redirect.html")


@app.route("/", methods=["GET", "POST"])
def index():
    class Button(FlaskForm):
        start_button = wtforms.SubmitField("Start Test")

    form = Button()

    if form.validate_on_submit():
        return redirect(url_for("redirect_to"))

    return render_template("index.html", form=form)


@app.route("/results")
def results():
    st.download()
    st.upload()

    result_json = json.loads(st.results.json())

    data = {
        "download": int(round(result_json['download'] / 1000.0, 0) / 1000),
        "ping": int(round(result_json['ping'], 0)),
        "upload": int(round(result_json['upload'] / 1000.0, 0) / 1000),
        "client": result_json["client"]
    }

    return render_template("result.html", data=data)


if __name__ == "__main__":
    app.run()
