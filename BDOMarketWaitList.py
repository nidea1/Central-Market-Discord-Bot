import urllib.request
import requests
import json
from datetime import datetime


def printResults(data):
    theJSON = json.loads(data)

    for i in range(len(theJSON)):
        print(theJSON[i]["name"])
        timestamp = theJSON[i]["liveAt"]
        time = datetime.fromtimestamp(timestamp)
        print("Register Time: ", str(time.hour)+":"+str(time.minute)+":"+str(time.second))

def main():
    urlData = "https://api.arsha.io/v2/mena/GetWorldMarketWaitList"


    webUrl = urllib.request.urlopen(urlData)
    if (webUrl.getcode() == 200):
        data = webUrl.read().decode("utf-8")
        printResults(data)
    else:
        print("Received an error from server, cannot retrieve results " +
              str(webUrl.getcode()))


if __name__ == "__main__":
    main()

