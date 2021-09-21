import requests
import csv

# csv file name
filename = "disabled.csv"
  
# initializing the titles and rows list
fields = []
rows = []

url = "https://cosmovision.smartolt.com/api/onu/bulk_disable"


# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
      
    # extracting field names through first row
    fields = next(csvreader)
  
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
  
    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))


#  printing first 5 rows
print('\nFirst 5 rows are:\n')
counter = 0
string = ""
for row in rows:
    # parsing each column of a row
    for col in row:
          counter += 1
          string += col + ","
          print(string)
          if counter == 10:
                string = string[:-1]
                counter = 0
                payload={'onus_external_ids': string}
                files=[

                ]
                headers = {
                   'X-Token': '78200d43cae043d597f0be1c5c66f0e5'
                 }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                print(response.text)
                string = ""

