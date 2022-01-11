import pandas as pd

input('Press any key for starting....')
df_lad = pd.read_csv('theladders_dataset.csv')
df_usj = pd.read_csv('us.jora_dataset.csv')
df_ind = pd.read_csv('indeed_dataset.csv')

#print(df1.append(df2))
df_ = df_ind.append(df_lad)
df_ = df_.append(df_usj)

df_.to_csv(r"result_dataset.csv",encoding="utf-8",index=False,mode="w")
print("Done.\ncontact:berkaycihan@icloud.com")