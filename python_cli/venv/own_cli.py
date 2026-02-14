import struct
import hashlib
import time
import json
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction, TransactionInstruction
from solana.rpc.api import Client

# Predefined things

program_id = PublicKey("8MsFsFz1cPshextfGhHCgXStV7YudFCPZWje3dU4n24t")
print("CLI Tool shit by Baveja!")

a = int(input("[+] Enter Your number : "))
b = int(input("[+] Enter your number : "))

# print(a+b)  fairly simple calculator in python

# setup the wallet shit part

wallet = [42,118,150,143,68,43,141,204,184,94,77,74,130,138,0,82,220,208,65,209,17,253,47,100,255,58,6,42,42,59,200,127,87,228,15,46,200,238,177,44,116,232,115,125,199,223,128,12,203,227,48,206,199,75,125,213,134,167,210,181,11,72,210,149]
payer = Keypair.from_secret_key(bytes(wallet))

print(f"Payer public key : " , payer.public_key)

# Setup client

http_client = Client("https://api.devnet.solana.com")
if not http_client.is_connected():
    print("Failed to connect to the devnet")
    exit(1)



# construct Instruction 



d = hashlib.sha256("global:add".encode()).digest()[:8]
data = d + struct.pack("<qq", a, b)

ix = TransactionInstruction(
    keys=[],
    program_id=program_id,
    data = data
)

# build and submit txn
blockhash = http_client.get_latest_blockhash().value.blockhash

txn = Transaction(recent_blockhash=str(blockhash),fee_payer=payer.public_key)

txn.add(ix)

print("Sending Solana txn")

try:
    res = http_client.send_transaction(txn ,payer)
    tx_sig = res.value
    print("Transaction is sent to the devnet network to solana")
    for i in range(10): # Try to get info every 10 sec
        time.sleep(2)
        tx_res = http_client.get_transaction(tx_sig , max_supported_transaction_version=0)

        if tx_res.value:
            meta = tx_res.value.transaction.meta
            if meta and meta.log_messages:
                logs = meta.log_messages

                for log in logs:
                    if "Result" in log:
                        clean_msg = log.split("Result")[-1].lstrip(": ")
                        print(f"Result : {clean_msg}")
            break
except Exception as e:
    print(e)

