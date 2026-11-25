# HALO / Butterfly 设计语言

## 原则
保留原 Butterfly 的交替封面、侧栏、分类归档、阅读页与 15 层动态横幅。以阅读为中心，低饱和背景、轻边线、少量阴影、单一强调色；不通过增加装饰弥补信息层级。当前版本图片保存在仓库、远程可变 WOFF2 字体、GitHub Pages 唯一正式发布平台。旧标签和文章原文不改动。

## 设计令牌
唯一来源：butterfly-optimized/styles/tokens.css。组件不得重复定义全局颜色变量，新增颜色应首先选择语义令牌。

| 角色 | 浅色 | 深色 |
| --- | --- | --- |
| 画布 | #f4f6fa | #10141b |
| 表面 | #ffffff | #191f29 |
| 抬升表面 | #fafbfe | #202733 |
| 正文 | #222d3d | #e5eaf2 |
| 辅助文字 | #607084 | #a6b3c5 |
| 强调 | #4269ae | #97baf0 |
| 链接 | #315da3 | #9cc6fa |
| Hover | #edf2fa | #283346 |
| 边界 | #e1e6ee | #303946 |

字体：Inter + Noto Sans SC 400–700 可变 WOFF2；代码使用系统等宽字体。正文 16px/1.9，手机 15px/1.85；标题首页 19–26px，阅读主标题 26–42px。控件圆角 8px、标签 6px、卡片 14px；移动卡片 12px。保留原始图标库。

## 统一交互规则
- Default：表面/透明背景和稳定边界；Hover：低饱和背景、链接颜色，只保留一种主要反馈，不改变几何。
- Selected：强调色填充和强调色前景，目录使用弱背景和内侧标记以避免过于突出。不能把 hover 和 current 当作同一状态。
- Focus-visible：可操作元素保留 2px 焦点轮廓；结构容器的 tabindex=-1 仅用于跳到正文，禁止出现包围整个页面的轮廓。
- 动效：快速 160ms、常规 260ms、封面 420ms、搜索入场 220ms。禁止新增 transition: all；圆角、边距、内边距默认固定。保留 reduced-motion，触控无需 hover。
- 首页顶部透明，品牌与菜单按内容宽度对齐；滚动导航重新出现时使用当前主题实体表面。有头图页面的整条导航同样透明，仅品牌、菜单及复杂插画标题使用随主题变化的局部半透明表面，浅底深字、深底浅字，保留原图与视差。
- 评论采用唯一 Giscus 编辑器，关闭独立 reactions 区；无旧 Issues UI 或查询。保留错误提示和重试，不删除历史讨论。

## 样式职责与构建
styles/order.json 是显式构建顺序：tokens、base、banner、navigation、cards、reading、toc、search、controls、comments、motion。prepare.py 验证清单与模块一致，合并为原 halo-refine.css，现有 clean-css 压缩；不增加独立 CSS 请求。原 Butterfly 和 source/css/butterfly.css 为历史兼容层，不直接大规模重写。改动放入归属模块；重复规则先合并，确有旧主题覆盖冲突才使用高特异性或必要的 important。样式改动必须检查浅深主题、桌面与移动宽度、hover 中间帧和键盘焦点。

## 验收入口
tests/style-states.cjs：透明导航、伪元素、归档圆角/内边距、分页配色、容器焦点、键盘焦点、头图遮罩。tests/design.cjs：双主题、字体、移动布局、封面 hover、reduced-motion、Giscus。tests/giscus.cjs：真实组件、模拟异常与主题同步。测试不发实际评论。

## V2.8 导航与内页
借鉴 DeepSeek 官网轻量文字、品牌/操作分区和透明背景，不复制其品牌素材。导航保持原七项功能，桌面主菜单文字为主，搜索及移动菜单保留识别图标。下拉垂直排列，鼠标与键盘均可操作，Escape 收起；当前页使用 aria-current。标题对比采用主题语义表面，而非实时读取每个像素亮度，防止动态横幅导致文字反复闪变。滚动吸顶与正文使用一致的明暗色彩。内页集合与阅读 Tab 样式由 styles/pages.css 维护。
