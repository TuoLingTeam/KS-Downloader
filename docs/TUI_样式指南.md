# KS-Downloader TUI 样式指南

## 快速参考

### 按钮变体

```python
# 主要操作按钮（强调）
Button("下载", variant="primary")

# 警告操作按钮
Button("删除", variant="warning")

# 默认按钮（次要操作）
Button("返回", variant="default")
```

### 标签类型

```python
# 参数标签（标题、强调）
Label("设置项", classes="params")

# 提示标签（带背景和边框）
Label("操作说明", classes="prompt")

# 状态标签（带左侧强调边框）
Label("当前状态：启用", classes="status")
```

### 容器使用

```python
# 设置区块容器
Container(
    Label("区块标题", classes="params"),
    Select(...),
    Button(...),
    classes="settings-section",
)

# 水平按钮组
HorizontalScroll(
    Button("按钮1"),
    Button("按钮2"),
    Button("按钮3"),
    classes="horizontal-layout",
)

# 关于页面容器
ScrollableContainer(
    Label(...),
    Link(...),
    Button(...),
    classes="about-container",
)
```

## 颜色系统

### Textual 内置颜色变量

| 变量 | 用途 | 示例 |
|------|------|------|
| `$primary` | 主题色 | 按钮、边框、标题 |
| `$accent` | 强调色 | 焦点状态、重要信息 |
| `$warning` | 警告色 | 免责声明、危险操作 |
| `$panel` | 面板背景 | 模态窗口、卡片 |
| `$surface` | 表面背景 | 日志区域、输入框 |
| `$text` | 文本颜色 | 主要文本内容 |

### 颜色修饰符

```css
/* 透明度 */
background: $primary 20%;  /* 20% 不透明度 */

/* 亮度调整 */
background: $primary-lighten-1;  /* 变亮一级 */
background: $primary-lighten-2;  /* 变亮两级 */
background: $primary-darken-1;   /* 变暗一级 */
```

## 边框样式

### 边框类型

| 类型 | 效果 | 用途 |
|------|------|------|
| `tall` | 竖线边框 | 按钮、输入框 |
| `round` | 圆角边框 | 提示框、设置区块 |
| `double` | 双线边框 | 模态窗口、日志区域 |
| `solid` | 实线边框 | 分隔线 |
| `thick` | 粗边框 | 强调边框 |

### 边框位置

```css
border: tall $primary;           /* 全边框 */
border-left: thick $accent;      /* 左边框 */
border-bottom: solid $warning;   /* 下边框 */
```

## 间距系统

### 标准间距单位

| 单位 | 像素 | 用途 |
|------|------|------|
| 0 | 0px | 无间距 |
| 1 | 1 单位 | 小间距（元素间） |
| 2 | 2 单位 | 中间距（区块间） |

### 间距属性

```css
margin: 1 0;        /* 上下 1，左右 0 */
margin: 1 2;        /* 上下 1，左右 2 */
padding: 1;         /* 四周 1 */
padding: 1 2;       /* 上下 1，左右 2 */
```

## 布局系统

### Grid 布局

```css
/* 单列多行 */
grid-size: 1 3;           /* 1 列 3 行 */
grid-rows: auto 1fr auto; /* 自动 弹性 自动 */
grid-gutter: 1;           /* 间隙 1 */

/* 多列单行 */
grid-size: 2 1;           /* 2 列 1 行 */
```

### 尺寸单位

```css
width: 1fr;        /* 弹性宽度 */
width: 50;         /* 固定 50 单位 */
width: 90vw;       /* 视口宽度 90% */
height: 80vh;      /* 视口高度 80% */
height: auto;      /* 自动高度 */
max-height: 40%;   /* 最大高度 40% */
```

## 状态样式

### 伪类选择器

```css
Button:hover {
    background: $primary 20%;
    border: tall $accent;
}

Button:focus {
    text-style: bold;
}

Link:hover {
    background: $accent 10%;
}
```

