import sqlite3 as sq3
from getpass import getpass
import re
from datetime import datetime
import hashlib
import os
from time import sleep


conn=sq3.connect('aa.db')
cursor=conn.cursor()


print("D-2 Bank Management System\n")

def clear():
	if os.name=='nt':
		os.system('cls')
	else:
		os.system('clear')



q1='''
	CREATE TABLE IF NOT EXISTS User(
	Name VARCHAR(20),
	Accno INTEGER PRIMARY KEY AUTOINCREMENT,
	ContactNo VARCHAR(10),
	Cash INTEGER,
	Password VARCHAR(255)
	CHECK (LENGTH(ContactNo)=10)
	);

	'''
cursor.execute(q1)

q2='''
	CREATE TABLE IF NOT EXISTS Transactions(
	Id INTEGER PRIMARY KEY AUTOINCREMENT,
	Accno INTEGER,
	Amount INTEGER,
	Type VARCHAR(6),
	CreatedOn DateTime,
	FOREIGN KEY(Accno) REFERENCES User(Accno)
	);

	'''
cursor.execute(q2)

q3='''
	CREATE TABLE IF NOT EXISTS Transfer(
	Id INTEGER PRIMARY KEY AUTOINCREMENT,
	Amount INTEGER,
	Sender INTEGER,
	Receiver INTEGER,
	CreatedOn DateTime,
	FOREIGN KEY(Sender) REFERENCES User(Accno)
	FOREIGN KEY(Receiver) REFERENCES User(Accno)
	);

	'''
cursor.execute(q3)



