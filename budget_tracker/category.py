catalogue={'food':(),'shopping':(),'education':()}
budget={'food':0,'shopping':0,'education':0}
def make_purchase():
    item=input('Item purchased: ')
    amount=round(float(input('Amount spent: ')),2)
    return(item,amount)
def log():
    while True:
        purchase=make_purchase()
        category=input('Which category: ')
        if category not in catalogue:
            print('No such category')
            continue    
        catalogue[category]+=(purchase,)
        breaker=input('Continue logging?: ')
        if breaker=='no':
            return 'Done'
def show_items(catalogue):
    while True:
        category=input('Check which category:')
        if category not in catalogue:
            print('No such category')
            continue
        print(catalogue[category])
        breaker2=input('Check another category?: ')
        if breaker2=='no':
            return 'Done'
def budget_tracker(budget):
    while True:
        budget_cat=input('Which category for budget: ')
        if budget_cat not in budget:
            print('No such category')
            continue
        goal=int(input('Budget goal to set: '))
        budget[budget_cat]+=goal
        next=input('Continue budget setting?: ')
        if next=='no':
            return 'Done'
def budget_calc(budget):
    while True:
        select=input('Check budget left for which category: ')
        if select not in budget:
            print('No such category')
            continue
        amount_spent=0
        for item in catalogue[select]:
            amount_spent+=item[1]
        amount_left=budget[select]-amount_spent
        if amount_left>=0:
            print('Budget left: '+str(amount_left))
            next=input('Check budget for another category?: ')
        else:
            print('Budget exceeded by: '+ str(abs(amount_left)))
            next=input('Check budget for another category?: ')
        if next=='no':
            return 'Done'

        
