def calculate_interpolation():
    print("--- 热电偶温度线性插值计算器 ---")
    try:
        # 获取用户输入
        u = float(input("请输入待求电势 u (mV): "))
        t1 = float(input("请输入上限温度 t1 (℃): "))
        t2 = float(input("请输入下限温度 t2 (℃): "))
        u1 = float(input("请输入 t1 对应的电势 u1 (mV): "))
        u2 = float(input("请输入 t2 对应的电势 u2 (mV): "))

        # 检查分母是否为零
        if u1 == u2:
            print("错误: u1 和 u2 不能相等（分母不能为零）。")
            return
        

        # 根据公式计算 x
        x = t2 + (u - u2) * (t1 - t2) / (u1 - u2)

        # 输出结果，保留三位小数
        print("-" * 30)
        if t1 <= t2:
            print("警告: 输入的上限温度小于等于下限温度。")
        print(f"计算得到的温度 x = {x:.3f} ℃")
        
    except ValueError:
        print("输入错误: 请输入有效的数字。")

if __name__ == "__main__":
    while True:
        calculate_interpolation()