# sleep(1)
clear()
class User:

	def __init__(self,account_number):
		self.account_number = int(account_number)


	def display_profile(self):

		fetch_user_query = '''
								SELECT Name,ContactNo,Cash FROM User
								WHERE Accno={};

							'''.format(self.account_number)

		
		cursor.execute(fetch_user_query)
		user_data = cursor.fetchone()

		clear()					
		print("Name:",user_data[0])
		print("Contact Number",user_data[1])
		print("Total available cash {}₹".format(user_data[2]))  # Display User profile  


	def total_balance(self):

		fetch_user_query = '''
								SELECT Cash FROM User
								WHERE Accno={};

							'''.format(self.account_number)

		
		cursor.execute(fetch_user_query)
		user_data = cursor.fetchone()

		sleep(1)
		clear()
		print("Total available balance is {}₹".format(user_data[0]))    # Check total balance of user    
		
	def transfer_money(self, amount, send_to_account):
		
		update_user_cash_query = '''UPDATE User SET Cash=Cash-{} WHERE Accno={};'''.format(amount,self.account_number)
		cursor.execute(update_user_cash_query)

		update_user_cash_query = '''UPDATE User SET Cash=Cash+{} WHERE Accno={};'''.format(amount,send_to_account)
		cursor.execute(update_user_cash_query)

		insert_transfer_entry = '''INSERT INTO TRANSFER(Amount,Sender,Receiver,CreatedOn) VALUES({},{},{},"{}");'''.format(amount, self.account_number, send_to_account, datetime.now())
		cursor.execute(insert_transfer_entry)

		conn.commit()   # To transfer money from one user account to another 

	def deposit(self,amount):
		deposit_amount_query = '''
				UPDATE User
				SET Cash=Cash+{}
				WHERE Accno={}
				'''.format(amount, self.account_number)

		cursor.execute(deposit_amount_query)

		insert_transactions_entry = '''INSERT INTO Transactions(Accno,Amount,Type,CreatedOn) VALUES({},{},"{}","{}");'''.format(self.account_number,amount,"Credited", datetime.now())
		cursor.execute(insert_transactions_entry)

		conn.commit()		  # Deposit money to user   

	def withdraw(self,amount):
		withdraw_amount_query = '''
				UPDATE User
				SET Cash=Cash-{}
				WHERE Accno={}
				'''.format(amount, self.account_number)

		cursor.execute(withdraw_amount_query)

		insert_transactions_entry = '''INSERT INTO Transactions(Accno,Amount,Type,CreatedOn) VALUES({},{},"{}","{}");'''.format(self.account_number,amount,"Debited", datetime.now())
		cursor.execute(insert_transactions_entry)

		conn.commit()		  # Withdraw money from user    

	def update_contact(self,mobile_number):
		update_contact_query = '''
				UPDATE User
				SET ContactNo="{}"
				WHERE Accno={}
				'''.format(mobile_number,self.account_number)

		cursor.execute(update_contact_query)
		conn.commit()		  # Update contact of user  

	def update_pass(self,password):
		password_hash = hashlib.sha384(password.encode()).hexdigest()
		update_password_query = '''
				UPDATE User
				SET Password="{}"
				WHERE Accno={}
				'''.format(password_hash,self.account_number)

		cursor.execute(update_password_query)
		conn.commit()	   # Update password of user 

	def transaction_table(self):
		transaction_query_table = ''' 
									SELECT Amount,Type,CreatedOn FROM Transactions
									WHERE Accno={};
									'''.format(self.account_number)
		cursor.execute(transaction_query_table)
		conn.commit()   # Details of credits and debits of money

	def menu(self):

		user_choice=1
		while user_choice!="9":
			sleep(2)
			clear()
			print("PROCEED",end="\n\n")
			print("1: PROFILE")
			print("2: BALANCE CHECK")
			print("3: TRANSFER MONEY")
			print("4: DEPOSIT MONEY")
			print("5: WITHDRAW")
			print("6: CHANGE CONTACT NUMBER")
			print("7: CHANGE PASSWORD")
			print("8: TRANSACTION HISTORY")
			print("9: MAIN MENU")
	
			user_choice=input()

			if user_choice=='1': #Display Profile
				self.display_profile()

			elif user_choice=='2': #Balance Check
				self.total_balance()

			elif user_choice=='3':
				while True:
					clear()
					send_to_account = input("ENTER AN ACCOUNT NUMBER IN WHICH YOU WANT TO TRANSFER: ")
					find_account_exist_query = '''SELECT Accno FROM User WHERE Accno={};'''.format(send_to_account)
					cursor.execute(find_account_exist_query)
					if cursor.fetchone() and int(send_to_account)!=self.account_number:
						send_to_account = int(send_to_account)
						break
					else:
						print("Account Number Is Invalid\n")

				while True:
					clear()
					amount = input("ENTER AMMOUNT YOU WANT TO TRANSFER: ")
					if re.fullmatch("^[1-9]\d*$", amount):
						find_account_exist_query = '''SELECT Cash FROM User WHERE Accno={};'''.format(self.account_number)
						cursor.execute(find_account_exist_query)
						if cursor.fetchone()[0] >= int(amount):
							amount = int(amount)
							break
						else:
							print("Insufficient Amount\n")
					else:
						print("Enter a Valid Amount")

				self.transfer_money(amount, send_to_account)

				print("Transfer Completed Successfully")

			elif user_choice=='4':

				while True:
					amount = input("ENTER AMMOUNT YOU WANT TO DEPOSIT: ")
					if re.fullmatch("^[1-9]\d*$", amount):
						amount = int(amount)
						break
					else:
						print("Enter a Valid Amount")

				self.deposit(amount)	

			elif user_choice=='5':

				while True:
					clear()
					amount = input("ENTER AMMOUNT YOU WANT TO WITHDRAW: ")
					if re.fullmatch("^[1-9]\d*$", amount):
						find_account_exist_query = '''SELECT Cash FROM User WHERE Accno={};'''.format(self.account_number)
						cursor.execute(find_account_exist_query)
						if cursor.fetchone()[0] >= int(amount):
							amount = int(amount)
							break
						else:
							print("Insufficient Amount\n")
					else:
						print("Enter a Valid Amount")

				self.withdraw(amount)

			elif user_choice=='6':

				while True:
					clear()
					print("ENTER YOUR NEW 10 DIGIT PHONE NUMBER")
					mobile_number = input()
					if re.fullmatch("^[6-9]\d{9}$", mobile_number):
						break
					else:
						print("Enter a valid number")
						pass

				self.update_contact(mobile_number)

			elif user_choice=='7':

				while True:
					clear()
					print("ENTER NEW PASSWORD\n")
					password = getpass()
					if re.fullmatch("^[\w!@#$%^&*()<>?:\s]{4,}$", password): 
						break
					else:
						print("ENTER A PASSWORD WITH LENGTH GRATER THEN 3", end="\n\n")

				self.update_pass(password)

				break

			elif user_choice=='8':
				self.transaction_table()
				print(*(cursor.fetchall()))



			elif user_choice=='9':
				break	

			else:
				clear()
				print("Wrong Entry")
				print("Try Again\n")  # Main menu of user  

				



