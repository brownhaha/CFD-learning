# CFD 学习项目

这个项目用于记录三个月的 CFD 求解器研发学习路径。

## 目录结构

- `notes/`：课程笔记，包含公式、示意图和代码对应关系。
- `solvers/`：从零实现的小型数值求解器。
- `scripts/`：绘图、动画和验证脚本。
- `figures/`：笔记中使用的生成图片和动画。
- `outputs/`：求解器输出的数据文件。

## 继续学习前先读

如果是在新对话、新设备或隔一段时间后继续学习，请先阅读：

```text
cfd-learning/notes/learning_context.md
```

这个文件记录了学习目标、讲解约定、当前进度和下一步入口。

## 第一周

第一课建立有限体积法对守恒律的理解，并实现一个一维线性对流求解器。

当前主题包括：

- 守恒律和控制体直觉
- 有限体积更新公式
- 一维线性对流方程
- 一阶迎风格式
- CFL 的物理意义
- CFL 和稳定性的关系
- 数值耗散和数值扩散的初步直觉

## 运行命令

运行一维对流求解器：

```powershell
python .\cfd-learning\solvers\advection_1d.py
```

生成第一课基础图片：

```powershell
python .\cfd-learning\scripts\make_week01_figures.py
```

生成 CFL 稳定性静态对比图：

```powershell
python .\cfd-learning\scripts\compare_cfl_stability.py
python .\cfd-learning\scripts\compare_cfl_stability.py --save
```

运行 MUSCL + minmod 二阶重构求解器：

```powershell
python .\cfd-learning\solvers\advection_1d_muscl.py
```

生成一阶迎风和 MUSCL 的结果对比图：

```powershell
python .\cfd-learning\scripts\compare_upwind_muscl.py
python .\cfd-learning\scripts\compare_upwind_muscl.py --save
```

诊断波峰位置误差和幅值误差：

```powershell
python .\cfd-learning\scripts\diagnose_peak_error.py
python .\cfd-learning\scripts\diagnose_peak_error.py --save
```

打开 CFL 动态演化窗口：

```powershell
python .\cfd-learning\scripts\animate_cfl_advection.py
```

如果需要保存 GIF：

```powershell
python .\cfd-learning\scripts\animate_cfl_advection.py --save
```

## 学习存档

- `cfd-learning/notes/latest_checkpoint.md`：最新学习断点。
- `cfd-learning/notes/day02_muscl_error_archive.md`：MUSCL、耗散误差、相位误差和下一步 limiter 对比计划。
