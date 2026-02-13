from flask import Flask, render_template, request
from flask_mail import Mail, Message
import zipfile
import os
from mashup_core import generate_mashup


app = Flask(__name__)

# EMAIL CONFIG (use your gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'yourgmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'cbjq ltop yrjm fqsw'

mail = Mail(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/send', methods=['POST'])
def send():
    singer = request.form['singer']
    num = int(request.form['num'])
    duration = int(request.form['duration'])
    email = request.form['email']

    output_file = f"output/{singer}_mashup.mp3"

    # generate mashup
    generate_mashup(singer, num, duration, output_file)

    # zip file
    zip_path = f"output/{singer}.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(output_file, os.path.basename(output_file))

    # send email
    msg = Message("Your Mashup is Ready",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email])

    msg.body = "Mashup attached."
    with app.open_resource(zip_path) as fp:
        msg.attach(zip_path, "application/zip", fp.read())

    mail.send(msg)

    return "Email Sent Successfully!"


if __name__ == '__main__':
    app.run(debug=True)
