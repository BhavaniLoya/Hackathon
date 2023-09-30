import pandas as pd

class Savings:
    def read(self):
        df= pd.read_excel('GrowDataBank.xlsx',sheet_name='Savings Accoun Transaction Data')
        df= df[' Customer_ID     Amount   Transaction_Type  Transaction_Date '].str.strip()
        savings = df.str.split('\s+',  expand=True)
        savings.columns = ['Account_Id','Amount','Transaction_Type','Transaction_Date']
        savings.dropna(inplace=True)
        return savings

    def  number_of_customers(self):
        df=Savings.read(self)
        customers=df['Account_Id'].unique()
        # print(customers)
        return customers


    def transaction_history(self,user_id):
        df=Savings.read(self)
        if df.empty:
            return f"There is no customer with customer id {user_id} in GrowDataBank"  
        cust_trans=df[df['Account_Id']==user_id]
        if cust_trans.empty:
            return f"User with ID {user_id} doesn't exist in the GrowDataBank."    
        cust_trans=cust_trans.sort_values(by='Transaction_Date',ascending=False)
        latest_10_transaction_history=cust_trans.head(10)
        return latest_10_transaction_history
    
    def statement(self,user_id):
        df=Savings.read(self)
        if df.empty:
            return f"There is no customer with customer id {user_id} in GrowDataBank"  
        cust_trans=df[df['Account_Id']==user_id]
        if cust_trans.empty:
            return f"User with ID {user_id} doesn't exist in the GrowDataBank."    
        statement=cust_trans.sort_values(by='Transaction_Date')
        return statement   

    def current_balance(self,user_id):
        df=Savings.transaction_history(self,user_id)
        # print(df)
        #performing sum on transaction_type as Credit 
        if df.empty:
            return f"There is no customer with customer id {user_id} in GrowDataBank"          
        credit= df[df['Transaction_Type']=='Credit']
        credit['Amount']=credit['Amount'].astype(float)
        credit_value=credit['Amount'].sum()
        # print("Sum of credit_value':", credit_value)
        #performing sum on transaction_type as Debit     
        debit= df[df['Transaction_Type']=='Debit']
        debit['Amount']=debit['Amount'].astype(float)
        debit_value=debit['Amount'].sum() 
        balance=credit_value-debit_value
        return balance
    


class Loan:
    def read(self):
        df=pd.read_excel('GrowDataBank.xlsx',sheet_name='Loan Account Data')
        return df
    
    def outstanding_amount(self,user_id):
        df=Loan.read(self)
        if df.empty:
            return f"There is no customer with customer id {user_id} in GrowDataBank"          
        df=df[df['Account_id']==user_id]
        if df.empty:
            return f"There is no customer with customer id {user_id} in GrowDataBank"          
        loan_amount=df['Loan Amount']
        recovered_til_now=df['Recovered Till Now']
        outstanding_amount=loan_amount-recovered_til_now
        return int(outstanding_amount)   

   
    def loan_status(self,user_id):
        df=Loan.read(self)
        if df.empty:
            return f"There is no customer with customer id {user_id} in Loan Department  GrowDataBank"          
        df=df[df['Account_id']==user_id]
        if df.empty:
            return f"There is no customer with customer id {user_id} in Loan Department "   
        loan_amount=df['Loan Amount'].iloc[0]
        recovered_till_now=df['Recovered Till Now'].iloc[0]
        if loan_amount==recovered_till_now:
            return f"Loan Status is NILL for this customer id {user_id}"
        else:
            a=Loan.outstanding_amount(self,user_id=user_id)
            return f"Loan Status is Acitve for this customer {user_id} and amount that needs to be paid is {a}"
  
class Credit:
    def read(self):
        df=pd.read_excel("GrowDataBank.xlsx",sheet_name="Credit Card Data")
        return df

    def credit_card_offering(self):
        df=Credit.read(self)
        if df.empty:
            return f"There are no customers in GrowDataBank"  
        # print(df)        
        card_limit_avergae=int(df['Card Limit'].mean())
        no_of_transactions_average=int(df['Number of Transactions'].mean())
        cur_out_bill_average=int(df['Current Outstanding Bill'].mean())
        #df= df[(df['Number of Transactions']>no_of_transactions_average) & (df['Number of Missed Payments']==0)]
        df = df[(df['Number of Missed Payments'] == 0) & (df['Number of Transactions']  >=15)]
        if df.empty:
            return "No User is eligible for Credit Card Offering"
        id=df['Account_Id'].tolist()        
        return id

    
    def npa_identification(self):
        df=Credit.read(self)
        if df.empty:
            return f"There are no customers in GrowDataBank"          
        df=df[df['Number of Missed Payments']>0]
        if df.empty:
            return "There are No NPA Customers in this GrowDataBank"
        id=df['Account_Id'].tolist()
        return id

    def credit_status(self,user_id):
        df=Credit.read(self)
        if df.empty:
            return "No Records Present in the Credit Card Department in the GrowDataBank"
        df=df[df['Account_Id']==user_id]
        if df.empty:
            return f"There is no customer with customer id {user_id} in credit status department of GrowDataBank Branch"
        df=df[(df['Current Outstanding Bill']!=0) & (df['Number of Transactions']>0)]
        if df.empty:
            return 'There are no records in credit_status  active filter dataframe'
        a=df['Account_Id']
        b=df['Current Outstanding Bill']
        return a
       

savings_account=Savings()
loan_account=Loan()
credit_card=Credit()
# id=input("Enter the Customer_ID:")
id='cust_idno_1002'


print(f' List of Customers in Grow Data Skills Branch is :',savings_account.number_of_customers())
print(f' Transaction history of {id} is as mentioned below:','\n',savings_account.transaction_history(id))
print(f' Balance amount for {id} is:',savings_account.current_balance(id))
print(f'Bank statment for the custormer{id} is :',savings_account.statement(id))




print(loan_account.read())
print(f'Outstanding amount for the customer {id} is :', loan_account.outstanding_amount(id))
status =loan_account.loan_status(id)
print(status)


print(credit_card.read())
credit_card_offering=credit_card.credit_card_offering()
print(f'Below mentioend are the list of  Customers who are eligible for the credit card limit increase:','\n')
print(credit_card_offering)
NPA_list=credit_card.npa_identification()
print(f'Below mentioend are the list of NPA Customers who has failed to pay the EMI"s atleast once:','\n')
print(NPA_list)
active_act=credit_card.credit_status(id)
print(f'The user {active_act} is active and has  outstanding credit bill')


def financial_summary(user_id):
    a=savings_account.current_balance(user_id=user_id)
    b=savings_account.transaction_history(user_id)
    c=loan_account.loan_status(user_id)
    d=credit_card.credit_status(user_id)
    return a,b,c,d

current_balance,transaction_history,loan_status,credit_status=financial_summary(user_id=id)
print(f'Customer with {id}''s current balance in GrowDataBank is ',current_balance)
print(f'Customer with {id} ''s transaction history in GrowDataBank is ','\n',transaction_history)
print(loan_status)
print(credit_status)