# Main Menu
while(True):
	# sleep(1)
	clear()
	print("Press 1 for Login")
	print("Press 2 for REGISTRATION")
	print("Press 3 for exit")
	choice=input()

	# Login
	if choice=='1':
		while True:
			try:
				account_number = int(input("ENTER ACCOUNT NUMBER\n"))
				break
			except ValueError:
				pass

		print("ENTER YOUR PASSWORD")
		password = getpass()
		password_hash = hashlib.sha384(password.encode()).hexdigest()


		registration_check_query = '''
			SELECT * FROM User
			WHERE Accno={}

			;'''.format(account_number)

		cursor.execute(registration_check_query)
		user_data=cursor.fetchone()


		if user_data==None:
			print("INFORMATION IS INVALID", end="\n\n")
			break
		elif password_hash!=user_data[4]:
			print("INFORMATION IS INVALID", end="\n\n")
			break
		else:
		
			user_object=User(account_number)
			user_object.menu()
	
	# Registration
	elif choice=='2':

		# Registration Menu
		while True:
			clear()
			print("ENTER REGISTRATION INFO")
			
			# Name of user
			while True:	
				print("ENTER YOUR NAME")
				name = input()
				if re.fullmatch("^[a-zA-Z]+(\s[a-zA-Z]+)*", name):
					break
				else:
					print("ENTER A VALID NAME")	   
			
			# Phone number of user
			while True:
				clear()
				print("ENTER YOUR 10 DIGIT PHONE NUMBER")
				mobile_number = input()
				if re.fullmatch("^[6-9]\d{9}$", mobile_number):
					break
				else:
					print("Enter a valid number")
					pass	

			# Amount to be deposited 
			while True:
				clear()
				print("ENTER AMOUNT YOU WANT TO START WITH GREATER THEN ZERO")
				amount = input()
				if re.fullmatch("^[1-9]\d*$", amount):
					amount = int(amount)
					break
				else:
					print("ENTER A VALID AMOUNT")
					print()
			
			# Password of user			
			print("ENTER YOUR PASSWORD")
			print("REMINDER: DON'T SHARE PASSWORD WITH ANYONE")

			while True:
				password = getpass()
				if re.fullmatch("^[\w!@#$%^&*()<>?:]{4,}$", password): 
					break
				else:
					print("ENTER A PASSWORD WITH LENGTH GRATER THEN 3")
				
			password_hash = hashlib.sha384(password.encode()).hexdigest()
			
			# insert into table
			create_user_query='''
				INSERT INTO User(Name,ContactNo,Cash,Password)
				VALUES("{}","{}",{},"{}")

				'''.format(name,mobile_number,amount,password_hash);

			cursor.execute(create_user_query)
			conn.commit()

			# fetch account number
			q3='''
				SELECT * FROM User
				ORDER BY Accno DESC;

				'''
			cursor.execute(q3)
			acc_no = cursor.fetchone()[1]	
			print("SUBMISSION SUCSESSFULLY DONE")
			print("YOUR ACCOUNT NUMBER IS ", acc_no)
			sleep(2)

			# insert into transaction table
			insert_transactions_entry = '''INSERT INTO Transactions(Accno,Amount,Type,CreatedOn) VALUES({},{},"{}","{}");'''.format(acc_no,amount,"Credited", datetime.now())
			cursor.execute(insert_transactions_entry)
			conn.commit()		

			break

	#Exit
	elif choice=='3':
		break
	else:
		print("Wrong Entry")
		print("Try Again\n")
																													