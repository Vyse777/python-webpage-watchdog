import os
import smtplib
import ssl
import sys


def sendRyobiAvailabilityNotificationEmail(smtpUsername, smtpPassword, emailAddress):
    message = f"""From: Home Depot RYOBI Watcher <{emailAddress}>
To: Notification <{emailAddress}>
Subject: Product Watcher - RYOBI Product Fulfillment Options Have Changed!

Your automated product watcher has detected the fulfillment options of the RYOBI Swift Clean product at Home Depot 
has changed! 

Please click here to view/purchase the product:
https://www.homedepot.com/p/RYOBI-ONE-18V-Cordless-SWIFTClean-Spot-Cleaner-Tool-Only-PCL756B/319962906
"""
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(smtpUsername, smtpPassword)
        # First use of email address is the from-address
        server.sendmail(emailAddress, emailAddress, message)


if __name__ == "__main__":
    smtpUsernameEnv = os.environ.get('SMTP_USERNAME')
    smtpPasswordEnv = os.environ.get('SMTP_PASSWORD')
    if smtpUsernameEnv is None or smtpPasswordEnv is None:
        print("ERROR: Missing SMTP_USERNAME or SMTP_PASSWORD environment variables")
        exit(-1)
    if len(sys.argv) == 1:
        print('No parameter supplied for sendTo and sendFrom. Please provide 1 email address as a parameter')
        exit(2)
    else:
        sendRyobiAvailabilityNotificationEmail(smtpUsernameEnv, smtpPasswordEnv, sys.argv[1], sys.argv[1])

