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

# Global variables
string1 = None
string2 = None
coin_sel = None


# Generate QR codes from strings
def makeqr(keystr, filename):
    img = qrcode.make(keystr)
    type(img)
    filename = 'PaperWallet/' + filename
    img.save(filename)


def show_popup(message):
    popup = tk.Tk()
    popup.title("WARNING!")
    label = tk.Label(popup, text=message)
    label.pack()
    ok_button = tk.Button(popup, text="Ok", command=popup.destroy)
    ok_button.pack()
    popup.mainloop()


class ThirdWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Decode private key")
        self.master.geometry("450x200")

        self.string1_label = tk.Label(master, text="Insert part 1/2 of the private key:")
        self.string1_label.pack()

        self.string1_entry = tk.Entry(master)
        self.string1_entry.pack()

        self.string2_label = tk.Label(master, text="Insert part 2/2 of the private key:")
        self.string2_label.pack()

        self.string2_entry = tk.Entry(master)
        self.string2_entry.pack()

        # Coin list
        self.coin_sel = tk.StringVar()
        self.coin_sel.set("Bitcoin")  # Default
        self.menu = tk.OptionMenu(master, self.coin_sel, "Bitcoin", "Ethereum (EVM)", "Litecoin", "Bitcoin Cash", "Bitcoin SV", "Dash", "ZCash", "Dogecoin", "Bitcoin testnet", "Monero")
        self.menu.pack()

        self.button = tk.Button(master, text="Show private key", command=self.show_priv_key, bg="black", fg="blue")
        self.button.pack()

    def show_priv_key(self):
        global string1, string2, coin_sel
        string1 = self.string1_entry.get()
        string2 = self.string2_entry.get()
        coin_sel = self.coin_sel.get()

        if string1 == '' or string2 == '':
            show_popup('Please insert the two parts of the private key. You may use QtQR to read QR codes.')
        else:
            priv_key = string1 + string2
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
                ssk = s.secret_spend_key()
                makeqr(ssk,'ssk.png')
                ft = open('PaperWallet/temp.html', 'w')
                ft.write('<!doctype html>\n<body>')
                if exists('PaperWallet/logo.png'):
                    ft.write('<p><img src="logo.png" width="100" height="100"></p>')
                ft.write('<h4>XMR Private key</h4>')
                ft.write('<p><strong>Secret view key: </strong>' + ssk + '</p>')
                ft.write('<p><img src="ssk.png" width="200" height="200"></p>')
                ft.write('<p></p><p></p><p><em>Import key in clients like MyMonero or Feather Wallet<br></em></p>')
                ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
                ft.write('</body>')
                ft.close()
                pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Private.pdf', options={"enable-local-file-access": ""})
                os.remove('PaperWallet/temp.html')
                os.remove('PaperWallet/ssk.png')
                subprocess.run(['xdg-open', 'PaperWallet/Private.pdf'])
            if coin_sel == 'Bitcoin' or coin_sel == 'Litecoin':
                hdwallet: HDWallet = HDWallet(symbol=coin)
                # Obtain wallet from private key
                hdwallet.from_private_key(private_key=priv_key)
                WIF_priv = hdwallet.wif()
                makeqr(WIF_priv,'wif.png')
                # Creating PDF
                ft = open('PaperWallet/temp.html', 'w')
                ft.write('<!doctype html>\n<body>')
                if exists('PaperWallet/logo.png'):
                    ft.write('<p><img src="logo.png" width="100" height="100"></p>')
                ft.write(f'<h4>{coin_sel} Private key</h4>')
                ft.write('<p><strong>Private key: </strong>' + WIF_priv + '</p>')
                ft.write('<p><img src="wif.png" width="200" height="200"></p>')
                ft.write('<p></p><p></p><p><em>Import private key in tools like Electrum<br></em></p>')
                ft.write('<p><em>Specify address format with:<br></em></p>')
                ft.write('<p><em>- p2pkh: for legacy addresses<br></em></p>')
                ft.write('<p><em>- p2wpkh-p2sh: for segwit addresses<br></em></p>')
                ft.write('<p><em>- p2wpkh: for native segwit addresses<br></em></p>')
                ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
                ft.write('</body>')
                ft.close()
                pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Private.pdf', options={"enable-local-file-access": ""})
                os.remove('PaperWallet/temp.html')
                os.remove('PaperWallet/wif.png')
                subprocess.run(['xdg-open', 'PaperWallet/Private.pdf'])
            elif coin_sel == 'Ethereum (EVM)':
                hdwallet: HDWallet = HDWallet(symbol=coin)
                hdwallet.from_private_key(private_key=priv_key)
                ETH_priv = '0x' + str(priv_key)
                makeqr(ETH_priv,'wif.png')
                # Creating PDF
                ft = open('PaperWallet/temp.html', 'w')
                ft.write('<!doctype html>\n<body>')
                if exists('PaperWallet/logo.png'):
                    ft.write('<p><img src="logo.png" width="100" height="100"></p>')
                ft.write(f'<h4>{coin_sel} Private Key</h4>')
                ft.write('<p><strong>Private key: </strong>' + ETH_priv + '</p>')
                ft.write('<p><img src="wif.png" width="200" height="200"></p>')
                ft.write('<p></p><p></p><p><em>Use the key in tools like MyCrypto or MEW<br></em></p>')
                ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
                ft.write('</body>')
                ft.close()
                pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Private.pdf', options={"enable-local-file-access": ""})
                os.remove('PaperWallet/temp.html')
                os.remove('PaperWallet/wif.png')
                subprocess.run(['xdg-open', 'PaperWallet/Private.pdf'])
            elif coin_sel != 'Monero':
                hdwallet: HDWallet = HDWallet(symbol=coin)
                # Obtain wallet from private key
                hdwallet.from_private_key(private_key=priv_key)
                WIF_priv = hdwallet.wif()
                makeqr(WIF_priv,'wif.png')
                # Creating PDF
                ft = open('PaperWallet/temp.html', 'w')
                ft.write('<!doctype html>\n<body>')
                if exists('PaperWallet/logo.png'):
                    ft.write('<p><img src="logo.png" width="100" height="100"></p>')
                ft.write(f'<h4>{coin_sel} paper wallet</h4>')
                ft.write('<p><strong>Private key: </strong>' + WIF_priv + '</p>')
                ft.write('<p><img src="wif.png" width="200" height="200"></p>')
                ft.write('<p></p><p></p><p><em>Use the keys with tools related to the desired coin<br></em></p>')
                ft.write('<p></p><p></p><p><em>Made with blindgen.py<br>More info at https://anubitux.org</em></p>')
                ft.write('</body>')
                ft.close()
                pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/Private.pdf', options={"enable-local-file-access": ""})
                os.remove('PaperWallet/temp.html')
                os.remove('PaperWallet/wif.png')
                subprocess.run(['xdg-open', 'PaperWallet/Private.pdf'])


def main():
    root = tk.Tk()
    app = ThirdWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
