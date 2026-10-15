import json
import streamlit as st
from pathlib import Path

#load budgetfile
Budget_file = Path(__file__).with_name('Budget.json')

def load_file():
    try:
        with Budget_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError: #when code runs first time no data
        #creates initial dict
        return {'Purchases': {'food': [] ,'shopping': [] ,'education': []},
             'Budget': {'food':0,'shopping':0,'education':0}}
    
    except json.JSONDecodeError as error:
        st.error(f"Could not read {Budget_file.name}: {error}")
        st.stop()

    # Validates both the outer wrapping dict and both inner dicts
    if (not isinstance(data, dict)
        or not isinstance(data.get("Purchases"), dict)
        or not isinstance(data.get("Budget"), dict)):

        st.error(f"{Budget_file.name} has an invalid format.")
        st.stop()
    return data

data = load_file()
purchases = data['Purchases']
budget = data['Budget']

def save_budget(data):
    with Budget_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

#Menu
#st.set_page_config(layout='wide')
st.title('Monthly Budget Tracking Programme',text_alignment='center')
st.header('Welcome!')
st.header('Track your spending more accurately')

#button
choice = st.radio(
    'Choose an action: ',
    ('1. Set up new budget',\
    '2. Log new purchase',\
    '3. View logged purchases',\
    '4. Check remaining budget',\
    '5. Delete logged purchase'),
    horizontal=True)

#func
if choice == '1. Set up new budget':
    with st.form('new_budget_form'):
        budget_category = st.text_input('Category: ').strip().lower()
        budget_amount = st.number_input('Amount($): ',min_value=0.0)
        submission = st.form_submit_button('Finalise goal')
    if submission: #if submitted
        if budget_category not in budget:
            st.error('No such category')
        elif budget[budget_category]!=0:
            st.error('Budget has been set before')
        elif budget_amount < 0:
            st.error('Enter a valid amount')
        else:
            budget[budget_category] += budget_amount
            save_budget(data)
            st.success(f'{budget_amount} set for {budget_category}')

elif choice == '2. Log new purchase':
    with st.form('purchase_form'):
        item_category = st.text_input('Category: ')
        item_puchased = st.text_input('Item purchased: ')
        item_cost = st.number_input('Item cost($): ' , min_value = 0.0)
        submission = st.form_submit_button('Done')
    if submission:
        if item_category.strip().lower() not in purchases:
            st.error('No such category')
        elif not item_cost or not item_puchased:
            st.error('Fields cannot be blank')
        else:
            purchases[item_category].append([item_puchased,item_cost])
            budget[item_category] -= item_cost
            if budget[item_category] < 0:
                st.warning(f'You have exceeded your budget for {item_category} by ${abs(budget[item_category])}')
            save_budget(data)
            st.success(f'{item_puchased} for {item_cost} logged')

elif choice=='3. View logged purchases':
    for cat in purchases:
        with st.expander(cat):
            for ind,elem in enumerate(purchases[cat]):
                st.markdown(f'{ind+1} : {elem[0]} for ${elem[1]}')
            save_budget(data)

elif choice == '4. Check remaining budget':
    for cat in budget:
            with st.expander(cat):
                st.markdown(f'${budget[cat]} left')
                save_budget(data)

elif choice == '5. Delete logged purchase':
    with st.expander('Clear entire programme'):
        if st.button('Confirm Deletion?'):
            with Budget_file.open("w", encoding="utf-8") as file:
                    json.dump({

'Purchases': {'food': [] ,'shopping': [] ,'education': []}, 'Budget': {'food':0,'shopping':0,'education':0}

                        }, file, indent=4)
            
    with st.expander('Delete specific logs'):
        with st.form('Del purchase'):
            del_cat = st.text_input('Which category: ').strip().lower()
            del_item = st.text_input('Name of item').strip().lower()
            submission = st.form_submit_button('Done')
            if submission:
                if del_cat not in purchases:
                    st.error('No such category')
                elif del_item not in purchases[del_cat]:
                    st.error('No such item purchased')
                else:
                    ind = data['Purchases'][del_cat].index(del_item)
                    with Budget_file.open("r", encoding="utf-8") as file:
                        data = json.load(file)
                    data['Purchases'][del_cat].pop(ind)
                    save_budget(data)
                    st.success('Item successfully deleted')
    
    