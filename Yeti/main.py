import sys

def print_welcome_and_constants():
    """输出黑板上的已知固定数据，便于用户确认"""
    print("=" * 60)
    print("        落球法液体黏度测定 - 数据处理控制台程序        ")
    print("=" * 60)
    print("【系统确认】正在载入黑板已知固定数据（已自动换算为国际标准单位）：")
    print("  • 钢球密度 (rho_钢) : 7.89 g/cm³  -> 7890.0 kg/m³")
    print("  • 液体密度 (rho_油) : 0.957 g/cm³ -> 957.0 kg/m³")
    print("  • 重力加速度 (g)    : 9.7988 m/s²")
    print("  • 量筒内径 (D)      : 22.00 mm    -> 0.022 m")
    print("  • 落球距离 (s)      : 0.1 m       (量筒标记位 7~17cm)")
    print("  • 仪器修正系数 (k)  : 2.4")
    print("=" * 60)

def get_float_input(prompt):
    """安全获取浮点数输入的函数"""
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input.lower() == 'q':
                print("\n程序已由用户退出。再见！")
                sys.exit()
            return float(user_input)
        except ValueError:
            print("❌ 输入错误！请输入有效的数字（或输入 'q' 退出）。")

def main():
    # 定义黑板固定常数
    RHO_STEEL = 7890.0  # kg/m^3
    RHO_OIL = 957.0     # kg/m^3
    G = 9.7988          # m/s^2
    D_CYLINDER = 0.022  # m (22.00 mm)
    S_DISTANCE = 0.1    # m
    K_COEFF = 2.4

    print_welcome_and_constants()

    # 1. 输入初始读数 d_0
    print("💡 提示：在接下来的任意输入步骤中，输入 'q' 均可直接退出程序。")
    d0 = get_float_input("👉 请输入螺旋测微器初读数 d_0 (mm): ")
    print(f"✅ 成功设定初读数 d_0 = {d0} mm\n")

    group_count = 1
    
    # 2. 循环处理每组数据
    while True:
        print("-" * 60)
        print(f" 当前正在录入：【第 {group_count} 组数据】")
        print("-" * 60)
        
        # 录入3次测量值
        d1 = get_float_input(f"  请输入第 {group_count} 组 - 测量值 1 (mm): ")
        d2 = get_float_input(f"  请输入第 {group_count} 组 - 测量值 2 (mm): ")
        d3 = get_float_input(f"  请输入第 {group_count} 组 - 测量值 3 (mm): ")
        
        # 录入温度和时间
        temp = get_float_input(f"  请输入第 {group_count} 组 - 当前温度 T (℃): ")
        t_time = get_float_input(f"  请输入第 {group_count} 组 - 下落时间 t (s): ")
        
        print("\n" + "." * 20 + " 正在开始数据处理 " + "." * 20)
        
        # 计算测量平均值和实际直径
        d_avg_measured = (d1 + d2 + d3) / 3.0
        d_actual_mm = d_avg_measured - d0
        d_actual_m = d_actual_mm / 1000.0  # 换算为米用于黏度计算
        
        # 输出直径计算算式与结果
        print("\n【1. 钢球实际直径计算】")
        print(f"  • 算式：d_i = ((d' + d'' + d''') / 3) - d_0")
        print(f"  • 带入：d_i = (({d1} + {d2} + {d3}) / 3) - ({d0})")
        print(f"  • 结果：测量平均值 = {d_avg_measured:.4f} mm")
        print(f"          修正后实际直径 d_i = {d_actual_mm:.4f} mm (即 {d_actual_m:.7f} m)")
        
        # 计算黏度
        # 分子 = (rho_钢 - rho_油) * g * d^2 * t
        numerator = (RHO_STEEL - RHO_OIL) * G * (d_actual_m ** 2) * t_time
        # 分母 = 18 * s * (1 + k * (d / D))
        denominator = 18 * S_DISTANCE * (1 + K_COEFF * (d_actual_m / D_CYLINDER))
        eta = numerator / denominator
        
        # 输出黏度计算算式与结果
        print("\n【2. 液体动力黏度计算】")
        print("  • 算式：eta = [ (rho_钢 - rho_油) * g * d_i² * t ] / [ 18 * s * (1 + k * (d_i / D)) ]")
        print(f"  • 带入：eta = [ ({RHO_STEEL} - {RHO_OIL}) * {G} * {d_actual_m:.6f}² * {t_time} ] /")
        print(f"                 [ 18 * {S_DISTANCE} * (1 + {K_COEFF} * ({d_actual_m:.6f} / {D_CYLINDER})) ]")
        print(f"  • 结果：在温度 T = {temp}°C 时，计算所得黏度 eta = {eta:.4f} Pa·s")
        print("." * 50 + "\n")
        
        # 询问是否继续
        choice = input("👉 是否继续录入下一组数据？(直接按回车继续，输入 'q' 或 'n' 退出): ").strip().lower()
        if choice in ['q', 'n', 'no']:
            print("\n数据录入完毕，程序退出。祝你实验报告拿高分！")
            break
            
        group_count += 1

if __name__ == "__main__":
    main()

