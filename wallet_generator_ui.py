import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
import sys

# 尝试导入SOL类
try:
    from sol import SOL
except ImportError:
    class SOL:
        def __init__(self, prefix="", suffix="", case_sensitive=False, on_found_callback=None):
            self.prefix = prefix
            self.suffix = suffix
            self.case_sensitive = case_sensitive
            self.on_found_callback = on_found_callback
            
        def generate_wallet(self):
            return None

# 尝试导入ETH和TRX的模块
try:
    from eth import ETH
except ImportError:
    # 创建一个简单的ETH类替代
    class ETH:
        def __init__(self, prefix="", suffix="", case_sensitive=False, on_found_callback=None):
            self.prefix = prefix
            self.suffix = suffix
            self.case_sensitive = case_sensitive
            self.on_found_callback = on_found_callback
            
        def generate_wallet(self):
            # 此处应添加真实的ETH钱包生成逻辑
            # 这只是一个占位符实现
            return None

try:
    from trx import TRX
except ImportError:
    # 创建一个简单的TRX类替代
    class TRX:
        def __init__(self, prefix="", suffix="", case_sensitive=False, on_found_callback=None):
            self.prefix = prefix
            self.suffix = suffix
            self.case_sensitive = case_sensitive
            self.on_found_callback = on_found_callback
            
        def generate_wallet(self):
            # 此处应添加真实的TRX钱包生成逻辑
            # 这只是一个占位符实现
            return None

class WalletGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("区块链靓号生成器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置应用风格
        style = ttk.Style()
        try:
            style.theme_use('clam')  # 使用clam主题
        except:
            pass  # 如果主题不可用，使用默认主题
        
        # 定义颜色
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6fa5"
        self.button_color = "#4a90e2"
        
        # 设置根窗口背景色
        self.root.configure(bg=self.bg_color)
        
        # 创建生成器状态变量
        self.running = False
        self.wallet_generators = {}
        self.count = 0
        self.start_time = 0
        
        # 加载配置
        self.load_config()
        
        # 创建UI元素
        self.create_ui()
    
    def load_config(self):
        """加载配置文件"""
        self.config = {
            "save_local": True,
            "chains": {
                "ETH": {
                    "enabled": True,
                    "prefix": "",
                    "suffix": ""
                },
                "TRX": {
                    "enabled": True,
                    "prefix": "",
                    "suffix": ""
                },
                "SOL": {
                    "enabled": True,
                    "prefix": "",
                    "suffix": ""
                }
            }
        }
        
        try:
            if os.path.exists("wallet_config.json"):
                with open("wallet_config.json", "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # 更新配置
                    self.config.update(loaded_config)
        except Exception as e:
            messagebox.showerror("配置加载错误", f"配置文件加载失败: {str(e)}")
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open("wallet_config.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("配置保存错误", f"配置保存失败: {str(e)}")
    
    def create_ui(self):
        """创建用户界面"""
        # 创建标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建生成器标签页和结果标签页
        self.generator_frame = ttk.Frame(self.notebook)
        self.results_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.generator_frame, text="靓号生成器")
        self.notebook.add(self.results_frame, text="结果")
        
        # 设置生成器页面
        self.setup_generator_page()
        
        # 设置结果页面
        self.setup_results_page()
    
    def setup_generator_page(self):
        """设置生成器页面"""
        # 创建主框架
        main_frame = ttk.Frame(self.generator_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 链选择部分
        chain_frame = ttk.LabelFrame(main_frame, text="选择链")
        chain_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建链选择变量和复选框
        self.chain_vars = {}
        for chain in ["ETH", "TRX", "SOL"]:
            self.chain_vars[chain] = tk.BooleanVar(value=False)  # 默认都不选
            cb = ttk.Checkbutton(chain_frame, text=chain, variable=self.chain_vars[chain])
            cb.pack(side=tk.LEFT, padx=20, pady=5)
        
        # 前缀后缀设置部分
        pattern_frame = ttk.LabelFrame(main_frame, text="靓号设置")
        pattern_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # 创建前缀后缀输入
        prefix_frame = ttk.Frame(pattern_frame)
        prefix_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(prefix_frame, text="前缀:").pack(side=tk.LEFT, padx=5, pady=5)
        self.prefix_entry = ttk.Entry(prefix_frame)
        self.prefix_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        suffix_frame = ttk.Frame(pattern_frame)
        suffix_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(suffix_frame, text="后缀:").pack(side=tk.LEFT, padx=5, pady=5)
        self.suffix_entry = ttk.Entry(suffix_frame)
        self.suffix_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # 区分大小写选项
        self.case_sensitive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(pattern_frame, text="区分大小写", variable=self.case_sensitive_var).pack(anchor=tk.W, padx=5, pady=5)
        
        # 控制区域
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.start_button = ttk.Button(control_frame, text="开始生成", command=self.start_generation)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = ttk.Button(control_frame, text="停止", command=self.stop_generation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 状态区域
        status_frame = ttk.LabelFrame(main_frame, text="状态")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # 进度信息 - 使用自动滚动的文本框
        self.status_text = scrolledtext.ScrolledText(status_frame, height=10)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.status_text.config(state=tk.DISABLED)
        
        # 添加一个清除状态的按钮
        clear_status_btn = ttk.Button(status_frame, text="清除状态", 
                                     command=lambda: self.update_status("已清除状态信息", append=False))
        clear_status_btn.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # 状态栏
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_results_page(self):
        """设置结果页面"""
        # 创建主框架
        main_frame = ttk.Frame(self.results_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 结果显示
        self.results_text = scrolledtext.ScrolledText(main_frame)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_text.config(state=tk.DISABLED)
        
        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        clear_button = ttk.Button(button_frame, text="清除结果", command=self.clear_results)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        export_button = ttk.Button(button_frame, text="导出结果", command=self.export_results)
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def update_status(self, text, append=True):
        """更新状态文本，并确保显示最新内容"""
        self.status_text.config(state=tk.NORMAL)
        if append:
            self.status_text.insert(tk.END, text + "\n")
            self.status_text.see(tk.END)  # 确保滚动到最新内容
        else:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, text + "\n")
        self.status_text.config(state=tk.DISABLED)
        
        # 强制更新UI
        self.root.update_idletasks()
    
    def update_results(self, text):
        """更新结果文本"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def clear_results(self):
        """清除结果"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def export_results(self):
        """导出结果"""
        try:
            filename = f"wallet_results_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.results_text.get(1.0, tk.END))
            messagebox.showinfo("导出成功", f"结果已导出到 {filename}")
        except Exception as e:
            messagebox.showerror("导出错误", f"导出失败: {str(e)}")
    
    def on_found_wallet(self, chain, address, private_key):
        """找到靓号时的回调函数"""
        result_text = f"找到 {chain} 靓号:\n地址: {address}\n私钥: {private_key}\n时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        self.update_results(result_text)
        self.update_status(f"找到 {chain} 靓号: {address}")
        
        # 保存到文件（始终保存）
        try:
            from hexer import save_result
            result_file = save_result(chain, private_key, address)
            if result_file:
                self.update_status(f"已保存到本地: {result_file}")
            else:
                self.update_status(f"保存失败")
        except Exception as e:
            self.update_status(f"保存失败: {str(e)}")
    
    def start_generation(self):
        """开始生成靓号"""
        # 检查是否选择了至少一个链
        selected_chains = [chain for chain in ["ETH", "TRX", "SOL"] if self.chain_vars[chain].get()]
        if not selected_chains:
            messagebox.showerror("错误", "请至少选择一个链")
            return
        
        # 更新配置
        for chain in ["ETH", "TRX", "SOL"]:
            self.config["chains"][chain]["enabled"] = self.chain_vars[chain].get()
        
        # 始终保存到本地
        self.config["save_local"] = True
        
        # 保存配置
        self.save_config()
        
        # 禁用开始按钮，启用停止按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 设置生成状态
        self.running = True
        self.count = 0
        self.start_time = time.time()
        
        # 清除状态
        self.update_status("开始生成靓号...", append=False)
        
        # 创建并启动生成线程
        self.gen_thread = threading.Thread(target=self.generation_loop, args=(selected_chains,))
        self.gen_thread.daemon = True
        self.gen_thread.start()
        
        # 启动更新线程
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def stop_generation(self):
        """停止生成靓号"""
        self.running = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.update_status("已停止生成")
    
    def generation_loop(self, selected_chains):
        """靓号生成循环"""
        # 创建钱包生成器
        self.wallet_generators = {}
        for chain in selected_chains:
            prefix = self.prefix_entry.get()
            suffix = self.suffix_entry.get()
            case_sensitive = self.case_sensitive_var.get()
            
            # 创建回调函数
            callback = lambda address, private_key, ch=chain: self.on_found_wallet(ch, address, private_key)
            
            if chain == "ETH":
                generator = ETH(prefix=prefix, suffix=suffix, case_sensitive=case_sensitive,
                               on_found_callback=callback)
            elif chain == "TRX":
                generator = TRX(prefix=prefix, suffix=suffix, case_sensitive=case_sensitive,
                               on_found_callback=callback)
            elif chain == "SOL":
                generator = SOL(prefix=prefix, suffix=suffix, case_sensitive=case_sensitive,
                               on_found_callback=callback)
            
            self.wallet_generators[chain] = generator
        
        # 生成循环
        try:
            while self.running:
                for chain in selected_chains:
                    if not self.running:
                        break
                    
                    generator = self.wallet_generators[chain]
                    result = generator.generate_wallet()
                    self.count += 1
                    
                    # 如果找到靓号，回调函数已经处理了
        
        except Exception as e:
            self.update_status(f"生成错误: {str(e)}")
            self.running = False
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
    
    def update_loop(self):
        """更新状态循环"""
        last_count = 0
        update_interval = 100  # 每生成100个地址更新一次状态
        
        while self.running:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                speed = self.count / elapsed
                status_text = f"已尝试: {self.count}, 速度: {speed:.2f}/秒"
                
                # 使用after方法安全地更新UI
                self.root.after(0, lambda: self.status_bar.config(text=status_text))
                
                # 定期在状态区域更新处理进度
                if self.count - last_count >= update_interval:
                    progress_text = f"处理中... 已尝试 {self.count} 个地址, 当前速度: {speed:.2f}/秒"
                    self.root.after(0, lambda txt=progress_text: self.update_status(txt))
                    last_count = self.count
            
            time.sleep(0.5)  # 更频繁地更新状态

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletGeneratorUI(root)
    root.mainloop() 