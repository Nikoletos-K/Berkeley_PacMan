# KONSTANTINOS NIKOLETOS
# 1115201700104
#buyLotsOfFruit.py

fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):

    totalCost = 0.0

    for fruit,pounds in orderList:

        if fruit in fruitPrices:
            totalCost += pounds*fruitPrices[fruit]
        else:
            print "Sorry we don't have %s" % (fruit)
            return None

    return totalCost


# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0) ]
    print 'Cost of', orderList, 'is', buyLotsOfFruit(orderList)
