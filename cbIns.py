import csv
from cbfhlsl import *
def parse_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            value = row['Value']
            data.append((name, value))
    return data

def getcbinsFP(file_path):
    parsed_data = parse_csv(file_path)

    def setpsCb(Value :str):
        Value=Value.split(',')
        ValueCon=''
        temp=[]
        end=''
        for j in Value:
            j=j.replace("E","e")
            j=j.replace("e-0","e-")
            j=j.replace(" ","")
            #j=j.replace("e-","e+")
            j=float(j)
            if abs(j)<0.00001:
                j=0
            # j="%.10f" % j
            #print("%.10f" % j)
            temp.append(str(j))
            # ValueCon+=str(j)+','
        end=",".join(temp)
        return end

    # 打印解析结果
    psCb = []
    for name, value in parsed_data:
        # outstr.append(f"{name}: {value}")
        psCb.append(f'_{name}("{name}",Vector)=({setpsCb(value)})')
        # print(f"{name}: {value}")
    print(psCb)

    psCb1=[]
    # psCb1.append(f"float4[{len(parsed_data)}] cb0;") 
    for i ,(name, value)  in enumerate(parsed_data):
        # outstr.append(f"{name}: {value}")
        psCb1.append(f"float4 _{name};")
    print(psCb1)

    psCbname=[]
    for i ,(name, value)  in enumerate(parsed_data):
        # outstr.append(f"{name}: {value}")
        psCbname.append(f"{name.split('_v')[0]}[{name.split('_v')[1]}]")
    print('psCbname')
    print(psCbname)

    psCbCon = []
    for i ,(name, value)  in enumerate(parsed_data):
        # outstr.append(f"{name}: {value}")
        psCbCon.append(f"cb0[{i}] = _{name};")
        # print(f"{name}: {value}")
    # print(psCbCon)
        endpsCb =[]
    endpsCb1 =[]
    endpsCbCon =[]
    endpsCbname = []


    Cbfhlsl =getCbfhlsl()
    for i ,( value)  in enumerate(psCbname):
        print(value in Cbfhlsl)
        key = value in Cbfhlsl
        if not key:
            psCb[i]= ''
            psCb1[i]= ''
            psCbCon[i]= ''
        else:
            endpsCb.append(psCb[i])
            endpsCb1.append(psCb1[i])
            endpsCbCon.append(psCbCon[i])
            endpsCbname.append(psCbname[i])

            
            # print(psCb[i] )
            # print(psCb1[i])
            # print(psCbCon[i])
    print(endpsCbname)
    #用组合而不是继承
    return endpsCb,endpsCb1,endpsCbCon,endpsCbname

def getcbIns():
    # 示例文件路径

    file_path = ['./cbs/cb0.csv','./cbs/cb1.csv']
    endpsCb,endpsCb1,endpsCbCon,endpsCbname=[],[],[],[]
    for value in file_path:
        psCb,psCb1,psCbCon,psCbname = getcbinsFP(value)
        endpsCb+=(psCb)
        endpsCb1+=(psCb1)
        endpsCbCon+=(psCbCon)
        endpsCbname+=(psCbname)
    print(endpsCb)
    return endpsCb,endpsCb1,endpsCbCon,endpsCbname

        

        
getcbIns()

