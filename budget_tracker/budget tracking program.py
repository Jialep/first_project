from budget_tracker.category import catalogue,log,show_items,budget_tracker,budget,budget_calc
def main_menu():
    print('Select a function')
    print('1. Set up budget goals')
    print('2. Log a new purchase')
    print('3. View logged purchases')
    print('4. Check budget left')
    print('5. Exit program')
    choice=int(input('Select 1,2,3,4 or 5: '))
    while True:
        if choice==1:
            print(budget_tracker(budget))
            choice=int(input('Select 1,2,3,4 or 5: '))
        elif choice==2:
            print(log())
            choice=int(input('Select 1,2,3,4 or 5: '))
        elif choice==3:
            print(show_items(catalogue))
            choice=int(input('Select 1,2,3,4 or 5: '))
        elif choice==4:
            print(budget_calc(budget))
            choice=int(input('Select 1,2,3,4 or 5: '))
        elif choice==5:
            return 'Finished'
        else:
            print('Invalid input, retry')
            choice=int(input('Select 1,2,3,4 or 5: '))
print(main_menu())