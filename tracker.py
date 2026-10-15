#budget=round(float(input('Enter desired budget: ')),2)
def tracker(budget1):
    counter=0
    total=()
    while budget>0:
        purchase=make_purchase()
        if purchase[1]<0:
            continue
        total+=(purchase[0],)
        budget-=purchase[1]       
        counter+=1
        if purchase[0]=='0':
            return 'Budget left: '+str(round(budget,2))+' Purchases: '+str(counter)+' Items bought: '+str(total)
    if budget<0:
        return 'You exceeded by: $'+str(abs(round(budget,2)))+' Purchases: '+str(counter)+' Items bought: '+str(total)
    elif budget==0:
        return 'Purchases: '+str(counter)+' Items bought: '+str(total)
def make_purchase():
    item=input('Item purchased: ')
    amount=round(float(input('Amount spent: ')),2)
    return (item,amount)

def simple_budget():
    budget=int(input('Enter budget goal: '))
    if budget<=0:
        return 'Invalid amount'
    expenditure=int(input('Enter amount spent: '))
    if expenditure<=0:
        return 'Invalid amount'
    if expenditure>budget:
        amount=expenditure-budget
        return'Uh oh, you exceeded your budget by: $'+str(amount)
    elif expenditure==budget:
        return 'You have finished your budget, no more spending'
    else:
        leftover=round((budget-expenditure)*100/budget,2)
        return 'Percentage of budget left: '+str(leftover)+"%"
