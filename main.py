import datetime
import smtplib
import ssl
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import gpt4o

# Path to your chromedriver
chromedriver_path = '/opt/homebrew/bin/chromedriver'

# Set up Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--window-size=1920,1080')  # Set window size

# Initialize the WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to the TradingView Bitcoin chart page
    driver.get('https://www.tradingview.com/chart/?symbol=BITSTAMP:BTCUSD')

    # Wait for the chart to load
    time.sleep(10)  # Adjust sleep time if necessary

    # Locate the chart element
    chart_element = driver.find_element(By.CLASS_NAME, 'chart-container')

    # Take a screenshot of the chart
    screenshot_path = 'bitcoin_chart.png'
    chart_element.screenshot(screenshot_path)
    
    print("Screenshot saved as 'bitcoin_chart.png'")

finally:
    # Close the browser
    driver.quit()

gpt_response = gpt4o.analyze_chart(screenshot_path)

# Email configuration
curr_datetime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
smtp_server = 'smtp.gmail.com'
smtp_port = 465
sender_email = '<SENDER EMAIL HERE>'
receiver_email = '<RECEIVER EMAIL HERE>'
password = '<ENTER (APP) PASSWORD HERE>'

# Create the email message
msg = EmailMessage()
msg['Subject'] = 'Bitcoin Chart Analysis ' + curr_datetime
msg['From'] = sender_email
msg['To'] = receiver_email

msg.set_content(gpt_response)

# Attach the screenshot
with open(screenshot_path, 'rb') as f:
    file_data = f.read()
    file_name = f.name
    msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

# Send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
    server.login(sender_email, password)
    server.send_message(msg)

print("Email sent successfully")
