import tkinter as tk
from tkinter import messagebox
import sys
import random
import os
import hashlib
from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH, LTC, BCH, BSV, DASH, ZEC, DOGE, BTCTEST
from monero.seed import Seed
import qrcode
import pdfkit
from os.path import exists
import subprocess
import bitcash
from bitcash import Key


# Obtain secure random numbers
system_random = random.SystemRandom()
# Global variables
half_key = None
sec_half_key = None
coin_sel = None


# Generate QR codes from strings
def makeqr(keystr, filename):
    img = qrcode.make(keystr)
    type(img)
    filename = 'PaperWallet/' + filename
    img.save(filename)


# Show popup when user does some shit
def show_popup(message):
    popup = tk.Tk()
    popup.title("WARNING!")
    label = tk.Label(popup, text=message)
    label.pack()
    ok_button = tk.Button(popup, text="Ok", command=popup.destroy)
    ok_button.pack()
    popup.mainloop()


class FirstWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Operator 1")
        self.master.geometry("450x150")

        self.input_label = tk.Label(master, text="Type some random text:")
        self.input_label.pack()

        self.input_text = tk.Entry(master)
        self.input_text.pack()

        # Opens a pdf with the part of the private key and QR codes
        self.button1 = tk.Button(master, text="Generate first half key", command=self.gen_first_half, bg="black", fg="blue")
        self.button1.pack()

        # Closes and deletes pdf file and qr code and shows a new window for the second user
        self.button2 = tk.Button(master, text="End, 2nd operator\'s turn", command=self.new_user_turn, bg="black", fg="blue")
        self.button2.pack()

    def gen_first_half(self):
        global half_key
        input_text = self.input_text.get()
        if input_text == '':
            show_popup('Please insert some text in the proper box before generating the 1/2 part of the private key')
        elif exists('PaperWallet/halfkey1.pdf'):
            show_popup('You already created the first part of th private key, click on the other button to go to the next step')
        else:
            # Add random system entropy
            extra_ent = str(system_random.randint(0, sys.maxsize))
            extra_ent += str(system_random.randint(0, sys.maxsize))
            # create entropy source joining random word to random system entropy
            ent_source = input_text + extra_ent
            # obtain first 128 bits of the private key
            half_key = hashlib.md5(ent_source.encode('utf-8')).hexdigest()
            # make qrcode for the key
            makeqr(half_key,'half1.png')
            # make printable pdf
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write('<h4>Private key, part 1/2</h4>')
            ft.write('<p><strong>Text: </strong>' + half_key + '</p>')
            ft.write('<p><img src="half1.png" width="200" height="200"></p>')
            ft.write('<p></p><p></p><p><em>Use blinddecode to obtain the full private key<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/halfkey1.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            subprocess.run(['xdg-open', 'PaperWallet/halfkey1.pdf'])


    def new_user_turn(self):
        if exists('PaperWallet/half1.png'):
            os.system('lsof -t PaperWallet/halfkey1.pdf | xargs kill')
            os.remove('PaperWallet/half1.png')
            os.remove('PaperWallet/halfkey1.pdf')
            self.master.withdraw()  
            second_window = tk.Toplevel(self.master)
            second_window.geometry("450x150")
            SecondWindow(second_window)
        else:
            show_popup('Before proceeding, type some text in the box, generate the 1/2 part of the private key and store it in a safe place')


class SecondWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Operator 2")
        self.master.geometry("450x150")

        self.input_label = tk.Label(master, text="Type some random text:")
        self.input_label.pack()

        self.input_text = tk.Entry(master)
        self.input_text.pack()

        # Opens a pdf with the part of the private key and QR codes
        self.button1 = tk.Button(master, text="Generate second half key", command=self.gen_second_half, bg="black", fg="blue")
        self.button1.pack()

        # Closes and deletes pdf file and qr code and opens a new window to generate receiving addresses
        self.button2 = tk.Button(master, text="End, obtain addresses", command=self.go_to_pub_gen, bg="black", fg="blue")
        self.button2.pack()


    def gen_second_half(self):
        global sec_half_key
        input_text = self.input_text.get()
        if input_text == '':
            show_popup('Please insert some text in the proper box before generating the 2/2 part of the private key')
        elif exists('PaperWallet/halfkey2.pdf'):
            show_popup('You already created the second part of th private key, click on the other button to go to the next step')
        else:
            # Add random system entropy
            extra_ent = str(system_random.randint(0, sys.maxsize))
            extra_ent += str(system_random.randint(0, sys.maxsize))
            # create entropy source joining random word to random system entropy
            ent_source = input_text + extra_ent
            # obtain first 128 bits of the private key
            sec_half_key = hashlib.md5(ent_source.encode('utf-8')).hexdigest()
            # make qrcode for the key
            makeqr(sec_half_key,'half2.png')
            # make printable pdf
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write('<h4>Private key, part 2/2</h4>')
            ft.write('<p><strong>Text: </strong>' + sec_half_key + '</p>')
            ft.write('<p><img src="half2.png" width="200" height="200"></p>')
            ft.write('<p></p><p></p><p><em>Use blinddecode to obtain the full private key<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/halfkey2.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            subprocess.run(['xdg-open', 'PaperWallet/halfkey2.pdf'])


    def go_to_pub_gen(self):
        if exists('PaperWallet/half2.png'):
            os.system('lsof -t PaperWallet/halfkey2.pdf | xargs kill')
            os.remove('PaperWallet/half2.png')
            os.remove('PaperWallet/halfkey2.pdf')
            self.master.withdraw()  
            third_window = tk.Toplevel(self.master)
            third_window.geometry("450x150")
            ThirdWindow(third_window)
        else:
            show_popup('Before proceeding, type some text in the box, generate the 2/2 part of the private key and store it in a safe place')


class ThirdWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Generating addresses")
        self.master.geometry("450x150")

        # Available coins list
        self.coin_sel = tk.StringVar()
        self.coin_sel.set("Bitcoin")  # Default
        self.menu = tk.OptionMenu(master, self.coin_sel, "Bitcoin", "Ethereum (EVM)", "Litecoin", "Bitcoin Cash", "Bitcoin SV", "Dash", "ZCash", "Dogecoin", "Bitcoin testnet", "Monero")
        self.menu.pack()

        # Generates pdf with public addresses and QR codes
        self.button2 = tk.Button(master, text="Generate public addresses", command=self.gen_public_paper, bg="black", fg="blue")
        self.button2.pack()

        # Closes the tool
        self.button3 = tk.Button(master, text="Close", command=self.close_all, bg="black", fg="blue")
        self.button3.pack()


    def gen_public_paper(self):
        global coin_sel
        coin_sel = self.coin_sel.get()
        if half_key == None or sec_half_key == None:
            show_popup('Something has gone wrong, consider restarting the process')
            exit()
        priv_key = half_key + sec_half_key
        if coin_sel == 'Bitcoin':
            coin = BTC
        elif coin_sel == 'Ethereum (EVM)':
            coin = ETH
        elif coin_sel == 'Litecoin':
            coin = LTC
        elif coin_sel == 'Bitcoin Cash':
            coin = BCH
        elif coin_sel == 'Bitcoin SV':
            coin = BSV
        elif coin_sel == 'Dash':
            coin = DASH
        elif coin_sel == 'ZCash':
            coin = ZCH
        elif coin_sel == 'Dogecoin':
            coin = DOGE
        elif coin_sel == 'Bitcoin testnet':
            coin = BTCTEST
        elif coin_sel == 'Monero':
            s = Seed(priv_key)
            svk = s.secret_view_key()
            makeqr(svk,'svk.png')
            psk = s.public_spend_key()
            pvk = s.public_view_key()
            addr1 = str(s.public_address())
            makeqr(addr1,'address.png')
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write('<h4>XMR Paper wallet</h4>')
            ft.write('<p><strong>Secret view key: </strong>' + svk + '</p>')
            ft.write('<p><img src="svk.png" width="200" height="200"></p>')
            ft.write('<p><strong>Public spend key: </strong>' + psk + '</p>')
            ft.write('<p><strong>Public view key: </strong>' + pvk + '</p>')
            ft.write('<p><strong>Primary address: </strong>' + addr1 + '</p>')
            ft.write('<p><img src="address.png" width="200" height="200"></p>')
            ft.write('<p></p><p></p><p><em>Make sure to have both parts of the private key before sending funds<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Public.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            os.remove('PaperWallet/svk.png')
            os.remove('PaperWallet/address.png')
            subprocess.run(['xdg-open', 'PaperWallet/Public.pdf'])
        if coin_sel == 'Bitcoin' or coin_sel == 'Litecoin':
            hdwallet: HDWallet = HDWallet(symbol=coin)
            # Obtain wallet from private key
            hdwallet.from_private_key(private_key=priv_key)
            WIF_priv = hdwallet.wif()
            addr1 = hdwallet.p2pkh_address()
            makeqr(addr1,'p2pkh.png')
            addr2 = hdwallet.p2wpkh_in_p2sh_address()
            makeqr(addr2,'p2wpkh-p2sh.png')
            addr3 = hdwallet.p2wpkh_address()
            makeqr(addr3,'p2wpkh.png')
            # Creating PDF
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write(f'<h4>{coin_sel} paper wallet</h4>')
            ft.write('<p><strong>p2pkh address: </strong>' + addr1 + '</p>')
            ft.write('<p><img src="p2pkh.png" width="200" height="200"></p>')
            ft.write('<p><strong>p2wpkh-p2sh address: </strong>' + addr2 + '</p>')
            ft.write('<p><img src="p2wpkh-p2sh.png" width="200" height="200"></p>')
            ft.write('<p><strong>p2wpkh address: </strong>' + addr3 + '</p>')
            ft.write('<p><img src="p2wpkh.png" width="200" height="200"></p>')
            ft.write('<p></p><p></p><p><em>Make sure to have both parts of the private key before sending funds<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Public.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            os.remove('PaperWallet/p2pkh.png')
            os.remove('PaperWallet/p2wpkh-p2sh.png')
            os.remove('PaperWallet/p2wpkh.png')
            subprocess.run(['xdg-open', 'PaperWallet/Public.pdf'])
        elif coin_sel == 'Ethereum (EVM)':
            hdwallet: HDWallet = HDWallet(symbol=coin)
            hdwallet.from_private_key(private_key=priv_key)
            ETH_priv = '0x' + str(priv_key)
  #          print(f'Wallet private key: {ETH_priv}')
            addr1 = hdwallet.p2pkh_address()
  #          print(coin_sel, ' Address: ', addr1)
            makeqr(addr1,'address.png')
            # Creating PDF
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write(f'<h4>{coin_sel} paper wallet</h4>')
            ft.write('<p><strong>Public address: </strong>' + addr1 + '</p>')
            ft.write('<p><img src="address.png" width="200" height="200"></p>')  # Check path
            ft.write('<p></p><p></p><p><em>Make sure to have both parts of the private key before sending funds<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Public.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            os.remove('PaperWallet/address.png')
            subprocess.run(['xdg-open', 'PaperWallet/Public.pdf'])
        elif coin_sel == 'Bitcoin Cash':
            hdwallet: HDWallet = HDWallet(symbol=coin)
            hdwallet.from_private_key(private_key=priv_key)
            WIF_priv = hdwallet.wif()
            key = Key(WIF_priv)
            addr1 = key.address
            makeqr(addr1,'address.png')
            # Creating PDF
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write(f'<h4>{coin_sel} paper wallet</h4>')
            ft.write('<p><strong>Public address: </strong>' + addr1 + '</p>')
            ft.write('<p><img src="address.png" width="200" height="200"></p>')  # Check path
            ft.write('<p></p><p></p><p><em>Make sure to have both parts of the private key before sending funds<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Public.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            os.remove('PaperWallet/address.png')
            subprocess.run(['xdg-open', 'PaperWallet/Public.pdf'])
        elif coin_sel != 'Monero':
            hdwallet: HDWallet = HDWallet(symbol=coin)
            # Obtain wallet from private key
            hdwallet.from_private_key(private_key=priv_key)
            WIF_priv = hdwallet.wif()
            addr1 = hdwallet.p2pkh_address()
            makeqr(addr1,'address.png')
            # Creating PDF
            ft = open('PaperWallet/temp.html', 'w')
            ft.write('<!doctype html>\n<body>')
            if exists('PaperWallet/logo.png'):
                ft.write('<p><img src="logo.png" width="100" height="100"></p>')
            ft.write(f'<h4>{coin_sel} paper wallet</h4>')
            ft.write('<p><strong>Public address: </strong>' + addr1 + '</p>')
            ft.write('<p><img src="address.png" width="200" height="200"></p>')  # Check path
            ft.write('<p></p><p></p><p><em>Make sure to have both parts of the private key before sending funds<br></em></p>')
            ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
            ft.write('</body>')
            ft.close()
            pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Public.pdf', options={"enable-local-file-access": ""})
            os.remove('PaperWallet/temp.html')
            os.remove('PaperWallet/address.png')
            subprocess.run(['xdg-open', 'PaperWallet/Public.pdf'])


    def close_all(self):
        self.master.destroy()
        sys.exit()


def main():
    root = tk.Tk()
    app = FirstWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
