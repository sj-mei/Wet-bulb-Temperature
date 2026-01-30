# atmos: fast and accurate calculations for applications in atmospheric science
_atmos：适用于大气科学应用的快速且精确计算库_


## What is atmos?
## atmos 是什么？

__atmos__ is a Python library for computing physical quantities commonly used in atmospheric science. The code comprises the following modules:
__atmos__ 是一个用于计算大气科学中常用物理量的 Python 库。代码由以下模块组成：
* _thermo_ - functions for calculating various thermodynamic quantities (density, wet-bulb temperature, potential temperature, etc.)
* _thermo_ - 用于计算各种热力学量的函数（密度、湿球温度、位温等）。
* _moisture_ - functions for convecting between different measures of atmospheric moisture (specific humidity, relative humidity, dewpoint temperature, etc.)
* _moisture_ - 在不同大气湿度指标之间转换的函数（比湿、相对湿度、露点温度等）。
* _parcel_ - functions for performing adiabatic and pseudoadiabatic parcel ascents to calculate convective available potential energy (CAPE) and convective inhibition (CIN) for surface-based, mixed-layer, most-unstable, and effective parcels
* _parcel_ - 用于执行绝热和伪绝热气块抬升的函数，以计算地面型、混合层、最不稳定以及有效气块的对流可用位能（CAPE）和对流抑制（CIN）。
* _kinematic_ - functions for converting between wind speed/direction and wind components (u and v) and for calculating kinematic quantities (bulk wind difference, storm-relative helicity, etc.)
* _kinematic_ - 在风速/风向与风矢量分量（u 和 v）之间转换，并计算动力学量（整层风差、风暴相对螺旋度等）的函数。
* _pseudoadiabat_ - functions for performing fast pseudoadiabatic calculations (see below)
* _pseudoadiabat_ - 用于进行快速伪绝热计算的函数（见下文）。
* _utils_ - generic functions for peforming interpolation and layer averaging of scalar and vector quantities
* _utils_ - 用于对标量和矢量量进行插值和层平均的通用函数。
* _constant_ - specifies physical constants used in the code
* _constant_ - 指定代码中所用物理常数的模块。

The functions in __atmos__ are designed to work with numpy arrays, though many of them can also be applied to scalar variables. This makes __atmos__ well suited for processing gridded numerical model output, as well as observational data.
__atmos__ 中的函数被设计为与 numpy 数组配合使用，虽然其中许多也可以作用于标量变量。这使得 __atmos__ 非常适合处理格点化的数值模式输出以及观测数据。


## Advantages of atmos
## atmos 的优势

