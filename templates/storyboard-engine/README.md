# 故事板视频工程母版

复制整个目录并改名后再开工。母版只包含工程骨架、通用代码和 Skill，不包含任何项目素材或成片内容。

## 开工顺序

1. 把视觉关键帧与运动关键帧放进 `.media/storyboard/`。
2. 填写 `STORYBOARD.md`、`RENDER_STRATEGY.md` 和唯一时间源 `timeline.json`，先给用户确认规划。
3. 每个共享主体分组从 `templates/group.html` 建一套母场景；镜头尽量只新增状态与时间参数。
4. 把成片会使用的素材按镜头放进 `assets/shot-NN/`；跨镜头复用素材放进 `assets/shared/`。
5. 按依赖图并行制作无依赖场景；在 `index.html` 挂载通过的分组合成，随后运行 `npm run dev`。

## 目录纪律

| 路径 | 只放什么 |
| --- | --- |
| `.media/storyboard/` | 视觉关键帧、运动关键帧等验收参考；不进入成片 |
| `.media/images/` | 临时导入或待处理图片；确认使用后移入 `assets/` |
| `assets/shot-NN/` | 指定镜头使用的图片、视频及纹理 |
| `assets/shared/` | 多镜头共用素材 |
| `assets/audio/` | 配音、音乐、音效 |
| `assets/fonts/` | 本地字体文件 |
| `compositions/` | 可渲染的分组合成 HTML；共享主体的连续镜头必须留在同一文件 |
| `compositions/components/` | 多个合成复用的代码组件 |
| `templates/` | 未使用的合成模板，禁止直接在这里制作正片 |
| `snapshots/` | 当前静态验收帧或单张接触表 |
| `.thumbnails/` | 预览工具生成的缩略图缓存 |
| `tmp/` | 可随时重建的中间产物；不得被成片直接引用 |
| `lib/` | 本地运行时、加载器和摄影机工具 |
| `skill/` | 故事板视频工作规范 |

不要把素材放在工程根目录，也不要让 `compositions/` 直接引用 `tmp/` 或 `.media/`。

## 常用命令

```bash
npm run dev
npm run check
npm run snapshot
```

默认只展示接触表或可拖动预览。不要生成审计报告、文件清单、重复渲染或逐帧回归；具体问题用相关帧和错误就地诊断。
