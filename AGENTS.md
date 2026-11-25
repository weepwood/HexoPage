# HexoPage 历史版本维护

- v1.0.0 固定于 70a1ac9aa9e438712a7ab17300e182027e184946，禁止移动历史标签。
- Pages 由 `.github/workflows/pages.yml` 和 `.github/pages/pages-versions.json` 管理；最新版本位于根路径，旧版本位于 `versions/<tag>/`。
- 构建使用独立临时源码目录，仅在构建副本覆盖域名、子路径及兼容性配置。不改变原主题和文章。
- 新历史版本必须先创建不可变标签，将标签及完整提交 SHA 纳入清单。保持版本目录及旧标签。
- 中文 Git commit。发布前检查构建产物、实际 Pages 状态及首页、文章、归档、搜索、资源路径。外部历史图床和 CDN 可用性不能保证。

- 原冬季/秋季 OSS 横幅已失效；部署副本使用同一历史主题的春季横幅，并保护空对象访问、停用历史访问统计。原标签内容不变。

## V2 现代博客
- 现代主题及锁定依赖位于 `modern/`；不要在历史根目录安装新版依赖。`source/` 是共享内容，构建临时副本补齐日期，不改原文。
- 最新标签由版本清单选择。旧版本永远保留独立子路径。新增版本时先提交主题与内容，创建不可变标签，再将 SHA 写入清单；不要自引用当前提交。
- 默认索引仅包含元数据；首页不发起第三方资源请求。遵循构建体积预算，避免引入客户端框架或全站动效。
- 详细设计、决策、测试与限制见 `docs/V2-升级分析报告.md`。

## V2.1 视觉方向（用户确认）
- 主站必须保持原 Butterfly 的导航、交替封面卡片、作者侧栏及原文章信息架构；优化性能、排版和交互细节，不擅自换主题。
- `butterfly-optimized/` 存放独立兼容优化层，在临时构建副本中启用；保留 `modern/` 对应 V2.0.0 预览。历史标签禁止移动。详见 `docs/V2.1-Butterfly优化报告.md`。

## V2.2 资源与动效规范
- 主站保留 Butterfly 视觉体系，远程中文字体使用可变 WOFF2 + Unicode 分片 + swap 与系统字体后备。
- 所有主站图片进入本仓库 `source/images/archive/`，禁止使用 OSS 或独立图库仓库作为运行时依赖。来源及缺失记录保存在 `butterfly-optimized/assets/images.json`，构建不联网下载图片，新增外链必须迁移或明确本地占位。
- 动态横幅保留原素材及深度视差，鼠标离开回中，离屏和隐藏时停止，移动端及 reduced-motion 降级。详细见 `docs/V2.2-字体图片与动效优化.md`。

## V2.3 目录交互规范
- 保留 Butterfly 原目录布局；目录跳转独立实现可中断缓动、统一标题偏移、当前目标锁定、实际边界跟随、分支独立展开和 reduced-motion。
- 长文章优先验证中文锚点、上下跳转、连续切换、浏览器前进后退及移动目录；不得恢复固定 150px 跳动策略。详见 docs/V2.3-目录交互优化.md。

## V2.4 集中完善与发布
- 正式部署仅 GitHub Pages；根目录 vercel.json 禁止 Git 自动部署，控制台绑定另行核对。保留历史标签及 Release。
- 主线计划见 docs/ROADMAP.md，实际验证见 docs/V2.4-集中完善报告.md。搜索优先 Pagefind Extended（中文），旧全文 JSON 仅作降级；不在首页加载索引。
- 不破坏 Butterfly 布局、目录、动态横幅、远程 WOFF2 和本仓库图片策略。固定历史快照缓存按 SHA/构建器/URL 隔离，验证标签，不为小修单独发版。

## V2.5 质量规范
- 保留 Butterfly 视觉与历史标签。MathJax 固定本地版本，静态 vendor 不进入模板渲染。
- Hexo 8 候选独立维护，结构差异未收口不得切换生产。
- 性能数据须标明版本、网络、采样次数和模拟/真机；保留可复现测试及原始报告，不将自动化无障碍扫描当作全站认证。

## V2.5.1 评论系统
- 新版本使用公开 GitHub Issues 讨论，按不含版本前缀的页面路径生成稳定键，站内只读，写入走 GitHub 登录页面，不向前端放置访问令牌。
- 原 Valine LeanCloud 应用已归档，旧评论不宣称已迁移。历史版本保持原始系统。测试不得自动发布垃圾评论；保留失败降级及重试。详见 docs/V2.5.1-评论区修复.md。

## V2.6 视觉系统与评论
- 视觉规则集中维护 butterfly-optimized/design.css，保留 Butterfly 原始结构；Inter/Noto Sans SC 远程可变字体、低饱和双主题、统一交互节奏与 reduced-motion。
- Giscus 为主要站内评论组件，Discussions 已启用且官方客户端可正常显示，稳定 specific/strict 路径映射；保留旧 Issues 折叠入口与历史 Valine，不在前端保存访问令牌。未实际发帖不得宣称写入验收。
- 验收使用 tests/design.cjs、tests/giscus.cjs、tests/comments.cjs，详见 docs/V2.6-视觉与站内评论.md。

## V2.7 样式架构
- 设计语言以根目录 DESIGN.md 为准。新样式集中于 butterfly-optimized/styles/，tokens.css 为唯一全局语义令牌来源，order.json 确定合并次序；禁止复建旧 refine.css/design.css。
- 默认/hover/选中/键盘焦点分离，hover 不改变圆角及间距，不新增 transition: all；首页透明导航，有图头部局部对比遮罩。
- Giscus 只保留站内编辑器，关闭独立表情区，禁止恢复旧 Issues 备用 UI；历史数据不删除。
- 样式回归优先 tests/style-states.cjs、tests/design.cjs、tests/giscus.cjs。

## V2.8 导航规范
- 顶部导航参考 DeepSeek 的透明、轻量文字与分区结构，禁止恢复整条黑色遮罩。复杂图片使用局部主题对比表面，保留横幅与视差。
- navigation.css/navigation.js 管理导航，pages.css 管理集合内页与阅读 Tab；遵循 DESIGN.md 与 styles/order.json。验收使用 tests/navigation.cjs 和 tests/style-states.cjs。
