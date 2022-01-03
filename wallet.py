import base64
import hashlib
import random
from Cryptodome import Random
from Cryptodome.Cipher import AES
import sys, os, subprocess
import time, requests
global balance
global key
key = "123"
def run():
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
    print("Welcome to No Server Currency (NSC) Wallet.")
    print("This version is currently on beta. So, there can be some problem.\n")
    with open("wallet.data", 'r+') as f:
        if f.readline().strip() == "":
            balance = 1
            dat = f"{balance}|{current_machine_id}"
            dat_hashed = AESCipher(key).encrypt(dat)
            f.write(dat_hashed)
            print("There is no wallet data, so we created wallet data.")
            print("Your wallet is located on wallet.data file.")
            print("In wallet.data file, there is your wallet data. So, do not delete this.\n")

    with open("wallet.data", 'r') as sd:
        if current_machine_id != AESCipher(key).decrypt(sd.readline().strip()).split("|")[1]:
            print("You can't use this wallet data because hwid is not same.\nIf you want to move wallet data, create another wallet and create transaction.\nOr, if you want to make new wallet, open wallet.data file with notepad, and delete all\n")
            print("Exiting in 3 seconds...")
            time.sleep(3)
            exit()
            

    with open("wallet.data", 'r') as r:
        print("Your wallet data")
        data = AESCipher(key).decrypt(r.readline().strip())
        data_balance = data.split("|")
        print(f"Current Balance: {data_balance[0]} NSC\n")
    def choice():
        print("Choose your option below:")
        print("1 - Make transaction")
        print("2 - Read transaction")
        print("3 - Move wallet data")
        m = input('Choice: ')
        if m == "1":
            def NSC():
                print("\nWhat amount of NSC do you wants to send?")
                am = input('Amount: ')
                am = int(am)
                with open("wallet.data", 'r') as df:
                    if am <= int(AESCipher(key).decrypt(df.readline().strip()).split("|")[0]):
                        if am == 0:
                            print("\nYou can't send 0 NSC.")
                            NSC()
                        else:
                            text = f"{random.random()}+{random.random()}+{random.random()}+{random.random()}+{random.random()}=="
                            md5 = hashlib.md5(text.encode('utf-8')).hexdigest()
                            transaction = AESCipher(key).encrypt(f"{am}+{md5}==")
                            print(f"\nTransaction has been created.\nCopy {transaction} and give to Trader\n")
                            choice()
                    else:
                        print("\nAmount is bigger than your balance.")
                        NSC()
            with open("wallet.data", 'r') as df2:
                if int(AESCipher(key).decrypt(df2.readline().strip()).split("|")[0]) == 0:
                    print("\nYou can't make transaction because, your balance is 0 NSC\n")
                    choice()
                else:
                    NSC()
        elif m == "2":
            print("\nPaste transaction that you got")
            tr = input('transaction: ')
            with open("wallet.data", 'r') as r2:
                bal = AESCipher(key).decrypt(r2.readline().strip()).split("|")[0]
                with open("wallet.data", 'w+') as wd:
                    aes = int(AESCipher(key).decrypt(tr).split("+")[0]) + int(bal)
                    dat = f"{aes}|{current_machine_id}"
                    dat_hashed = AESCipher(key).encrypt(dat)
                    requests.post("http://localhost:5000/not_used/add", data = {"data":dat_hashed})
                    wd.write(dat_hashed)
                    print("\nNow your balance is " + aes + " NSC")
                    choice()
        elif m == "3":
            print("\nHow to move wallet data.")
            print("1. Create new wallet on new workspace.")
            print("2. Make a transaction on wallet.")
            print("3. Read transaction on new wallet.\n")
            choice()
        else:
            print()
            choice()
    choice()

class AESCipher:

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type((b'').decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def main():
   # text = f"{random.random()}-{random.random()}-{random.random()}-{random.random()}"
   # md5 = str(hashlib.md5(text.encode('utf-8')).hexdigest())
    #sha512 = hashlib.sha512(md5.encode('utf-8')).hexdigest()
    # 지갑에 대한 정보
   # print(AESCipher(data).encrypt(key))
    #return AESCipher(data).encrypt(key)
    if len(sys.argv) < 3:
        print(f'[!] 사용방법: "{sys.argv[0]}" <encrypt | decrypt> <text> <code>')

    else:
        if str(sys.argv[1]) == "encrypt":
            print(sys.argv[2])
            print(AESCipher(sys.argv[3]).encrypt(sys.argv[2]))
            return
        elif str(sys.argv[1]) == "decrypt":
            print(AESCipher(sys.argv[3]).decrypt(sys.argv[2]))
            return
        else:
            print("Not Mode.")
            return

if __name__ == "__main__":
    run()