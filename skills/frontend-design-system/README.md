# Frontend Design System

一个用于网页、数据报告和工作台的主题优先设计 Skill。它先识别产品语境和现有视觉语言，再调整颜色、排版、间距、组件与响应式结构，避免把不同产品套成同一种模板。

## 安装

```bash
git clone https://github.com/wangge-ai/wangge-skills.git
cp -R wangge-skills/skills/frontend-design-system ~/.agents/skills/frontend-design-system
```

Windows PowerShell 可使用：

```powershell
Copy-Item -Recurse wangge-skills/skills/frontend-design-system "$HOME/.agents/skills/frontend-design-system"
```

## 自带脚本

`scripts/create_visual_comparator.py` 使用 Python 标准库生成本地前后对比 HTML，只读取清单或命令参数中的图片路径，并写入显式指定的输出文件。它不会联网、删除文件或启动浏览器。

```bash
python scripts/create_visual_comparator.py --output comparison.html --pair "首页|before.png|after.png"
```

## 开源协议

[MIT](LICENSE)
