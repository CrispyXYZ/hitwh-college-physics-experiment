import matplotlib.pyplot as plt
import numpy as np

# 角度数据（度）
theta_deg = [x for x in range(0, 361, 10)]

# 椭圆偏振数据（自己填）
r_old = []

# 圆偏振数据（自己填）
r_new = []

# 转换为弧度
theta_rad = np.radians(theta_deg)

# 创建极坐标图
plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection='polar')

# 第一组曲线：三角形标记 + 实线
ax.plot(theta_rad, r_old, marker='^', markersize=6, linewidth=1.5,
        linestyle='-', color='black', label=r'$\alpha = 30 ^\circ$')

# 第二组曲线：圆形标记 + 虚线
ax.plot(theta_rad, r_new, marker='o', markersize=6, linewidth=1.5,
        linestyle='--', color='black', label=r'\alpha = 45 ^\circ$')

# 图例
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

ax.set_title('', va='bottom')
plt.show()