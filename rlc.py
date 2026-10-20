import math

def calculate_phi(f, dt):
    """
    计算相位差 phi = 2 * pi * f * dt
    f: 频率，单位 Hz
    dt: 时间差，单位 s
    """
    return 2 * math.pi * f * dt

def main():
    print("=" * 60)
    print("表格 1 (RC串联) 相位差计算")
    print("=" * 60)
    # 数据录入：频率 f (Hz), 时间差 dt (s)
    data_table1 = [
        (300, -0.8e-3),    # 300 Hz, -0.8 ms
        (500, -0.4e-3),    # 500 Hz, -0.4 ms
        (1000, -0.16e-3),  # 1k Hz, -0.16 ms
        (1836, -60e-6),    # 1.836k Hz, -60 us
        (3000, -24e-6),    # 3k Hz, -24 us
        (5000, -10e-6)     # 5k Hz, -10 us
    ]

    print(f"{'频率 f (Hz)':<15} | {'时间差 Δt (s)':<18} | {'相位差 φ (rad)':<15}")
    print("-" * 60)
    for f, dt in data_table1:
        phi = calculate_phi(f, dt)
        print(f"{f:<15} | {dt:<18.6e} | {phi:<15.2f}")

    print("\n" + "=" * 60)
    print("表格 3 (RLC串联) 相位差计算")
    print("=" * 60)
    # 数据录入：频率 f (Hz), 时间差 dt (s)
    data_table3 = [
        (1755, -0.14e-3),   # 1.755k Hz, -0.14 ms
        (7662, -22e-6),     # 7.662k Hz, -22 us
        (10190, -10e-6),    # 10.19k Hz, -10 us
        (15390, 0),         # 15.39k Hz, 0
        (22680, 5e-6),      # 22.68k Hz, 5 us
        (29560, 6e-6),      # 29.56k Hz, 6 us
        (62470, 4e-6)       # 62.47k Hz, 4 us
    ]

    print(f"{'频率 f (Hz)':<15} | {'时间差 Δt (s)':<18} | {'相位差 φ (rad)':<15}")
    print("-" * 60)
    for f, dt in data_table3:
        phi = calculate_phi(f, dt)
        print(f"{f:<15} | {dt:<18.6e} | {phi:<15.2f}")

if __name__ == "__main__":
    main()
