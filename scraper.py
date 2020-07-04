import requests
import time

from bs4 import BeautifulSoup
import smtplib

"""
This is my first dabble into webscraping. Not anything fancy, 
just a program that gets an URL for a product from komplett.no 
(minor customization is needed if you wanna change the website)

check_price uses BeautifulSoup to scrape the page and get the 
price of the item. If price is below desired price, an email
is sent through the send_email function

send_email uses smtplib to just send an email with the URL
to my personal email (must be gmail if you wanna customize
it for yourself)

To get YOUR_APP_PASSWORD just set up 2-step authentication and google search "google app password"
"""

# Get URL and desired price
URL = input("Paste desired URL: ")
desiredMax = input("Give a maximum price in NOK: ")

headers = {
    'YOUR_USER_AGENT'}

searching = True


# Check price by scraping
def check_price():
    print(URL)
    print(desiredMax)
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(name="title").get_text()
    rawPrice = soup.find(class_="product-price-now").get_text()
    remove = '[-, \xa0 ]'
    rawPrice = ''.join(c for c in rawPrice if c not in remove)
    price = float(rawPrice)

    print(title)
    print(price)

    if(price < float(desiredMax)):
        send_email()
        return True


# Send mail when price is below desiredMax
def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('YOUR_EMAIL@gmail.com', 'YOUR_APP_PASSWORD')

    subject = 'Price fell down!'
    body = 'Check the link ' + URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('YOUR_EMAIL@gmail.com', 'YOUR_EMAIL@gmail.com', msg)

    print("MAIL SENT")
    server.quit()


while(searching):
    if(check_price()):
        searching = False
    # Sleep for 1 hour
    time.sleep(60 * 60)
