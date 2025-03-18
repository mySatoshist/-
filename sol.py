import os
import sys
import random
import time
import binascii
from solana.keypair import Keypair
from base58 import b58encode
from hexer import is_valid_pattern

class SOL:
    def __init__(self, prefix="", suffix="", case_sensitive=False, on_found_callback=None):
        """
        Initialize SOL class
        """
        self.prefix = prefix
        self.suffix = suffix
        self.case_sensitive = case_sensitive
        self.on_found_callback = on_found_callback
        
    def generate_wallet(self):
        """
        Generate a random SOL wallet
        """
        try:
            # Generate Solana keypair
            keypair = Keypair()
            
            # Get public key (address) and private key
            address = str(keypair.public_key)
            private_key = keypair.secret_key.hex()
            
            if self.is_vanity_address(address):
                if self.on_found_callback:
                    self.on_found_callback(address, private_key)
                return (address, private_key)
                
            return None
            
        except Exception as e:
            print(f"SOL wallet error: {str(e)}")
            return None
        
    def is_vanity_address(self, address):
        """
        Check if address matches vanity criteria
        """
        # Check prefix
        if self.prefix:
            check_prefix = address[:len(self.prefix)]
            if self.case_sensitive:
                if check_prefix != self.prefix:
                    return False
            else:
                if check_prefix.lower() != self.prefix.lower():
                    return False
                
        # Check suffix
        if self.suffix:
            check_suffix = address[-len(self.suffix):]
            if self.case_sensitive:
                if check_suffix != self.suffix:
                    return False
            else:
                if check_suffix.lower() != self.suffix.lower():
                    return False
                
        return True

if __name__ == "__main__":
    sol = SOL(prefix="sol", suffix="8888")
    
    print("Starting SOL address generation...")
    start_time = time.time()
    count = 0
    
    try:
        while True:
            result = sol.generate_wallet()
            count += 1
            
            if result:
                address, private_key = result
                print(f"\nFound matching address:")
                print(f"Address: {address}")
                print(f"Private key: {private_key}")
                
            if count % 100 == 0:
                elapsed = time.time() - start_time
                print(f"\rTried: {count}, Speed: {count/elapsed:.2f}/s", end="")
                
    except KeyboardInterrupt:
        print("\n\nStopped")
        elapsed = time.time() - start_time
        print(f"Total: {count}, Average speed: {count/elapsed:.2f}/s")
