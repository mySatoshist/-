import random
import time
import os
import json
from datetime import datetime

def mHash():
    """
    生成一个64字符长度的随机十六进制字符串，用作私钥
    """
    hex_chars = '0123456789abcdef'
    return ''.join(random.choice(hex_chars) for _ in range(64))

def save_result(chain, privkey, address):
    """将找到的靓号保存到本地文件"""
    try:
        os.makedirs("results", exist_ok=True)
        
        result_file = os.path.join("results", f"{chain}_wallet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(result_file, "w") as f:
            f.write(f"Chain: {chain}\n")
            f.write(f"Private Key: {privkey}\n")
            f.write(f"Address: {address}\n")
            f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return result_file
    except Exception:
        return None

def is_valid_pattern(address, prefix="", suffix="", case_sensitive=False):
    """检查地址是否符合指定的模式"""
    if not case_sensitive:
        address = address.lower()
        prefix = prefix.lower()
        suffix = suffix.lower()
    
    if prefix and not address.startswith(prefix):
        return False
    
    if suffix and not address.endswith(suffix):
        return False
    
    return True


