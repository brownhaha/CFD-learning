# 第二天学习存档：MUSCL、耗散误差与相位误差

## 1. 今日学习主题

今天围绕 MUSCL 重构后的结果诊断展开，重点是：

- 如何判断一个格式是不是更少耗散。
- 为什么只看波峰高度不够。
- 耗散误差和相位误差的区别。
- 为什么 `minmod` 限制器比较保守。
- 下一步为什么要比较不同 limiter。

## 2. 已完成的代码工作

新增 MUSCL 求解器：

```text
cfd-learning/solvers/advection_1d_muscl.py
```

新增一阶迎风与 MUSCL 对比脚本：

```text
cfd-learning/scripts/compare_upwind_muscl.py
```

新增波峰误差诊断脚本：

```text
cfd-learning/scripts/diagnose_peak_error.py
```

新增 MUSCL 笔记：

```text
cfd-learning/notes/week02_muscl_reconstruction.md
```

## 3. 绘图脚本约定

已达成新约定：

> 后续绘图脚本默认运行后弹出图形窗口；只有显式传入 `--save` 时才保存图片或动画。

例如：

```powershell
python .\cfd-learning\scripts\compare_upwind_muscl.py
```

默认弹窗。

```powershell
python .\cfd-learning\scripts\compare_upwind_muscl.py --save
```

保存图片。

## 4. MUSCL 代码中的关键经验

最初只加入 MUSCL 空间重构，但时间推进仍用一阶 Euler，结果出现不稳定。

因此 MUSCL 求解器改成：

```text
MUSCL + minmod + TVD RK2
```

经验：

> 空间格式和时间格式要匹配。只升级空间离散，不升级时间推进，可能导致整体格式不稳定或精度不匹配。

TVD RK2 写成：

$$
U^{(1)}
=
U^n
+
\Delta t L(U^n),
$$

$$
U^{n+1}
=
\frac12 U^n
+
\frac12
\left[
U^{(1)}
+
\Delta t L(U^{(1)})
\right].
$$

其中 \(L(U)\) 是有限体积空间离散算子。

## 5. 一阶迎风与 MUSCL 的误差对比

在当前参数：

```text
nx = 200
CFL = 0.8
final_time = 1.0
```

下，误差为：

```text
一阶迎风 L1 error = 2.037210e-02
MUSCL    L1 error = 1.788616e-02
```

结论：

> MUSCL 的整体 L1 误差更小，说明整体波形分布更接近精确解。

但这并不意味着每一个局部指标都明显改善。

## 6. 峰值诊断结果

使用：

```powershell
python .\cfd-learning\scripts\diagnose_peak_error.py --save
```

得到：

```text
scheme                     x_peak     u_peak   phase_dx     amp_du
initial                  0.297500   0.998751   0.000000   0.000000
first-order upwind       0.302500   0.844631   0.005000  -0.154120
MUSCL + minmod           0.292500   0.846025  -0.005000  -0.152726
```

从峰值高度看：

- 一阶迎风峰值损失：\(-0.154120\)
- MUSCL 峰值损失：\(-0.152726\)

所以在这个算例里：

> 只看波峰高度，MUSCL 和一阶迎风的耗散差不多。

从峰值位置看：

- 一阶迎风波峰偏右 \(+0.005\)
- MUSCL 波峰偏左 \(-0.005\)

这说明二者相位误差方向不同。

## 7. 耗散误差与相位误差

今天建立的关键区分：

```text
耗散误差：波被抹平，幅值降低，尖锐结构变宽。
相位误差：波跑错位置，传播速度不完全正确。
```

判断格式时不要只看：

```text
峰值高不高
```

还要看：

```text
1. 幅值对不对       -> 耗散
2. 位置对不对       -> 相位误差/色散误差
3. 形状对不对       -> 耗散 + 色散
4. 守恒量对不对     -> 有限体积核心
```

核心句：

> 耗散看波有没有被抹平；相位误差看波有没有跑错位置。一个格式可能峰值看起来还行，但位置错了；也可能位置对了，但幅值被吃掉。

## 8. 为什么 minmod 的改善不夸张

`minmod` 限制器比较保守。

它的行为可以理解为：

> 宁可少给斜率，也不冒险。

在波峰附近，左右斜率异号，`minmod` 会把斜率压成 0。

因此在局部极值附近，MUSCL + minmod 会退化得接近一阶格式。

这解释了为什么：

- MUSCL 的整体误差更小。
- 但峰值高度没有明显比一阶迎风更好。

## 9. 下一步学习计划

下一步要比较不同 limiter：

```text
minmod   -> 最保守，最稳，耗散较大
MC       -> 折中，常用，比较稳
van Leer -> 平滑，不那么突然截断斜率
Superbee -> 锐利，低耗散，但更激进
```

计划把 MUSCL 求解器扩展成：

```text
--limiter minmod
--limiter mc
--limiter vanleer
--limiter superbee
```

并画图比较：

```text
一阶迎风
MUSCL + minmod
MUSCL + MC
MUSCL + van Leer
MUSCL + Superbee
```

目标是看到不同 limiter 的“性格”如何体现在波形上。

