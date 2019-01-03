
def main():
    propertyPrice = input('Enter price of property in Number! Don''t anyhow! Program not handled!:  ')
    typeOfcitizenship = input("Type of citizenship: \n"
"S - Singaporean \n "
"P - Singapore Permanent Resident \n"
"F - Foreigner \n Enter citizen type: ")

    if typeOfcitizenship!='F':
        numberOfPastPurchased = input('Enter number of properties already purchased in Singapore: ')
    else:
        numberOfPastPurchased = 3

    BSD = calculateBSD(int(propertyPrice))
    ABSD_percentage = calculateAdditionaBuyerStamp(typeOfcitizenship, int(numberOfPastPurchased))
    TOTALRate = (ABSD_percentage*int(propertyPrice)) + BSD;

    print('Buyer stamp duty = ${} \n'.format(BSD))
    print('Total Stamp Duty Payable = ${} \n'.format(TOTALRate))

def calculateAdditionaBuyerStamp(typeOfCitizenship, noPastPurchase):
    data = {  'S' : {
                1: 0,
                2: 0.12,
                3: 0.15
            }, 'P' : {
                1: 0.05,
                2: 0.15,
                3: 0.15
            }, 'F' : {
                1: 0.20,
                2: 0.20,
                3: 0.20
            }
    }

    if noPastPurchase>=3:
        noPastPurchase = 3

    #print(data[typeOfCitizenship][noPastPurchase])
    return data[typeOfCitizenship][noPastPurchase]

def calculateBSD(propertyPrice):

    first = 180000
    next = 180000
    next2 = 640000
    remainingAmount = 0

    totalStampDuty = 0
    remainingAmtPrice = propertyPrice;
    milestone = 0
    result = 0
    for round in range(4):
        round = round + 1
        outputText = ''

        amountToMul = 0
        if remainingAmtPrice != 0:
            percentage = 0
            if round == 1:
                remainingAmount = remainingAmtPrice
                result = remainingAmount // first
                if result != 0:
                    percentage = 0.01
                    amountToMul = first
                    remainingAmount = remainingAmtPrice - first
                    milestone = milestone + amountToMul
                    outputText = 'first'

            elif round == 2:
                result = remainingAmount // next
                if result != 0:
                    percentage = 0.02
                    amountToMul = next
                    remainingAmount = remainingAmtPrice - next
                    milestone = milestone + amountToMul
                    outputText = 'next'

            elif round == 3:
                result = remainingAmount // next2
                if result != 0:
                    percentage = 0.03
                    amountToMul = next2
                    remainingAmount = remainingAmtPrice - next2
                    milestone = milestone + amountToMul
                    outputText = 'next'

            elif round == 4:
                # check whether still got any money left
                # print("remaining amount after 4 rounds {}".format(remainingAmount))
                # remainingAmount = 1000000
                if remainingAmount != 0:
                    percentage = 0.04
                    amountToMul = remainingAmount
                    milestone = milestone + amountToMul
                    outputText = 'remaining'
                # amountToMul = next2
                # remainingAmount = remainingAmtPrice - next
                # milestone = milestone + amountToMul

            totalStampDuty = totalStampDuty + (amountToMul * percentage)
            remainingAmtPrice = remainingAmount;
            print('remainingAmtPrice {} left to calculate'.format(remainingAmtPrice))
            interestCharge = (amountToMul * percentage)

            print('{}% of the {} S${}'.format(round, outputText, amountToMul) + ' S${}'.format(interestCharge))

    print("BSD payable .......... S${:7,.2f}".format(totalStampDuty))
    return totalStampDuty


main()