__atmos__ offers several key advantages over existing libraries for calculating meteorological variables (such as [MetPy](https://unidata.github.io/MetPy/latest/index.html)).
__atmos__ 相比于现有用于计算气象变量的库（例如 [MetPy](https://unidata.github.io/MetPy/latest/index.html)）具有若干关键优势。

#### 1. Accuracy and physical consistency
#### 1. 精度与物理一致性

All of the thermodynamic equations in __atmos__ are analytical and derived from a common set of assumptions, known as the _Rankine-Kirchhoff_ approximations [(Romps, 2021)](https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/qj.4154). No empircal equations are used in __atmos__. The core assumptions of the Rankine-Kirchhoff approximations are: (i) ideal gases, (ii), constant specific heat capacities, and (iii) zero volume of condensates (liquid and ice). Together, these allow for the derivation of highly accurate analytical equations for moist thermodynamics.
在 __atmos__ 中，所有热力学方程都是解析形式，并从一套统一的假设推导而来，即著名的 _Rankine-Kirchhoff_ 近似（[Romps, 2021](https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/qj.4154)）。__atmos__ 不使用任何经验公式。Rankine-Kirchhoff 近似的核心假设包括：(i) 理想气体；(ii) 恒定的定压比热容；(iii) 凝结物（液态和冰态）的体积可忽略。综合这些假设，可以推导出对湿热力学高度精确的解析方程。

#### 2. Speed of calculations
#### 2. 计算速度

All of the functions in __atmos__ are vectorised to allow for fast processing of multidimensional arrays. To speed up pseudoadiabatic parcel calculations, __atmos__ uses high-order polynomial fits to (i) parcel temperature as a function of wet-bulb potential temperature (WBPT) and pressure and (ii) WBPT as a function of parcel temperature and pressure following [Moisseeva and Stull (2017)](https://acp.copernicus.org/articles/17/15037/2017/). This is also the basis for the Noniterative Evaluation of Wet-bulb Temperature (NEWT) method ([Rogers and Warren, 2023](https://doi.org/10.22541/essoar.170560423.39769387/v1)).
__atmos__ 中所有函数都进行了向量化处理，以便快速计算多维数组。为了加速伪绝热气块计算，__atmos__ 使用高阶多项式拟合：(i) 气块温度关于湿球位温（WBPT）和压强的函数，以及 (ii) WBPT 关于气块温度和压强的函数，方法遵循 [Moisseeva and Stull (2017)](https://acp.copernicus.org/articles/17/15037/2017/)。这也是非迭代湿球温度计算方法 NEWT（Noniterative Evaluation of Wet-bulb Temperature，[Rogers and Warren, 2023](https://doi.org/10.22541/essoar.170560423.39769387/v1)）的基础。

#### 3. Representation of saturation
#### 3. 饱和表示

Another novel feature in __atmos__ is the treatment of saturation, which can be represented with respect to liquid, ice, or a combination of the two (via the `phase` argument) following [Warren (2025)](https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.4866). When using the mixed-phase option (`phase="mixed"`), liquid water and ice are assumed to coexist between temperatures of 0°C and -20°C, with the ice fraction (denoted `omega` in the code) increasing nonlinearly from 0 to 1 across this range. This temperature range can be adjusted by altering the values of `T_liq` and/or `T_ice` in atmos/constant.py.
__atmos__ 的另一个创新点是对饱和的处理，可以选择相对于液态、冰态或二者混合（通过 `phase` 参数指定）的饱和程度，方法遵循 [Warren (2025)](https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.4866)。当使用混合相选项（`phase="mixed"`）时，假设在 0°C 到 -20°C 之间液态水和冰共存，且冰相体积分数（在代码中记为 `omega`）在这一温度范围内以非线性方式从 0 增加到 1。用户可以通过修改 `atmos/constant.py` 中的 `T_liq` 和/或 `T_ice` 的值来调整这一温度范围。

#### 4. Ability to handle different vertical grids
#### 4. 适应不同的垂直网格

The functions in __atmos__ that perform vertical integration, averaging, or interpolation are designed to be agnostic of the vertical grid; so long as arrays of pressure and/or height are provided, the calculations should work. However, when working with data on pressure levels, it is important to provide surface/screen-level variables (specified using the `_sfc` keyword arguments) in addition to the pressure-level arrays. This will ensure that values below the surface are excluded from the calculations.
__atmos__ 中用于进行垂直积分、平均或插值的函数在设计上与具体的垂直坐标无关；只要提供压强和/或高度数组即可完成计算。但是，当处理压强层数据时，除了压强层数组之外，还需要提供地面/屏幕高度的变量（通过 `_sfc` 关键字参数指定）。这样可以确保计算中排除地表以下的网格层。


## Examples
## 示例

Below are a few examples of using __atmos__ functions. Note that all variables are assumed to be in SI units; i.e., m for heights, Pa for pressures, K for temperatures, kg/kg for mass fractions (specific humidities) and mixing ratios, m/s for wind velocities. Relative humidities are expressed as fractions rather than percentages. For functions that perform vertical integration, averaging, or interpolation, it is assumed that the first array dimension corresponds to the vertical axis (unless the `vertical_axis` keyword is specified) and that pressure decreases and height increases along this axis. By default, saturation is calculated with respect to liquid water only.
下面给出几个使用 __atmos__ 函数的示例。注意所有物理量都假定为 SI 单位：高度使用 m，压强使用 Pa，温度使用 K，质量分数（比湿）和混合比使用 kg/kg，风速使用 m/s。相对湿度用 0–1 的小数表示而非百分数。对于执行垂直积分、平均或插值的函数，假定数组的第一维对应垂直轴（除非通过 `vertical_axis` 关键字显式指定），并且沿该轴压强单调减小、高度单调增大。默认情况下，饱和是相对于液态水计算的。

### Basic thermodynamic variables
### 基本热力学变量

Calculating saturation vapour pressure with respect to liquid water `esl`, ice `esi`, and mixed-phase condensate `esx` from temperature `T`:
根据温度 `T` 计算相对于液态水 `esl`、冰 `esi` 以及混合相凝结物 `esx` 的饱和水汽压：
```python
esl = atmos.thermo.saturation_vapour_pressure(T, phase="liquid")
esi = atmos.thermo.saturation_vapour_pressure(T, phase="ice")
omega = atmos.thermo.ice_fraction(T)  # ice fraction assuming saturation at temperature T
esx = atmos.thermo.saturation_vapour_pressure(T, phase="mixed", omega=omega)
```

Calculating "pseudo" (aka "adiabatic") wet-bulb temperature `Twp` and "isobaric" (aka "thermodynamic") wet-bulb temperature `Twi` from pressure `p`, temperature `T`, and specific humidity `q`:
根据压强 `p`、温度 `T` 和比湿 `q` 计算“伪”（或称“绝热”）湿球温度 `Twp` 以及“等压”（或称“热力学”）湿球温度 `Twi`：
```python
Twp = atmos.thermo.pseudo_wet_bulb_temperature(p, T, q)
Twi = atmos.thermo.isobaric_wet_bulb_temperature(p, T, q)
```

Calculating potential temperature `th`, virtual potential temperature `thv`, and equivalent potential temperature `theq` from pressure `p`, temperature `T`, specific humidity `q`, and total water mass fraction `qt`:
根据压强 `p`、温度 `T`、比湿 `q` 和总水质量分数 `qt` 计算位温 `th`、虚位温 `thv` 和相当位温 `theq`：
```python
th = atmos.thermo.potential_temperature(p, T, q, qt=qt)
thv = atmos.thermo.virtual_potential_temperature(p, T, q, qt=qt)
theq = atmos.thermo.equivalent_potential_temperature(p, T, q, qt=qt)
```

Converting from relative humidity with respect to ice `RHi` to vapour pressure `e`, mixing ratio `r`, and dewpoint temperature `Td` given pressure `p` and temperature `T`:
在给定压强 `p` 和温度 `T` 的条件下，从相对于冰的相对湿度 `RHi` 转换到水汽压 `e`、混合比 `r` 以及露点温度 `Td`：
```python
# Compute vapour pressure
e = atmos.moisture.vapour_pressure_from_relative_humidity(T, RHi, phase='ice')

# Compute mixing ratio
r = atmos.moisture.mixing_ratio_from_vapour pressure(p, e)

# Compute relative humidity with respect to liquid water
RHl = atmos.moisture.convert_relative_humidity(T, RHi, 'ice', 'liquid')

# Compute dewpoint temperature
Td = atmos.moisture.dewpoint_temperature_from_relative_humidity(T, RHl)
```

### Convective parameters
### 对流参数

Calculating surface-based (SB), mixed-layer (ML), and most-unstable (MU) CAPE and CIN and the associated lifting condensation level (LCL), level of free convection (LFC), level of maximum buoyancy (LMB), and equilibrium level (EL) given arrays of pressure `p`, temperature `T` and specific humidity `q`:
给定压强 `p`、温度 `T` 和比湿 `q` 的数组，计算地面型（SB）、混合层（ML）、最不稳定（MU）气块的 CAPE 和 CIN 以及对应的抬升凝结高度（LCL）、自由对流高度（LFC）、最大浮力高度（LMB）和平衡高度（EL）：
```python
SBCAPE, SBCIN, SBLCLp, SBLFCp, SBLMBp, SBELp = atmos.parcel.surface_based_parcel(p, T, q)
MLCAPE, MLCIN, MLLCLp, MLLFCp, MLLMBp, MLELp = atmos.parcel.mixed_layer_parcel(p, T, q)
MUCAPE, MUCIN, MULPLp, MULCLp, MULFCp, MULMBp, MUELp = atmos.parcel.most_unstable_parcel(p, T, q)
```
Note that the MU parcel function also outputs the lifted parcel level (LPL), which is the starting level of the parcel ascent (for the SB and ML parcels, this is the lowest level). The levels output by these function are all pressures. Given a corresponding array of heights `z`, levels can be converted to heights using the _utils_ function `height_of_pressure_level`. For example, the height of the MLLCL can be calculated as:
需要注意的是，MU 气块函数还会输出抬升气块层（LPL），即气块抬升的起始高度（对于 SB 和 ML 气块，这一高度为最低层）。这些函数输出的层都是以压强形式给出的。若提供相应的高度数组 `z`，可以使用 _utils_ 模块中的函数 `height_of_pressure_level` 将压强层转换为高度。例如，MLLCL 的高度可通过以下方式计算：
```python
MLLCLz = atmos.utils.height_of_pressure_level(p, z, MLLCLp)
```

Calculating 0-6 km bulk wind difference (BWD06) given arrays of height `z`, zonal wind `u`, and meridional wind `v`:
计算 0–6 km 的整层风差（BWD06），给定高度 `z`、纬向风 `u` 和经向风 `v` 的数组：
```python
# Compute BWD components
BWD06u, BWD06v = atmos.kinematic.bulk_wind_difference(z, u, v, 0.0, 6000.0)

# Compute BWD magnitude
BWD06 = np.hypot(BWD06u, BWD06v)
```

Calculating effective storm-relative helicity (ESRH):
计算有效风暴相对螺旋度（ESRH）：
```python
# Use the MU parcel function with the "max_cape" option to get the effective inflow
# layer base (EIB) and top (EIT)
*_, EIBp, EITp = atmos.parcel.most_unstable_parcel(p, T, q, mu_parcel="max_cape")

# Convert from pressure to height
EIBz = atmos.utils.height_of_pressure_level(p, z, EIBp)
EITz = atmos.utils.height_of_pressure_level(p, z, EITp)

# Compute Bunkers left and right storm motion vectors:
u_bl, v_bl, u_br, v_br = atmos.kinematic.bunkers_storm_motion(z, u, v)

# Compute ESRH for Bunkers left storm motion vector:
ESRH_bl = atmos.kinematic.storm_relative_helicity(z, u, v, u_bl, v_bl, EIBz, EITz)

# Compute ESRH for Bunkers right storm motion vector:
ESRH_br = atmos.kinematic.storm_relative_helicity(z, u, v, u_br, v_br, EIBz, EITz)
```


## Developer notes
## 开发者说明

The development of __atmos__ has been something of a side project for me and, as yet, I have not had time to create unit tests in order to rigorously test the code. As such it is possible that a few bugs are present. If you identify one please raise an issue and I will aim to fix it ASAP. That said, users should find that the code is well commented and easy to read. The choice of variable names and the formatting of equations matches more or less exactly the notation in [Warren (2025)](https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.4866), which should make it easy to understand the origins of each function.
__atmos__ 的开发更多是我的一个业余项目，目前还没有时间为代码编写单元测试来进行严格检验。因此，代码中有可能仍然存在一些 bug。如果你发现了问题，请提交 issue，我会尽快修复。尽管如此，用户应该会发现代码注释充分、易于阅读。变量命名和方程的书写格式基本与 [Warren (2025)](https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.4866) 中的记号一致，这有助于理解每个函数的来源。

If you have any suggestions for new features you would like to see added to __atmos__, please don't hesitate to get in touch.
如果你对 __atmos__ 有任何希望新增的功能或改进建议，欢迎随时联系我。

Rob Warren (13-01-2026)
Rob Warren（2026-01-13）
