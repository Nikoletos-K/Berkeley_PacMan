# KONSTANTINOS NIKOLETOS
# 1115201700104
# shopSmart.py

import shop

def shopSmart(orderList, fruitShops):

    ShopPrices=[]
    ShopPrices.append(fruitShops[0].getPriceOfOrder(orderList))     # Initialazing the list

    for shop in fruitShops:
        price=shop.getPriceOfOrder(orderList)           # Gets the current price for every shop
        ShopPrices.append(price)                        # Informing the list
        if price <= min(ShopPrices):                    # Checking for the minimum
            Wanted_Shop=shop


    if Wanted_Shop!=None:
            return Wanted_Shop

    return None

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print "For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName()
  orders = [('apples',3.0)]
  print "For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName()
