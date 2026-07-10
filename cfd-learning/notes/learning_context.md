# CFD 学习上下文

这份文件用于在新对话、新设备或隔一段时间后快速续上当前学习状态。

## 1. 学习目标

三个月目标：

- 建立 CFD 前沿求解器研发能力
- 能读懂并复现论文中的核心数值方法
- 能完成一个可展示的小型求解器项目
- 能面向求职讲清楚数值格式、稳定性、边界条件、OpenFOAM 二次开发和工程取舍

目标不是只会使用 CFD 软件，而是逐步具备：

- 求解器数学与物理直觉
- 有限体积/高阶格式/稳定性分析能力
- C++/Python 实现能力
- OpenFOAM 或类似框架的二次开发能力
- 论文复现和项目表达能力

## 2. 当前基础画像

学习者当前情况：

- 数学基础很久没系统复习，属于能看懂、能较快想起来，但不常用会忘
- C++ 和 Python 会用
- 用过 OpenFOAM、Fluent 和自研代码
- 希望以市场需求为导向学习
- 工作日每天约 3 小时，周末每天约 8 小时
- 期望产出包括论文复现、求解器项目和找工作能力

因此学习策略应是：

- 不按零基础慢速讲解
- 但关键公式必须建立物理直觉
- 每个公式尽量配图、配代码、配算例
- 少堆抽象概念，多把数学、物理和程序实现对应起来

## 3. 已达成的讲解约定

后续讲解默认采用：

1. 公式使用 LaTeX 块公式，避免难读的纯文本公式。
2. 重要公式后立即解释符号含义。
3. 数学、物理直觉和代码实现分开讲。
4. 尽量配合示意图、结果图或流程图。
5. 复杂推导分层展开：先物理意义，再公式，再代码。
6. 如果某个公式不符合直觉，优先用总量、平均量、单位量来解释。
7. 后续新增或更新的 Markdown 文档默认使用中文记录，除非英文术语、代码标识符或论文原文必须保留英文。
8. 后续绘图脚本默认运行后弹出图形窗口；只有显式传入 `--save` 时才把图片或动画保存到 `figures/`。

推荐讲解结构：

```text
物理图像 -> 控制体/守恒关系 -> 数学公式 -> 代码实现 -> 数值结果 -> 误差或稳定性解释
```

## 4. 已完成的第一课内容

第一课主题：

```text
有限体积法的几何意义 + 1D 线性对流方程 + CFL 初步直觉
```

已经建立的核心公式：

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

已经达成的关键共识：

- \(\left(F_{i+\frac12}-F_{i-\frac12}\right)\Delta t\) 表示一个时间步内 cell 的总量变化。
- \(U_i\) 存的通常不是总量，而是 cell average。
- 因此需要除以 \(\Delta x\)，把总量变化换算成平均值变化。
- 如果直接更新总量 \(Q_i\)，公式中不会出现 \(\Delta x\)：

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

- 因为 \(Q_i=U_i\Delta x\)，把总量公式换成平均值公式后，就自然出现 \(\Delta x\)。

## 5. CFL 当前理解断点

对于一维线性对流：

$$
\frac{\partial u}{\partial t}
+
a\frac{\partial u}{\partial x}
=
0
$$

当 \(a>0\) 时，信息从左向右传播，一阶迎风格式可以写成：

$$
U_i^{n+1}
=
U_i^n
-
\mathrm{CFL}
\left(
U_i^n
-
U_{i-1}^n
\right)
$$

进一步改写为：

$$
U_i^{n+1}
=
(1-\mathrm{CFL})U_i^n
+
\mathrm{CFL}U_{i-1}^n
$$

已达成理解：

- 新的 \(U_i\) 是当前 cell 和左侧上游 cell 的加权组合。
- \(\mathrm{CFL}\) 决定从左侧 cell 接收多少信息。
- \(\mathrm{CFL}=0.2\)：保留 80% 自己旧状态，接收 20% 左侧信息。
- \(\mathrm{CFL}=0.8\)：保留 20% 自己旧状态，接收 80% 左侧信息。
- 这就是“按 CFL 比例把信息从左往右传”的含义。

CFL 定义：

$$
\mathrm{CFL}
=
\frac{|a|\Delta t}{\Delta x}
$$

物理直觉：

> CFL 表示一个时间步内信息走过了几个网格宽度。

## 6. 当前项目文件

已有文件：

- `cfd-learning/README.md`
- `cfd-learning/notes/week01_finite_volume.md`
- `cfd-learning/notes/week01_take_home_review.md`
- `cfd-learning/notes/learning_context.md`
- `cfd-learning/solvers/advection_1d.py`
- `cfd-learning/scripts/make_week01_figures.py`
- `cfd-learning/figures/finite_volume_cell.png`
- `cfd-learning/figures/advection_result.png`
- `cfd-learning/outputs/advection_1d.npz`

已验证运行：

```text
nx          = 200
CFL         = 0.8
final_time  = 1.0
L1 error    = 2.037210e-02
Linf error  = 1.546376e-01
```

观察结果：

- 高斯波包经过一个周期后位置基本回到原处。
- 波峰降低、波形变宽。
- 这说明一阶迎风格式稳定，但有明显数值耗散。

## 7. 下一次继续的建议入口

下一次对话可以直接从这里开始：

```text
继续 CFD 学习。请先读取 cfd-learning/notes/learning_context.md，
然后从 CFL 为什么影响稳定性开始讲。
```

或者更短：

```text
继续第一课，从 CFL 稳定性开始。
```

下一节建议内容：

1. 为什么 \(\mathrm{CFL}\le 1\) 时是一种正常加权平均。
2. 为什么 \(\mathrm{CFL}>1\) 时变成外推，容易放大误差。
3. 用简单数值例子解释振荡和发散。
4. 对比不同 CFL 下的数值结果。
5. 连接到真实 CFD 中的局部波速和时间步限制。
