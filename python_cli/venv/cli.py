import struct
import hashlib
import json
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction, TransactionInstruction
from solana.rpc.api import Client

print("CLI Tool Shit on Chain by Baveja!")

# 1. Inputs
try:
    a = int(input("[+] Enter a number : "))
    b = int(input("[+] Enter a number : "))
except ValueError:
    print("Invalid input")
    exit(1)

# 2. Setup Wallet
wallet_data = [42,118,150,143,68,43,141,204,184,94,77,74,130,138,0,82,220,208,65,209,17,253,47,100,255,58,6,42,42,59,200,127,87,228,15,46,200,238,177,44,116,232,115,125,199,223,128,12,203,227,48,206,199,75,125,213,134,167,210,181,11,72,210,149]
payer = Keypair.from_secret_key(bytes(wallet_data))
print(f"Payer Public Key: {payer.public_key}")

# 3. Setup Client
http_client = Client("https://api.devnet.solana.com")
if not http_client.is_connected():
    print("Failed to connect to devnet")
    exit(1)

# 4. Construct Instruction
# Discriminator for "global:add"

# user defined discriminator


print("""
    1. Addition
    2. subtraction
    3. Multiply
    4. Division
""")
c = int(input("[+] Enter your choice : "))
if(c==1):
    d = hashlib.sha256("global:add".encode()).digest()[:8]
    data = d + struct.pack("<qq", a, b)
elif(c==2):
    d = hashlib.sha256("global:sub".encode()).digest()[:8]
    data = d + struct.pack("<qq", a, b)
elif (c==3):
    d = hashlib.sha256("global:mul".encode()).digest()[:8]
    data = d + struct.pack("<qq", a, b)

else:
    d = hashlib.sha256("global:div".encode()).digest()[:8]
    data = d + struct.pack("<qq", a, b)

# d = hashlib.sha256("global:add".encode()).digest()[:8]
# dsub = hashlib.sha256("global:sub".encode()).digest()[:8]

# dataadd = d + struct.pack("<qq", a, b)
# datasub = dsub + struct.pack("<qq",a,b)

program_id = PublicKey("8MsFsFz1cPshextfGhHCgXStV7YudFCPZWje3dU4n24t")

ix = TransactionInstruction(
    keys=[],
    program_id=program_id,
    data=data
)

# 5. Build and Sign Transaction
# Explicitly set recent_blockhash to avoid logic errors in auto-fetch
blockhash = http_client.get_latest_blockhash().value.blockhash
txn = Transaction(recent_blockhash=str(blockhash), fee_payer=payer.public_key)
txn.add(ix)

import time

DEBUG = False 

print("--- Solana Calculator ---\n") # Cleaner header

try:
    res = http_client.send_transaction(txn, payer)
    tx_sig = res.value
    print(f"Transaction Sent: https://explorer.solana.com/tx/{tx_sig}?cluster=devnet\n")
    print("Waiting for result...\n")

    # Poll for confirmation
    confirmed = False
    for i in range(10): # Try for 20 seconds
        try:
            time.sleep(2)
            tx_resp = http_client.get_transaction(tx_sig, max_supported_transaction_version=0)
            
            if tx_resp.value:
                meta = tx_resp.value.transaction.meta
                if meta and meta.log_messages:
                    logs = meta.log_messages
                    
                    if DEBUG:
                        print("\n--- Full Logs ---")
                        for log in logs:
                            print(log)
                        print("-----------------")

                    # Look for our specific program log
                    found = False
                    for log in logs:
                        if "Result" in log:
                            # Handle both "Result:" and "Result :"
                            clean_msg = log.split("Result")[-1].lstrip(": ")
                            print(f"\nResult: {clean_msg}")
                            # print(f"\nResult: {type(clean_msg)}")
                            found = True
                            
                    if not found and not DEBUG:
                        print("Transaction confirmed.")
                        
                    confirmed = True
                    break
        except Exception:
            pass
            
    if not confirmed:
        print("Transaction taking longer than expected...")
        
except Exception as e:
    print(f"Error: {e}")