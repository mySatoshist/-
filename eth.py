import os
import random
import binascii
import time
from eth_account import Account
from hexer import is_valid_pattern

class ETH:
    def __init__(self, prefix="", suffix="", case_sensitive=False, on_found_callback=None):
        """
        Initialize ETH class
        """
        self.prefix = prefix
        self.suffix = suffix
        self.case_sensitive = case_sensitive
        self.on_found_callback = on_found_callback
        
    def generate_wallet(self):
        """
        Generate a random ETH wallet
        """
        try:
            # 启用本地账户功能
            Account.enable_unaudited_hdwallet_features()
            
            # 生成随机私钥
            private_key = '0x' + ''.join(random.choice('0123456789abcdef') for _ in range(64))
            
            # 从私钥生成账户
            account = Account.from_key(private_key)
            
            # 提取地址，去掉前缀"0x"
            address = account.address[2:]
            
            if self.is_vanity_address(address):
                # 如果符合靓号条件，回调处理
                private_key_raw = private_key[2:]  # 移除0x前缀
                
                if self.on_found_callback:
                    self.on_found_callback(address, private_key_raw)
                    
                return (address, private_key_raw)
                
            return None
            
        except Exception as e:
            print(f"ETH wallet generation error: {str(e)}")
            return None
        
    def is_vanity_address(self, address):
        """
        Check if address matches vanity criteria
        """
        # 检查前缀
        if self.prefix:
            check_prefix = address[:len(self.prefix)]
            if self.case_sensitive:
                if check_prefix != self.prefix:
                    return False
            else:
                if check_prefix.lower() != self.prefix.lower():
                    return False
                
        # 检查后缀
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
    # 测试代码
    eth = ETH(prefix="88", suffix="88")
    
    print("Starting ETH address generation...")
    start_time = time.time()
    count = 0
    
    try:
        while True:
            result = eth.generate_wallet()
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