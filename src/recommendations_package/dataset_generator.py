import random
import pandas as pd

df = pd.DataFrame(columns=["rate", "user_id", "obj_id","obj_title"])
arr = []
for i in range(1,2500):
    dict = {'rate':random.randint(-1,1),'user_id':random.randint(1,5),
            'obj_id':random.randint(1,10), "obj_title":"title_"+str(i)}
    rate = random.randint(-1,1)
    user_id = random.randint(1,100)
    obj_id = random.randint(1,100)
    obj_title = "title_"+str(obj_id)
    struct = (rate,user_id,obj_id,obj_title)
    arr.append(struct)

dfObj = pd.DataFrame(arr, columns=["rate", "user_id", "obj_id", "obj_title"])
print(dfObj)
dfObj.to_csv("W:\programms\dbeaver\sample db\sampledata.csv", index=False)
print(dfObj)