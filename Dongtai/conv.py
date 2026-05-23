import sys


def get_float_input(prompt):
    """安全获取浮点数输入的函数"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("输入不能为空，请重新输入。")
                continue
            return float(user_input)
        except ValueError:
            print("输入格式错误！请输入有效的数字（支持科学计数法，如 2uF 输入 2e-6）。")


def main():
    print("=" * 50)
    print("       磁滞回线与基本磁化曲线数据处理程序")
    print("=" * 50)

    # 1. 选择样品并加载已知图像参数
    while True:
        choice = input("请选择实验样品 [1 或 2]: ").strip()
        if choice == "1":
            L = 0.130  # 平均磁路长度 (m)
            S = 1.24e-4  # 截面积 (m^2)
            N1 = 150  # 原边匝数
            N2 = 150  # 副边匝数
            print("已加载【样品1】参数: L=0.130m, S=1.24e-4 m^2, N1=N2=150")
            break
        elif choice == "2":
            L = 0.075  # 平均磁路长度 (m)
            S = 1.24e-4  # 截面积 (m^2)
            N1 = 150  # 原边匝数
            N2 = 150  # 副边匝数
            print("已加载【样品2】参数: L=0.075m, S=1.24e-4 m^2, N1=N2=150")
            break
        else:
            print("输入错误，请输入 1 或 2。")

    print("\n" + "-" * 40)
    print("请输入以下实验仪器缺失参数（请注意单位）：")
    print("-" * 40)

    # 2. 提示用户输入缺失的仪器常数
    R1 = get_float_input("1. 请输入采样电阻 R1 的值 (单位: 欧姆 Ω): ")
    R2 = get_float_input("2. 请输入积分电阻 R2 的值 (单位: 欧姆 Ω): ")
    print("提示：电容 C 格式支持科学计数法，例如 1微法(1μF) 请输入 1e-6")
    C = get_float_input("3. 请输入积分电容 C 的值 (单位: 法拉 F): ")
    Sx = get_float_input("4. 请输入示波器 X 轴灵敏度 Sx (单位: V/格): ")
    Sy = get_float_input("5. 请输入示波器 Y 轴灵敏度 Sy (单位: V/格): ")

    # 3. 预先计算公式中的常数系数，提高循环效率
    factor_H = (N1 * Sx) / (L * R1)
    factor_B = (R2 * C * Sy) / (N2 * S)

    # 4. 循环读取 X 计算磁场强度 H
    print("\n" + "=" * 50)
    print("第一部分：开始循环计算磁场强度 H")
    print("提示：直接输入 X 的格数即可计算；输入 'q' 或直接回车可结束此轮计算。")
    print("=" * 50)

    x_count = 1
    while True:
        user_in = (
            input(f"[{x_count}] 请输入 X 轴坐标格数 (或输入 'q' 退出): ")
            .strip()
            .lower()
        )
        if user_in == "q" or user_in == "":
            print("已结束 H 的计算。")
            break
        try:
            X = float(user_in)
            H = X * factor_H
            print(f"    --> 计算结果: H = {H:.4f} A/m")
            x_count += 1
        except ValueError:
            print("    输入无效，请输入数字或 'q'。")

    # 5. 循环读取 Y 计算磁感应强度 B
    print("\n" + "=" * 50)
    print("第二部分：开始循环计算磁感应强度 B")
    print("提示：直接输入 Y 的格数即可计算；输入 'q' 或直接回车可结束此轮计算。")
    print("=" * 50)

    y_count = 1
    while True:
        user_in = (
            input(f"[{y_count}] 请输入 Y 轴坐标格数 (或输入 'q' 退出): ")
            .strip()
            .lower()
        )
        if user_in == "q" or user_in == "":
            print("已结束 B 的计算。")
            break
        try:
            Y = float(user_in)
            B = Y * factor_B
            print(f"    --> 计算结果: B = {B:.6f} T (特斯拉)")
            y_count += 1
        except ValueError:
            print("    输入无效，请输入数字或 'q'。")

    print("\n数据处理完毕，程序退出。祝你实验报告顺利拿高分！")


if __name__ == "__main__":
    main()