## 文本样式

### 文本对齐

```css
text-align: center;              /* 水平居中 */
content-align-horizontal: center; /* 内容水平居中 */
content-align-vertical: middle;   /* 内容垂直居中 */
```

### 文本样式

```css
text-style: bold;           /* 粗体 */
text-style: bold underline; /* 粗体下划线 */
line-height: 1.5;          /* 行高 */
```

## 特效

### 阴影

```css
box-shadow: 0 0 8 2 rgba(0, 0, 0, 0.5);
/* 水平偏移 垂直偏移 模糊半径 扩散半径 颜色 */
```

### 滚动条

```css
scrollbar-gutter: stable;  /* 稳定的滚动条槽 */
```

## 最佳实践

### 1. 视觉层次

```python
# ✅ 好的做法：使用变体区分重要性
Button("主要操作", variant="primary")
Button("次要操作", variant="default")

# ❌ 避免：所有按钮都一样
Button("主要操作")
Button("次要操作")
```

### 2. 内容分组

```python
# ✅ 好的做法：使用容器分组相关内容
Container(
    Label("标题", classes="params"),
    Input(...),
    Button(...),
    classes="settings-section",
)

# ❌ 避免：所有元素平铺
Label("标题", classes="params")
Input(...)
Button(...)
```

### 3. 一致性

```python
# ✅ 好的做法：统一使用相同的类名
Label("状态1", classes="status")
Label("状态2", classes="status")

# ❌ 避免：混用不同的样式
Label("状态1", classes="status")
Label("状态2", classes="prompt")
```

### 4. 响应式设计

```css
/* ✅ 好的做法：使用相对单位 */
width: 90vw;
height: 1fr;

/* ❌ 避免：使用固定像素 */
width: 800px;
height: 600px;
```

## 常见模式

### 模态窗口

```python
class MyModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("标题", classes="params"),
            ScrollableContainer(
                # 内容
            ),
            Grid(
                Button("确认", variant="primary"),
                Button("取消"),
                classes="modal-buttons",
            ),
            id="my-modal",
        )
```

```css
#my-modal {
    grid-size: 1 3;
    grid-rows: auto 1fr auto;
    width: 70vw;
    height: 60vh;
    border: double $primary;
    background: $panel;
    padding: 1;
}

.modal-buttons {
    grid-size: 2 1;
    grid-gutter: 1;
    height: auto;
    padding: 1;
}
```

### 设置区块

```python
Container(
    Label("设置项名称", classes="params"),
    Select(...),
    Button("保存", variant="primary"),
    classes="settings-section",
)
```

### 信息展示

```python
Label(
    Text("重要提示信息", style=PROMPT),
    classes="prompt",
)

Label(
    Text(f"当前状态：{status}", style=INFO),
    classes="status",
)
```

## 调试技巧

### 1. 使用 Textual 开发工具

```bash
# 启动应用时开启开发者控制台
textual console

# 在另一个终端运行应用
python main.py
```

### 2. 临时边框调试

```css
/* 临时添加边框查看布局 */
Container {
    border: solid red;
}
```

### 3. 检查元素层次

```python
# 在 on_mount 中打印元素树
def on_mount(self):
    self.log(self.tree)
```

## 主题定制

### 修改主题

```python
class KSDownloader(App):
    async def on_mount(self) -> None:
        # 可选主题：nord, dracula, monokai, gruvbox 等
        self.theme = "nord"
```

### 自定义颜色

```css
/* 在 .tcss 文件中覆盖颜色变量 */
App {
    --primary: #5E81AC;
    --accent: #88C0D0;
    --warning: #BF616A;
}
```

## 总结

这个样式系统提供了：
- 🎨 一致的视觉语言
- 🔧 灵活的组件系统
- 📱 响应式布局支持
- ♿ 良好的可访问性
- 🚀 易于维护和扩展

遵循这些指南可以确保 TUI 界面保持专业、一致和用户友好。
