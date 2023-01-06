import urllib.request
import json
from datetime import datetime


def printResults(data):
    # Use the json module to load the string data into a dictionary
    theJSON = json.loads(data)
    # Created a new dict for our getted datas
    obj = {"Sıra": 0, "Item": "", "Fiyat": "", "Listeleneceği saat": "", " -----------------------------> ": "✓"}

    # We querying if it's a list. Cuz theJSON has can more data
    if type(theJSON) == list:

        # i converting list to dict
        for i in range(len(theJSON)):

            # now we can access the contents of the JSON like any other Python object
            for k,v in theJSON[i].items():

                if k == "name":
                    obj["Item"] = v

                if k == "price":
                    obj["Fiyat"] = "{:,d}".format(v)

                if k == "liveAt":
                    date = datetime.fromtimestamp(v).strftime("%H:%M:%S")
                    obj["Listeleneceği saat"] = date
                    obj["Sıra"] += 1

            for key,val in obj.items():
                print("""{} : {} """.format(key,val))

    # if theJSON is not list, it has 1 data and it's dict
    else:

        # now we can access the contents of the JSON like any other Python object
        for k,v in theJSON.items():

            if k == "name":
                obj["Item"] = v

            if k == "price":
                obj["Fiyat"] = v

            if k == "liveAt":
                date = datetime.fromtimestamp(v).strftime("%H:%M:%S")
                obj["Listeleneceği saat"] = date
                obj["Sıra"] += 1

        for key,val in obj.items():
            print("""{} : {}""".format(key,val))
        

def WaitList():
    # define a variable to hold the source URL
    # in this case we'll use the free data feed from the arsha.io
    # this feed lists Black Desert Online(MENA) Market Wait List
    # if u want use this for other server just change 'YourServer' from "https://api.arsha.io/v2/YourServer/GetWorldMarketWaitList"
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
    WaitList()

