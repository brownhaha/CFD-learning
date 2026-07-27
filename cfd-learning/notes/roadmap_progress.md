# CFD 学习路线与当前进度

更新时间：2026-07-15

## 1. 总体阶段图

```mermaid
flowchart LR
    A["阶段 0<br/>学习框架与目标"] --> B["阶段 1<br/>有限体积基础"]
    B --> C["阶段 2<br/>高阶重构与 limiter"]
    C --> D["阶段 3<br/>Euler 方程与 Riemann solver"]
    D --> E["阶段 4<br/>Navier-Stokes / 粘性项"]
    E --> F["阶段 5<br/>OpenFOAM / 工程化"]
    F --> G["阶段 6<br/>ROM / POD / BCI-ROM 入门"]
    G --> H["阶段 7<br/>论文复现与求职项目"]

    A:::done
    B:::done
    C:::now
    D:::todo
    E:::todo
    F:::todo
    G:::todo
    H:::todo

    classDef done fill:#dcfce7,stroke:#16a34a,color:#14532d;
    classDef now fill:#fef9c3,stroke:#ca8a04,color:#713f12;
    classDef todo fill:#f3f4f6,stroke:#6b7280,color:#374151;
```

当前处于：

```text
阶段 2：高阶重构与 limiter
```

也就是已经从有限体积基础进入现代有限体积格式的核心部分。

## 2. 三个月路线中的位置

```text
第 1 月：有限体积求解器基础
  [████████░░] 约 80%

第 2 月：Euler / Navier-Stokes / OpenFOAM
  [░░░░░░░░░░] 尚未正式开始

第 3 月：论文复现 / ROM / 求职项目
  [░░░░░░░░░░] 尚未正式开始
```

当前已经掌握或正在掌握：

```text
有限体积守恒更新公式
CFL 物理意义与稳定性
数值耗散 / 数值扩散
相位误差 / L1 误差
一阶迎风格式
MUSCL 分片线性重构
minmod / MC / van Leer / Superbee limiter 对比
TVD RK2 时间推进
```

正在重点形成的能力：

```text
从图形和指标判断格式误差
区分耗散误差和相位误差
理解 limiter 在稳定性和低耗散之间的取舍
理解空间重构、通量、残差、时间推进之间的求解器结构关系
```

## 3. 接下来的学习计划

### 3.1 完成 1D 标量方程训练

目标：把一维对流方程作为数值格式实验台彻底玩透。

任务：

```text
1. 对比不同 limiter 在高斯波、方波、三角波上的表现。
2. 观察耗散、相位误差、振荡、间断厚度。
3. 加入质量守恒检查。
4. 做网格收敛性分析。
```

预期掌握：

```text
什么叫稳定
什么叫耗散
什么叫色散
什么叫 limiter 保边
什么叫高阶格式退化
```

### 3.2 进入 1D Euler 方程

这是从玩具方程走向真正 CFD 的关键。

需要掌握守恒变量：

```text
rho
rho * u
E
```

需要掌握通量：

```text
质量通量
动量通量
能量通量
```

典型算例：

```text
Sod shock tube
Lax shock tube
blast wave
```

核心概念：

```text
特征速度
声速
激波
接触间断
稀疏波
Riemann solver
```

### 3.3 学习 Riemann solver

建议顺序：

```text
Rusanov / Local Lax-Friedrichs
-> HLL
-> HLLC
-> Roe
```

目标：

```text
真正理解可压缩 CFD 求解器如何在界面处计算通量。
```

### 3.4 进入 2D 有限体积

内容：

```text
二维结构网格
x/y 方向通量
边界条件
二维对流
二维 Euler
```

目标：

```text
理解多维通量如何组装。
理解 ghost cell 如何处理边界。
理解 CFL 在二维里怎么定义。
```

### 3.5 Navier-Stokes 与粘性项

内容：

```text
扩散项离散
粘性通量
Reynolds 数
边界层基本直觉
```

目标：

```text
为不可压流、湍流模型和 OpenFOAM 学习打基础。
```

### 3.6 OpenFOAM / 工程化

内容：

```text
读懂 solver 结构
理解 fvMatrix
理解 div(phi,U), laplacian(nu,U)
改一个简单 solver
加源项或自定义输运方程
```

目标：

```text
从自研小求解器过渡到工业/开源 CFD 框架。
```

### 3.7 ROM / POD / BCI-ROM 铺垫

前置能力：

```text
会生成 FOM 数据
会理解边界条件
会理解状态变量
会做 SVD/POD
会构造低维基
```

之后进入：

```text
POD-ROM
Galerkin projection
边界条件 lifting
参数化入口条件
BCI-ROM
```

目标：

```text
三个月内达到能讲清楚 BCI-ROM 思想，并做一个简化复现或原型项目。
```

## 4. 下一节建议

下一节建议做：

```text
方波/间断初值下的 limiter 对比
```

原因：

```text
高斯波太光滑，limiter 差异不够残酷。
方波会更清楚地展示 limiter 在间断附近的性格。
```

预计观察：

```text
minmod 抹宽
Superbee 保边
MC 折中
van Leer 平滑
是否出现振荡
间断厚度如何变化
```

## 5. 当前继续入口

下次可以直接说：

```text
继续 CFD 学习，从方波/间断初值下的 limiter 对比开始。
```

