# HexoPage 历史版本维护

- v1.0.0 固定于 70a1ac9aa9e438712a7ab17300e182027e184946，禁止移动历史标签。
- Pages 由 `.github/workflows/pages.yml` 和 `.github/pages/pages-versions.json` 管理；最新版本位于根路径，旧版本位于 `versions/<tag>/`。
- 构建使用独立临时源码目录，仅在构建副本覆盖域名、子路径及兼容性配置。不改变原主题和文章。
- 新历史版本必须先创建不可变标签，将标签及完整提交 SHA 纳入清单。保持版本目录及旧标签。
- 中文 Git commit。发布前检查构建产物、实际 Pages 状态及首页、文章、归档、搜索、资源路径。外部历史图床和 CDN 可用性不能保证。
