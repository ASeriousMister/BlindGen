# BlindGen
This tool allows two operators to create a crypto wallet to receive funds so that nobody has access to the entire private key.

## How to use
### Creating private key and receiving addresses
Install python virtual environments
```
sudo apt install python3-virtualenv
```
Clone this tool and move to its folder
```
git clone github.com/ASeriousMister/BlindGen
cd /path/SecureGen
```
Create a virtual environment
```
virtualenv sgve
```
Activate it
```
source sgve/bin/activate
```
Install dependencies
```
pip3 install -r requirements.txt
```
install wkhtmltopdf to generate printable PDFs
```
sudo apt install wkhtmltopdf
```
Install evince as default pdf reader
```
sudo apt install evince
```
Launch the tool
```
pytohn3 blindgen.py
```
Take note of the private keys and store them in a safe place
### Spending funds
Launch the proper tool
```
python3 blinddecode.py
```
Insert private key parts in the proper boxes.\
To read QR codes, QtQR may be useful
```
sudo apt install qtqr
```
## Disclaimer
This tool has been designed to generate cruypto wallets allowing nobody to have access to the whole private key. It works only if used properly. End users are responsible for their actions and for any misuse.\
End users are also responsible for storing the private keys in a safe way. The tool does not store any tipe of information related to the private keys and in no way it will be able to recover access to lost information.\
This tool is provided 'as is' without any warranty of any kind, express or implied. The developers make no warranty that the tool will be free from errors, defects or inaccuracies.\
In no event shall the developers be liable for any damages or losses incurred as a result of using this tool.
