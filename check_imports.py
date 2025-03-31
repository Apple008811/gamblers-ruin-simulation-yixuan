import importlib
import subprocess
import sys

def check_and_install_module(module_name, package_name=None):
    """检查模块是否已安装，如果没有则尝试安装"""
    if package_name is None:
        package_name = module_name
        
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} 已安装")
        return True
    except ImportError:
        print(f"✗ 未找到 {module_name} 模块")
        
        choice = input(f"是否要安装 {package_name}? (y/n): ")
        if choice.lower() != 'y':
            return False
            
        print(f"正在安装 {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} 安装成功!")
            return True
        except Exception as e:
            print(f"✗ 安装失败: {str(e)}")
            return False

def check_required_modules():
    """检查所有需要的模块"""
    required_modules = [
        ("tkinter", "tkinter"),
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("ttkthemes", "ttkthemes"),
        ("requests", "requests"),
        ("json", None),  # 内置模块
        ("threading", None),  # 内置模块
        ("time", None),  # 内置模块
        ("datetime", None),  # 内置模块
        ("flask", "flask"),
        ("plotly", "plotly"),
    ]
    
    all_installed = True
    missing_modules = []
    
    for module_name, package_name in required_modules:
        if package_name is None:
            try:
                importlib.import_module(module_name)
                print(f"✓ {module_name} 已安装 (内置模块)")
            except ImportError:
                print(f"✗ 未找到内置模块 {module_name}")
                all_installed = False
                missing_modules.append(module_name)
        else:
            if not check_and_install_module(module_name, package_name):
                all_installed = False
                missing_modules.append(module_name)
    
    if all_installed:
        print("\n✓ 所有必需的模块已安装。可以运行主程序。")
        return True
    else:
        print(f"\n✗ 以下模块缺失: {', '.join(missing_modules)}")
        print("请安装缺失的模块后再运行程序。")
        return False

if __name__ == "__main__":
    print("检查数据可视化应用所需的Python模块...\n")
    if check_required_modules():
        print("\n您可以现在运行 advanced_gui_app.py") 