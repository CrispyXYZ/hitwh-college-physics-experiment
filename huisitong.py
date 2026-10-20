import math

# ==========================================
# 仪器铭牌参数配置区 (如仪器规格不同，请在此处修改)
# ==========================================
INSTRUMENT_NAME = "Zx21 直流多值十进电阻箱"

# 误差率配置 (根据铭牌上的 PPM 值换算)
# 万位、千位、百位：1000 PPM = 0.1%
RATE_10K = 0.001  # 万位
RATE_1K  = 0.001  # 千位
RATE_100 = 0.001  # 百位
# 十位：2000 PPM = 0.2%
RATE_10  = 0.002  
# 个位：5000 PPM = 0.5%
RATE_1   = 0.005  
# 十分位：50000 PPM = 5%
RATE_01  = 0.05   

# 零电阻 (铭牌上 Ro = (30 ± 10)mΩ)
ZERO_RESISTANCE_B = 0.03  # 单位：Ω

# ==========================================
# 计算核心逻辑
# ==========================================

def print_instrument_specs():
    """打印当前内置的仪器铭牌参数，供用户核对"""
    print("\n" + "="*50)
    print("  当前内置的仪器参数 (请核对是否与实际仪器一致)  ")
    print("="*50)
    print(f"仪器型号: {INSTRUMENT_NAME}")
    print("误差限 (准确度等级):")
    print(f"  - 万位, 千位, 百位 : {RATE_10K*100}% ({RATE_10K:.3f})")
    print(f"  - 十位             : {RATE_10*100}% ({RATE_10:.3f})")
    print(f"  - 个位             : {RATE_1*100}% ({RATE_1:.3f})")
    print(f"  - 十分位           : {RATE_01*100}% ({RATE_01:.3f})")
    print(f"零点误差 b         : {ZERO_RESISTANCE_B} Ω (即 {ZERO_RESISTANCE_B*1000:.0f}mΩ)")
    print("="*50)
    print("提示: 如果您的仪器参数与此不同，请按提示修改代码顶部的配置区！")
    print("="*50 + "\n")

def get_delta_r0_info(r_val):
    """
    根据电阻箱读数计算 Delta_R0，并生成完整式子和代值字符串。
    """
    s_val = f"{r_val:.1f}" # 强制保留一位小数
    parts = s_val.split('.')
    int_part = parts[0].zfill(5) # 补全万、千、百、十、个位
    dec_part = parts[1] if len(parts) > 1 else "0"
    
    rates = [RATE_10K, RATE_1K, RATE_100, RATE_10, RATE_1] # 万、千、百、十、个位
    delta_r0 = 0.0
    m = 0
    
    formula_terms = [] 
    value_terms = []   
    
    # 整数部分解析
    for i, char in enumerate(int_part):
        if char != '0':
            digit = int(char)
            place_value = 10 ** (4 - i)
            rate = rates[i]
            
            prod = digit * place_value * rate
            delta_r0 += prod
            m += 1
            
            formula_terms.append(f"{digit * place_value}×{rate*100}%")
            value_terms.append(f"{prod:g}")
            
    # 十分位解析
    if dec_part and dec_part[0] != '0':
        digit = int(dec_part[0])
        prod = digit * 0.1 * RATE_01
        delta_r0 += prod
        m += 1
        
        formula_terms.append(f"{digit * 0.1}×{RATE_01*100}%")
        value_terms.append(f"{prod:g}")
        
    # 加上零点误差 m * b
    delta_r0 += m * ZERO_RESISTANCE_B
    
    # 拼接完整式子
    formula_str = " + ".join(formula_terms)
    value_str = " + ".join(value_terms)
    
    # 形成最终输出的完整代值式子字符串
    full_calc_str = f"ΔR0 = {formula_str} + {m}×{ZERO_RESISTANCE_B} = {value_str} + {m}×{ZERO_RESISTANCE_B} = {delta_r0:.4f} Ω"
    
    return delta_r0, m, full_calc_str

def round_ur(ur_val):
    """
    根据黑板要求修约 U_R: 首位数字是1或2时保留2位有效数字，否则保留1位。
    """
    if ur_val == 0:
        return 0.0, 0
    exponent = math.floor(math.log10(abs(ur_val)))
    first_digit = int(ur_val / (10 ** exponent))
    
    if first_digit in [1, 2]:
        decimals = max(0, -(exponent - 1))
        rounded_ur = round(ur_val, decimals)
    else:
        decimals = max(0, -exponent)
        rounded_ur = round(ur_val, decimals)
        
    return rounded_ur, decimals

