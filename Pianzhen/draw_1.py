import matplotlib.pyplot as plt

# 生成 x 和 y 数据
x = [x for x in range(0, 361, 10)]
y = [0.375, 0.36, 0.32, 0.27, 0.238, 0.171, 0.085, 0.048, 0.01, 0.0,
     0.012, 0.045, 0.101, 0.161, 0.228, 0.272, 0.326, 0.342, 0.335, 0.325,
     0.315, 0.287, 0.225, 0.149, 0.086, 0.043, 0.011, 0.0, 0.012, 0.05,
     0.107, 0.157, 0.23, 0.312, 0.357, 0.408, 0.409]
# 数据仅做示例，实际数据请根据需要进行修改

# 绘制直角坐标系图
plt.figure(figsize=(10, 5))
plt.plot(x, y, marker='o', markersize=4, linewidth=1.5, color='steelblue')

# 纵轴标注 I/mW，横轴标注 θ/°
plt.ylabel(r'$I$ / mW)')
plt.xlabel(r'$\theta$ / $^\circ$')

plt.grid(True, linestyle='--', alpha=0.7)
plt.show()