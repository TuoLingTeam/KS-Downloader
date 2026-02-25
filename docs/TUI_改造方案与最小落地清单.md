# KS-Downloader Textual 多屏 UI 改造方案与最小落地清单

## 目标

将 `KS-Downloader` 的默认可执行交互界面从当前终端菜单模式升级为 `Textual` 多屏 UI（对齐 `XHS-Downloader` 的交互形态），并保持以下约束：

1. 默认 `python main.py` 启动 Textual TUI。
2. `python main.py api ...` 保持现有 API 行为不变。
3. 下载/解析/存储核心业务逻辑尽量复用现有 `source/app/app.py` 中 `KS` 类。
4. PyInstaller 构建产物可正常运行新 TUI。

## 按文件拆分的改造方案

### 1. 新增 TUI 目录与页面文件

1. `source/TUI/__init__.py`
   - 导出 `KSDownloader`。
2. `source/TUI/app.py`
   - Textual 主应用类；
   - 注册并管理页面：`index`、`setting`、`loading`、`update`、`about`、`disclaimer`。
3. `source/TUI/index.py`
   - 首页：输入链接、下载按钮、日志输出区（`RichLog`）、快捷键（`Q/U/S/A`）。
4. `source/TUI/setting.py`
   - 设置页（MVP 仅保留必要配置项）：语言切换、下载记录开关、读取 Cookie。
5. `source/TUI/loading.py`
   - 通用处理中模态（`LoadingIndicator`）。
6. `source/TUI/update.py`
   - 检查更新模态，复用 `Version` 逻辑。
7. `source/TUI/about.py`
   - 项目说明页、仓库链接、版本信息。
8. `source/TUI/disclaimer.py`
   - 首次启动免责声明确认页，确认后写入数据库配置。
9. `source/TUI/KS-Downloader.tcss`
   - 统一样式、布局、按钮状态色、模态尺寸。

### 2. 业务层最小改造

1. `source/app/app.py`
   - 保留现有终端菜单逻辑；
   - 增加给 TUI 调用的公开方法（避免直接调用私有方法），例如：
     - `bootstrap()`：初始化配置与选项；
     - `process_links(text)`：处理输入链接并执行下载；
     - `toggle_record()`；
     - `set_language(language)` + 持久化；
     - `check_update()`；
     - `accept_disclaimer()`。
2. `source/tools/console.py`
   - 给 `ColorConsole` 增加输出 sink 机制，使日志可写入 Textual `RichLog`；
   - 保留原 stdout 行为，保证 API 与旧逻辑不受影响。

### 3. 入口与导出调整

1. `source/__init__.py`
   - 新增 `KSDownloader` 导出。
2. `main.py`
   - 无参数时启动 Textual TUI；
   - `api` 子命令保持原样；
   - 可选新增 `legacy` 模式用于回退终端菜单（非必须）。

### 4. 依赖与构建调整

1. `pyproject.toml`
   - 新增 `textual` 依赖（必要）；
   - 可选新增 `pyperclip`（若首页需要“读取剪贴板”按钮）。
2. `requirements.txt`
   - 重新锁定，补齐上面新增依赖。
3. `.github/workflows/Manually_build_executable_programs.yml`
4. `.github/workflows/Release_build_executable_program.yml`
   - PyInstaller 参数补充 Textual 打包所需资源（必要时 `--collect-all textual`）。

## 最小可落地改动清单（MVP）

按顺序执行：

1. 新增 `source/TUI` 的核心文件：`app/index/setting/loading/update/disclaimer/__init__/tcss`。
2. 在 `source/tools/console.py` 增加日志 sink，打通 TUI 日志展示。
3. 在 `source/app/app.py` 增加 TUI 公开服务方法，不改下载核心流程。
4. 修改 `main.py` 默认入口为 TUI，保留 `api`。
5. 修改 `source/__init__.py` 导出 TUI App。
6. 更新 `pyproject.toml` 与 `requirements.txt`（加入 `textual`）。
7. 更新两个构建 workflow 的 PyInstaller 参数。
8. 本地验收并修复：
   - `python main.py`
   - `python main.py api --host 0.0.0.0 --port 5557`
   - PyInstaller 构建后启动 smoke test。

## 验收标准

1. 启动默认界面为 Textual 多屏 UI。
2. 可在首页输入快手链接并完成下载。
3. 日志实时显示在 TUI 页面中。
4. 设置页可切换语言并持久化。
5. 免责声明首次展示、确认后不再重复出现。
6. API 模式与现有路由行为保持兼容。
7. 构建出的可执行文件在 Windows/macOS 下可启动并进入 TUI。

## 第二阶段（非 MVP，可后续迭代）

1. 完整迁移 `config.yaml` 全字段到设置页表单。
2. 增加下载记录管理页（删除指定 ID、清空记录）。
3. 增加剪贴板监听模式（类似 XHS `monitor`）。
4. 补齐 Textual UI 单测/集成测试矩阵与快照测试。
