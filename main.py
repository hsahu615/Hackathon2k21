import pandas as pd

class hospital():

     # Extracting data from Rajasthan Govt. website
     def __init__(self, city):
         self.city = city
     def extraction(self):
         df = pd.read_html("hospital.html")
         df = df[0]
         df.drop("S.No.", axis=1, level=0, inplace=True)
         a = []
         for i in df.columns:
             a.append(i[1])
         new_index = ["GenBed_Total", "GenBed_Occupied", "GenBed_Available", "OxyBed_Total", "OxyBed_Occupied",
                      "OxyBed_Available", "ICUBedWithoutVent_Total", "ICUBedWithoutVent_Occupied",
                      "ICUBedWithoutVent_Available", "ICUBedWithVent_Total", "ICUBedWithVent_Occupied",
                      "ICUBedWithVent_Available"]
         for i in range(12):
             a[i + 2] = new_index[i]
         df.columns = a
         df.drop(0, axis=0, inplace=True)
         return df[df.District=="Jaipur"].values.tolist()

a = hospital("Jaipur")
b = a.extraction()
print(b)
