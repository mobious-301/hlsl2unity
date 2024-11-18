import pandas as pd
# 读取CSV文件
file_path = './cb2.csv'
csvList = pd.read_csv(file_path)

count=len(csvList)

#1 //name ("display name", Vector) = (number,number,number,number)
for i in range(0, count):
    csvList.replace("_v","_")
    Value=csvList.iloc[i,1].split(',')
    ValueCon=''
    for j in Value:
        j=j.replace("E","e")
        j=j.replace("e-0","e-")
        j=j.replace(" ","")
        #j=j.replace("e-","e+")
        j=float(j)
        j="%.10f" % j
        #print("%.10f" % j)
        ValueCon+=str(j)+','
    csvList.iloc[i,1]=ValueCon
    #print(csvList.iloc[i,1])
    end=csvList.iloc[i,0]+'("'+csvList.iloc[i,0]+'", Vector) = ('+csvList.iloc[i,1]+')'
    end=end.replace(",)",")")
    print(end)

for i in range(0, count):
    csvList.replace("_v","_")
    print(csvList.iloc[i,3]+' '+csvList.iloc[i,0]+';')