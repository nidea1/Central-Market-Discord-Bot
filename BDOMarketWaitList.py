import urllib.request
import requests
import json
from datetime import datetime


def printResults(data):
    # Use the json module to load the string data into a dictionary
    theJSON = json.loads(data)

    # now we can access the contents of the JSON like any other Python object
    for i in range(len(theJSON)):
        print(theJSON[i]["name"])
        timestamp = theJSON[i]["liveAt"]
        time = datetime.fromtimestamp(timestamp)
        ("Register Time: ", str(time.hour)+":"+str(time.minute)+":"+str(time.second))
        

def main():
    # define a variable to hold the source URL
    # in this case we'll use the free data feed from the arsha.io
    # this feed lists Black Desert Online(MENA) Market Wait List
    # if u want use this for other server just change YourServer from "https://api.arsha.io/v2/YourServer/GetWorldMarketWaitList"
    urlData = "https://api.arsha.io/v2/mena/GetWorldMarketWaitList"

    # Open the URL and read the data
    webUrl = urllib.request.urlopen(urlData)
    if (webUrl.getcode() == 200):
        data = webUrl.read().decode("utf-8")
        printResults(data)
    else:
        print("Received an error from server, cannot retrieve results " +
              str(webUrl.getcode()))


if __name__ == "__main__":
    main()

