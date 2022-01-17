class DairyProduct:

    def __init__(self,dairyId,dairyBrand,productType,Price,grade):
        self.dairyId=dairyId
        self.dairyBrand=dairyBrand
        self.productType=productType
        self.price=Price
        self.grade=grade


class ProductGrade:

    def __init__(self,dairyList,weightagedict):
        self.dairyList=dairyList
        self.weightageDict=weightageDict
    
    def priceBasedOnBrandAndType(self,dairyBrand,productType):
        li=[]
        j=0
        for i in self.dairyList:
            if i.dairyBrand==dairyBrand and i.productType==productType:
                li.append(self.dairyList[j])
            j+=1

        ans=[]
        for i in li:
            t=[]
            t.append(i.dairyBrand)
            update_price=i.price+i.price*self.weightageDict[i.grade]/100
            t.append(update_price)
            ans.append(t)     
        return ans

#INPUT THE SIZE OF THE LIST
n=int(input())

object_list=[]
for i in range(0,n):
    dairyId=int(input())
    dairyBrand=str(input())
    ProductType=str(input())
    Price=int(input())
    grade=str(input())

    obj=DairyProduct(dairyId,dairyBrand,ProductType,Price,grade)
    object_list.append(obj)
    
cntGrade=int(input())
weightageDict={}

for i in range(0,cntGrade):
    key=str(input())
    value=int(input())
    weightageDict[key]=value

dairyBrand=str(input())
ProductType=str(input())

obj_Product=ProductGrade(object_list,weightageDict)

print(obj_Product.priceBasedOnBrandAndType(dairyBrand,ProductType))