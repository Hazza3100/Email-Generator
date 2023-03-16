# -*- coding: utf-8 -*-
# Time       : 16/03/23 11:55
# Author     : Hazza3100
# Github     : https://github.com/Hazza3100
# Description: 🚀 Email Generator

import threading
import requests
import customtkinter


class Gui(customtkinter.CTk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		customtkinter.set_appearance_mode("Dark")
		customtkinter.set_default_color_theme("green")

		self.iconbitmap("Assets/email.ico")
		self.title("Email Generator")
		self.resizable(0,0)
		self.geometry(f"{270}x{410}")

		# Apikey Label
		self.apikeyLabel = customtkinter.CTkLabel(self, text="API Key")
		self.apikeyLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

		# Apikey Entry Field
		self.ApiKeyEntry = customtkinter.CTkEntry(self, placeholder_text="57evkle0bw93adqw79zbez2rbjpozy1u")
		self.ApiKeyEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

		# Amount Label
		self.amountLabel = customtkinter.CTkLabel(self, text="Amount")
		self.amountLabel.grid(row=1, column=0,padx=20, pady=20, sticky="ew")

		# Amount Entry Field
		self.amountEntry = customtkinter.CTkEntry(self, placeholder_text="2")
		self.amountEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

		# Type Label
		self.occupationLabel = customtkinter.CTkLabel(self, text="Mail Type")
		self.occupationLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

		# Email Type combo box
		self.typeOptionMenu = customtkinter.CTkOptionMenu(self, values=['Outlook', 'Hotmail', 'Outlook Trusted', 'Hotmail Trusted'])
		self.typeOptionMenu.grid(row=4, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

		# Generate Button
		self.generateResultsButton = customtkinter.CTkButton(self, text="Generate Results", command=self.generateEmailProcess)
		self.generateResultsButton.grid(row=5, column=0, columnspan=2, padx=65, pady=20, sticky="ew")

		# Result Box
		self.displayBox = customtkinter.CTkTextbox(self, width=200, height=100)
		self.displayBox.grid(row=6, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")


	def convert(self, vnd_amount: int) -> int:
		response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
		exchange_rate = response.json()["rates"]["VND"]
		usd_amount = vnd_amount / exchange_rate
		return f'{usd_amount:.2f}'
	
	def __balance__(self, apikey) -> str:
		return requests.get(f'https://api.hotmailbox.me/user/balance?apikey={apikey}').json()

	def get_email(self, etype: str, apikey: str):
		response = requests.get(f'https://api.hotmailbox.me/mail/buy?apikey={apikey}&mailcode={etype.upper()}&quantity=1')
		if response.json()['Code'] == 0:
			self.displayBox.insert('0.0', f"{response.json()['Data']['Emails'][0]['Email']}:{response.json()['Data']['Emails'][0]['Password']}\n")
		else:
			self.displayBox.insert('0.0', 'Error Fetching Email\n')

	def generateEmailProcess(self):
		apikey = self.ApiKeyEntry.get()
		amount = self.amountEntry.get()
		etype  = self.typeOptionMenu.get()
		if apikey == '':
			self.displayBox.insert('0.0', 'Invalid api key\n')
			return
		if amount == '':
			self.displayBox.insert('0.0', 'Invalid Amount\n')
			return
		else:
			x = self.__balance__(apikey)
			if x['Message'] == 'Thành công':
				balanceVND = x['Balance']
				USDBalance = self.convert(balanceVND)
				if float(USDBalance) > 0.002222:
					for i in range(int(amount)):
						threading.Thread(target=self.get_email, args=(etype, apikey,)).start()
				else:
					self.displayBox.insert('0.0', 'Insufficient funds\n')
			else:
				self.displayBox.insert('0.0', 'Invalid api key\n')


if __name__ == "__main__":
	app = Gui()
	app.mainloop()
