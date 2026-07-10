# 第一周回家复习：有限体积直觉

这份笔记用于下班后复习，不依赖本机代码环境。

## 1. 今天最重要的公式

有限体积法的一维更新公式是：

$$
U_i^{n+1}
=
U_i^n
-
\frac{\Delta t}{\Delta x}
\left(
F_{i+\frac12}
-
F_{i-\frac12}
\right)
$$

它的口语版本是：

> 新的单元平均值 = 旧的单元平均值 - 单位体积内的净流出量

其中：

- \(U_i^n\)：第 \(i\) 个 cell 在第 \(n\) 个时间步的平均值
- \(F_{i-\frac12}\)：左边界面的通量
- \(F_{i+\frac12}\)：右边界面的通量
- \(\Delta t\)：一个时间步有多长
- \(\Delta x\)：一个 cell 有多宽

## 2. 为什么要除以 \(\Delta x\)

通量差乘以时间：

$$
\left(
F_{i+\frac12}
-
F_{i-\frac12}
\right)\Delta t
$$

表示的是这个时间步内 cell 的总量变化。

但是求解器里存的 \(U_i\) 通常不是 cell 里的总量，而是 cell average：

$$
U_i
=
\frac{Q_i}{\Delta x}
$$

也就是：

$$
Q_i
=
U_i\Delta x
$$

如果先写总量更新，就没有除以 \(\Delta x\)：

$$
Q_i^{n+1}
=
Q_i^n
-
\Delta t
\left(
F_{i+\frac12}
-
F_{i-\frac12}
\right)
$$

代入 \(Q_i = U_i\Delta x\)：

$$
U_i^{n+1}\Delta x
=
U_i^n\Delta x
-
\Delta t
\left(
F_{i+\frac12}
-
F_{i-\frac12}
\right)
$$

两边除以 \(\Delta x\)，就得到：

$$
U_i^{n+1}
=
U_i^n
-
\frac{\Delta t}{\Delta x}
\left(
F_{i+\frac12}
-
F_{i-\frac12}
\right)
$$

所以：

> 通量差乘以 \(\Delta t\) 给的是总量变化；除以 \(\Delta x\) 是把总量变化换算成平均值变化。

一个直觉例子：

- 同样流出 4 单位的水
- 如果 cell 长度是 1，平均值下降 \(4 / 1 = 4\)
- 如果 cell 长度是 4，平均值下降 \(4 / 4 = 1\)

cell 越大，同样的总量变化摊到更大的空间里，平均值变化越小。

## 3. 线性对流方程

第一课的模型问题是：

$$
\frac{\partial u}{\partial t}
+
a\frac{\partial u}{\partial x}
=
0
$$

也可以写成守恒形式：

$$
\frac{\partial u}{\partial t}
+
\frac{\partial (au)}{\partial x}
=
0
$$

因此通量是：

$$
f(u) = au
$$

当 \(a > 0\) 时，信息从左往右传播，所以界面 \(i+\frac12\) 的通量取左侧 cell 的值：

$$
F_{i+\frac12}
=
aU_i
$$

这就是一阶迎风格式。

## 4. CFL 的直觉

CFL 数定义为：

$$
\mathrm{CFL}
=
\frac{|a|\Delta t}{\Delta x}
$$

它表示：

> 一个时间步内，信息走过了几个网格宽度。

例如：

- \(\mathrm{CFL}=0.2\)：一个时间步走过 20% 个 cell
- \(\mathrm{CFL}=0.8\)：一个时间步走过 80% 个 cell
- \(\mathrm{CFL}=1.0\)：一个时间步刚好走过 1 个 cell

对于 \(a>0\) 的一阶迎风格式，更新公式可以写成：

$$
U_i^{n+1}
=
U_i^n
-
\mathrm{CFL}
\left(
U_i^n - U_{i-1}^n
\right)
$$

把它展开：

$$
U_i^{n+1}
=
(1-\mathrm{CFL})U_i^n
+
\mathrm{CFL}U_{i-1}^n
$$

这说明新的 \(U_i\) 是两个旧值的加权平均：

- \((1-\mathrm{CFL})U_i^n\)：保留自己旧状态的比例
- \(\mathrm{CFL}U_{i-1}^n\)：接收左边邻居信息的比例

所以当 \(a>0\) 时：

> CFL 越大，cell \(i\) 在一个时间步内接收的左侧信息越多。

## 5. 为什么 CFL 太大会危险

如果 \(\mathrm{CFL} \le 1\)，那么：

$$
(1-\mathrm{CFL}) \ge 0
$$

此时：

$$
U_i^{n+1}
=
(1-\mathrm{CFL})U_i^n
+
\mathrm{CFL}U_{i-1}^n
$$

是一个正常的加权平均。

但如果 \(\mathrm{CFL} > 1\)，例如 \(\mathrm{CFL}=1.2\)，则：

$$
U_i^{n+1}
=
-0.2U_i^n
+
1.2U_{i-1}^n
$$

这不再是正常平均，而是在做外推。外推很容易放大误差，所以数值解可能振荡甚至发散。

## 6. 今天要记住的三句话

第一句：

> 有限体积法先更新 cell 里的总量，再换算成 cell 平均值。

第二句：

> 除以 \(\Delta x\) 是因为 \(U_i\) 存的是平均值，不是总量。

第三句：

> CFL 是一个时间步内信息走过的网格比例，也决定了当前 cell 从上游 cell 接收多少信息。

## 7. 回家后的思考题

不用写代码，只用纸笔想：

1. 如果 \(\Delta x\) 变成原来的两倍，而净流出总量不变，\(U_i\) 的变化会变大还是变小？
2. 如果 \(a>0\)，为什么 \(U_i^{n+1}\) 会看 \(U_{i-1}^n\)，而不是看 \(U_{i+1}^n\)？
3. 如果 \(\mathrm{CFL}=0.3\)，请把

   $$
   U_i^{n+1}
   =
   (1-\mathrm{CFL})U_i^n
   +
   \mathrm{CFL}U_{i-1}^n
   $$

   写成具体数字比例。

4. 如果 \(\mathrm{CFL}=1.2\)，为什么它不再是正常的加权平均？

## 8. 回家继续时直接发这句话

如果你在另一台电脑或手机上继续学习，可以直接发：

```text
我回来了，继续第一课。从 CFL 为什么会导致稳定性问题开始。
```
