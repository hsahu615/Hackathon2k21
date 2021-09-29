import pandas as pd
import requests
from flask import Flask, redirect, render_template, url_for, request
import json
import os

class hospital():

     # Extracting data from Rajasthan Govt. website
     def __init__(self, district):
         self.district = district
     def extraction(self):
         try:
             df = pd.read_html("https://covidinfo.rajasthan.gov.in/Covid-19hospital-wisebedposition-wholeRajasthan.aspx")[0]
             df.drop("S.No.", axis=1, level=0, inplace=True)
             a = []
             for i in df.columns:
                 a.append(i[1])

             # Data was in multi index so resetting index
             new_index = ["GenBed_Total", "GenBed_Occupied", "GenBed_Available", "OxyBed_Total", "OxyBed_Occupied",
                          "OxyBed_Available", "ICUBedWithoutVent_Total", "ICUBedWithoutVent_Occupied",
                          "ICUBedWithoutVent_Available", "ICUBedWithVent_Total", "ICUBedWithVent_Occupied",
                          "ICUBedWithVent_Available"]
             for i in range(12):
                 a[i + 2] = new_index[i]
             df.columns = a
             df.drop(0, axis=0, inplace=True)
             return df[df.District==self.district].values.tolist()
             #Converting dataframe to list so furthure it can be processed in JS
         except Exception as e:
             return e

class pharma():

    def __init__(self, city):
        self.city = city
    def pharmalist(self):
        try:
            pharmalist = [(17, "ajmer"), (28, "alwar"), (104, "banswara"), (110, "baran"), (116, "barmer"), (143, "bharatpur"), (150, "bhilwara"), (164, "bikaner"),(182, "bundi"), (224, "chittorgarh"), (227, "churu"), (248, "dausa"), (338, "jaipur"),(381, "jaisalmer"), (386, "jalore"), (399, "jhalawar"),(403, "jhunjhunu"), (379, "jodhpur"), (440, "karauli"), (488, "kota-rajasthan"), (600, "nagpur"),    (848, "pali-rajasthan"),(894, "pratapgarh"), (925, "rajsamand"), (673, "sawai-madhopur"), (692, "sikar"), (699, "sirohi"),     (716, "sri-ganganagar-rajasthan"), (767, "tonk"), (771, "udaipur-rajasthan")]
            code = 0
            city = ""
            for i in range(len(pharmalist)):
                if(self.city in pharmalist[i][1]):
                    code = pharmalist[i][0]
                    city = pharmalist[i][1]
                    break

            url = 'https://www.medicineindia.org/pharmacies-chemists-drugstores-in-city/' + str(code) + '/' + city + '/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            result = requests.get(url, headers=headers)
            pharma = pd.read_html(result.text)[0]
            return pharma.values.tolist()
        except Exception as e:
            return e
# Starting Flask work from here

app = Flask(__name__)


# District list unique districts
district_list = ['Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu',
                 'Jodhpur', 'Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer',
                 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittorgarh',
                 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Ganganagar',
                 'Hanumangarh', 'Karauli', 'Kota', 'Nagaur', 'Pali', 'Pratapgarh',
                 'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Tonk',
                 'Udaipur']
pharmalist = [(17, "ajmer"), (28, "alwar"), (104, "banswara"), (110, "baran"), (116, "barmer"),
              (143, "bharatpur"), (150, "bhilwara"), (164, "bikaner"),(182, "bundi"), (224, "chittorgarh"),
              (227, "churu"), (248, "dausa"), (338, "jaipur"),(381, "jaisalmer"), (386, "jalore"), (399, "jhalawar"),
              (403, "jhunjhunu"), (379, "jodhpur"), (440, "karauli"), (488, "kota-rajasthan"), (600, "nagpur"),
              (848, "pali-rajasthan"),(894, "pratapgarh"), (925, "rajsamand"), (673, "sawai-madhopur"), (692, "sikar"),
              (699, "sirohi"),     (716, "sri-ganganagar-rajasthan"), (767, "tonk"), (771, "udaipur-rajasthan")]
# Home page which have district list in select menu
@app.route('/')
def home_page():
    return render_template("index.html", district_list = district_list)

# page after district has been chosed
@app.route('/hospitals', methods=['POST', 'GET'])
def hospitalList():
    district = request.form.get("cars")
    a = hospital(district)
    dataset = a.extraction()
    return render_template("home.html", dataset = dataset, district_list = district_list)

@app.route('/hospital', methods=['POST', 'GET'])
def hos():
    return render_template("hospital.html",  district_list = district_list)

@app.route('/pharmacies', methods=['POST', 'GET'])
def pharmacylist():
    lis = []
    for i in range(len(pharmalist)):
        lis.append(pharmalist[i][1])
    return render_template("pharmaList.html", pharmalist = lis)
@app.route('/pharmaTable', methods=['POST','GET'])
def pharmaExtraction():
    lis=[]
    def pharmacylist():
        lis = []
        for i in range(len(pharmalist)):
            lis.append(pharmalist[i][1])

    selected_value = request.form.get('pharma')
    b = pharma(selected_value)
    b.pharmalist()
    return render_template('pharma_Table.html', dataset = b.pharmalist(), pharmalist = lis)

@app.route('/about')
def about():
    return render_template('about.html')


# port = os.getenv("PORT")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)