def process_data():
    try:
        # 1. 获取用户输入
        R0 = float(input("请输入 R0 (未互换时电阻箱读数, 单位Ω，如 509.2): "))
        R0_prime = float(input("请输入 R0' (互换后电阻箱读数, 单位Ω，如 505.5): "))
        
        dR = float(input("请输入 ΔR (未互换时调节量, 单位Ω, 如 1.0): "))
        dI = float(input("请输入 ΔI (未互换时电流偏转量, 单位μA, 如 0.307): "))
        Im = float(input("请输入 Im (未互换时偏离零点数值, 单位μA, 如 0.012): "))
        
        dR_prime = float(input("请输入 ΔR' (互换后调节量, 单位Ω, 如 1.0): "))
        dI_prime = float(input("请输入 ΔI' (互换后电流偏转量, 单位μA, 如 0.354): "))
        Im_prime = float(input("请输入 Im' (互换后偏离零点数值, 单位μA, 如 0.009): "))

        print("\n" + "-"*20 + " 计算过程 " + "-"*20)

        # 2. 计算 Rx
        Rx = math.sqrt(R0 * R0_prime)
        print(f"1. 计算 Rx: Rx = √(R0 × R0') = √({R0} × {R0_prime}) = √{R0*R0_prime:.4f} ≈ {Rx:.4f} Ω")

        # 3. 计算 Delta R0 和 Delta R0' (包含完整式子)
        delta_R0, m1, calc_str1 = get_delta_r0_info(R0)
        delta_R0_prime, m2, calc_str2 = get_delta_r0_info(R0_prime)
        
        print(f"\n2. 电阻箱仪器误差 ΔR0 (完整公式与代入数值):")
        print(f"   [公式] ΔR0 = Σ(Ri × fi) + m × b")
        print(f"   {calc_str1}")
        print(f"   {calc_str2}")

        # 4. 计算灵敏度误差项 Im/S
        term1 = (Im * dR) / (R0 * dI)
        term2 = (Im_prime * dR_prime) / (R0_prime * dI_prime)
        
        print(f"\n3. 电桥灵敏度误差项 Im/S:")
        print(f"   Im/S = (Im × ΔR) / (R0 × ΔI) = ({Im} × {dR}) / ({R0} × {dI}) = {Im*dR:.4f} / {R0*dI:.4f} ≈ {term1:.2e}")
        print(f"   Im'/S' = (Im' × ΔR') / (R0' × ΔI') = ({Im_prime} × {dR_prime}) / ({R0_prime} × {dI_prime}) = {Im_prime*dR_prime:.4f} / {R0_prime*dI_prime:.4f} ≈ {term2:.2e}")

        # 5. 计算相对不确定度 ER 和 UR (引入 sqrt(3) 修正)
        sqrt3 = math.sqrt(3)
        
        # 对电阻箱仪器误差项除以 sqrt(3)
        term_A = (delta_R0 / (sqrt3 * R0)) ** 2
        term_B = (delta_R0_prime / (sqrt3 * R0_prime)) ** 2
        term_C = term1 ** 2
        term_D = term2 ** 2
        
        ER = 0.5 * math.sqrt(term_A + term_B + term_C + term_D)
        UR = Rx * ER
        
        print(f"\n4. 合成相对不确定度 ER:")
        print(f"   ER = 0.5 × √[(ΔR0/(√3×R0))² + (ΔR0'/(√3×R0'))² + (Im/S)² + (Im'/S')²]")
        print(f"   ER = 0.5 × √[({delta_R0}/(√3×{R0}))² + ({delta_R0_prime}/(√3×{R0_prime}))² + ({term1:.2e})² + ({term2:.2e})²] = {ER:.6f}")

        print(f"\n5. 计算绝对不确定度 UR:")
        print(f"   UR = Rx × ER = {Rx:.4f} × {ER:.6f} = {UR:.4f} Ω")

        # 6. 修约并输出最终结果
        UR_rounded, decimals = round_ur(UR)
        Rx_rounded = round(Rx, decimals)
        
        print(f"\n6. 修约 (UR首位为1或2时保留2位有效数字，否则保留1位):")
        print(f"   UR修约: {UR:.4f} -> {UR_rounded}")
        print(f"   Rx 末位与 UR 对齐: {Rx:.4f} -> {Rx_rounded}")

        print("\n" + "*"*45)
        print(f"最终结果表达式:")
        print(f"Rx = ({Rx_rounded} ± {UR_rounded}) Ω  (P=0.683)")
        print("*"*45)

    except ZeroDivisionError:
        print("错误：输入的数据中存在分母为0的情况，请检查 ΔI 或 ΔI' 是否为0。")
    except ValueError:
        print("错误：请输入有效的数字。")

if __name__ == "__main__":
    # 程序启动时，先打印铭牌数据
    print_instrument_specs()
    
    while True:
        process_data()
        again = input("\n是否继续计算下一组数据? (输入 y 继续，输入 n 退出): ").strip().lower()
        if again != 'y':
            print("计算结束，祝实验报告顺利！")
            break
