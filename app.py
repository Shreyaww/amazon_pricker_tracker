from flask import Flask, render_template, request
from flask import Flask, render_template, url_for
import requests
from bs4 import BeautifulSoup as bs
from smtplib import SMTP

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL_ID = "2020.shreya.singh@ves.ac.in"
PASSWORD = "gyhbuntzprvskqnv"


app = Flask(__name__)

def notify(url):
    server = SMTP(SMTP_SERVER, PORT)
    server.starttls()
    server.login(EMAIL_ID, PASSWORD)

    subject = "BUY NOW!!"
    body = "Price has reduced, Go Buy Now! " +url
    msg = f"Subject : {subject}\n\n{body}"

    server.sendmail(EMAIL_ID, EMAIL_ID, msg)
    server.quit()

@app.route('/track_price', methods = ["POST"])
def track_price():
    url = request.form['url-input']
    afford_price = float(request.form['affordable'])
    page = requests.get(url, headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"})
    soup = bs(page.content, "html.parser")
    val = soup.find(class_ = "a-price-whole").text.split()[0].replace(",", "")
    val = val.split()[0].replace("₹", "")
    price = float(val)
    if price <= afford_price :
        notify(url)
        return "mail sent successfully!!"
    return "Low Price Product not Found!"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
