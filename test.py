str="madhya-pradesh"

str=str.replace('-',' ')
str1=str[0].capitalize()
for i in range(1,len(str)):
    if str[i-1]==' ':
        str1+=str[i].capitalize()
    else:
        str1+=str[i]    

print(str1)