import requests
from bs4 import BeautifulSoup
import hashlib
from os.path import exists
from datetime import datetime

URL = ""
BASIC_AUTH_USERNAME = ""
BASIC_AUTH_PASSWORD = ""
# Update this to anything you want to use as the 'seed' for the change hash
# Ideally it is a region or set of values that a page has that you want to watch.
SOUP_FIND_ALL_CONDITION = "table"
FILENAME = "SiteHashLog.txt"


def checkIfPageChanged(hash):
    file = open(FILENAME, 'r')
    lastLine = file.readlines()[-1].split(',')[1]
    return lastLine == hash


def generateSiteHash():
    if (BASIC_AUTH_USERNAME != ""):
        page = requests.get(URL, auth=(
            BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))
    else:
        page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser").findAll(
        SOUP_FIND_ALL_CONDITION)
    return hashlib.md5(str(soup).encode('utf-8')).hexdigest()


def saveHashToFile(hash):
    file = open(FILENAME, "a")
    dateTimeNow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    file.write(dateTimeNow + ',' + hash + '\n')
    file.close()


def setup():
    if not exists(FILENAME):
        print(
            "First time run detected - you will need to run it again to check for changes")
        file = open(FILENAME, 'w').close()
        saveHashToFile(generateSiteHash())
        exit()


def run():
    pageHash = generateSiteHash()
    if (checkIfPageChanged(pageHash)):
        # TODO: Pop an OS notification
        print("Website has changed!")
        saveHashToFile(pageHash)
    else:
        # TODO: Pop an OS notification
        print("Website is the same as it was before")


if __name__ == "__main__":
    setup()
    run()
