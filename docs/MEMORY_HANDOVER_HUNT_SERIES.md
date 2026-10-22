# 《你要么猎杀，要么被猎杀》商业短视频大片全流程记忆交接文档 (Master Memory Handover)

> [!IMPORTANT]
> **新会话使用指南**：
> 在 Antigravity 点击「+」新建任意窗口，只需发送首条指令：  
> `请阅读 /Users/mlx/Desktop/IP/code-video-works/MEMORY_HANDOVER_HUNT_SERIES.md 继承全部记忆、规范与工程管线，并根据最新状态继续推进。`  
> 即可无缝继承 100% 的全部工作流、音色凭证、剪映规范与美学标准！

---

## 一、 IP 主理人人设与剧作核心原则

1. **IP 主理人**：**骁清Finn**
   - **人设风格**：冷峻、从容、刺骨、去鸡汤、降维审视、具有顶级商业认知穿透力。杜绝打鸡血和空洞说教，像顶尖外科医生一样冷酷剖开人性与商业规则。
   - **固定收尾落款**：每集片尾必须锁定黄金落款——「**我是骁清Finn，想清楚了，评论区聊聊。**」
2. **原著依托**：树林 著《你要么猎杀，要么被猎杀》（EPUB 全本已吸收提炼于 `/Users/mlx/Desktop/IP/你要么猎杀，要么被猎杀.epub`）。
3. **剧作结构（5~6幕电影级叙事）**：
   - Hook 刺痛破防 ➔ 现实打脸 ➔ 商业底层模型/算力推演 ➔ 升维视角 ➔ 极简执行破局 ➔ 品牌收束。

---

## 二、 视频制作核心规范与铁律 (Production Constraints)

### 1. 视频母版纯净度规范 (Clean Feed Rule)
- **代码渲染视频画面不得压制/烧录硬字幕 (No Hardcoded Subtitles)**：
  - 在 HTML / Canvas / HyperFrames 代码渲染成片时，画面主体必须保持纯净无字。
  - **画面底端 20%（竖屏 Y > 1536 区域）严格保持纯净留白**（深岩灰微光渐变），严禁出现主要视觉主体，避免字幕遮挡底层场景与微动态。
- **剪映端灵活编辑**：
  - 字幕统一生成并在剪映工程的**独立文本轨道**中挂载，应用香槟金高亮（`#ffd76a`）+ 黑色描边双色样式。

### 2. 视频规格参数
- **分辨率**：`1080 × 1920`（竖屏 9:16 移动端全屏画质）
- **帧率**：`30 FPS`（纯确定性渲染：$t$ 为时间变量的封闭函数）
- **引擎**：单文件 HTML5 Canvas / WebGL 确定性渲染（零外部未经授权图片，全部纯数学绘制）
- **美学体系（告别死黑油腻）**：
  - 参考 `https://github.com/Vincentwei1021/mg-styles-15.git`（15种商业MG风格）
  - **弥散玻璃拟态 (Aurora & Glassmorphism)**：高斯模糊彩色大光斑漂移 + 3%微弱噪点防banding + 悬浮磨砂玻璃卡片（`backdrop blur` + 1px 白色内发光高光边框 + 真实色散）；
  - **香槟金一笔画 (Atelier Linea)**：一根香槟冷金线贯穿全篇连续变形；
  - **包豪斯度量衡沙盘**：0.5px 网格、刻度十字与空间平移运镜（Camera Pan & Zoom）。

---

## 三、 配音生成引擎：Fish Audio 专属克隆技术规范

所有的口播音频均由 Fish Audio 专属声音克隆 API 驱动，参数与配置锁定如下：

1. **API 核心凭证与参数**
   - **API 端点**：`https://api.fish.audio/v1/tts`
   - **API Key**：`sk-fish-4GPT3tSw1c0YN-rxK0jZiHDbpcAHIAAZlndZSbPyEB4`
   - **专属 Voice ID**：`db0639bd49fd407e9845829ee044cfa4`（骁清Finn 原声克隆）
   - **锁定模型**：`s2.1-pro-free`
   - **格式与采样率**：MP3 生成（44.1kHz），终混母带统一重采样至 48kHz WAV。
   - **超参数**：`temperature: 0.6`, `top_p: 0.72`, `repetition_penalty: 1.2`
2. **母带标准化与终混**
   - 响度标准化：`loudnorm=I=-16:TP=-1.5:LRA=11`
   - BGM 动态混音：人声保持 1.0，BGM 压至 `volume=0.15`，片头 1s 淡入，片尾 4s 淡出。
   - 混音参考音轨：`/Users/mlx/Desktop/IP/code-video-works/22-hunt-v1/audio_pipeline/bgm_score_v4.wav`

---

## 四、 剪映 Pro 原生工程自包含导出规范 (JianYing Pro Workflow)

1. **工程输出目录**：
   `~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/<工程名>`
2. **核心工具脚本**：
   位于 `/Users/mlx/.gemini/config/skills/jianying-draft-export/scripts/draft_builder.py`
3. **剪映缓存刷新与置顶铁律（避坑指南）**：
   - 剪映在后台运行时有内存缓存，直接写 `root_meta_info.json` 不会触发 UI 刷新。
   - **标准流程**：
     ```bash
     killall -9 VideoFusion VideoFusion-macOS VideoFusion-macOSTrayHelper 2>/dev/null
     # 更新 draft_content.json 与 draft_meta_info.json
     # 将当前工程以最新微秒时间戳 now_us 插入 root_meta_info.json 的 all_draft_store[0]（最左上角第0位）
     open -a "JianyingPro"
     ```

---

## 五、 系列剧集制作进度与历史状态

| 集数 | 章节原著名 | 时长 | 视觉隐喻与美学 | 当前状态 | 对应工程目录 |
|:---|:---|:---:|:---|:---:|:---|
| **EP.01** | 第一章《世界的真相：不是善恶，是猎人与猎物》 | 35.5s | 决策边界红金分割、算法提线木偶、旋转高维棋盘 | ✅ 100% 交付已入剪映 | `22-hunt-v1` |
| **EP.02** | 第二章《自私是清醒，不是罪》 | 35.5s | 粒子向心螺旋归零、开普勒金色同心圆、价值导数铡刀、双势阱逃逸 | ✅ 100% 交付已入剪映 | `23-hunt-ep02` |
| **EP.03** | 第三章《完美主义是慢性自杀》 | 69.0s | 数字时钟破防、审判天平倾斜、24h能量圈翻倍、连续函数积分、瑞士陀飞轮齿轮 | ✅ 100% 交付已入剪映 | `24-hunt-ep03` |
| **EP.04** | 第四章《弱者心智才是真正的贫穷》 | 116.0s (2分钟旗舰) | 弥散极光微光 + 磨砂玻璃卡片 + 香槟金一笔画贯穿 + 算法漏斗借口粒子 + 6区沙盘平移运镜 + 极简执行刀锋射线 | ✅ 100% 交付已入剪映 | `25-hunt-ep04` |
| **EP.05** | 第五章《造梦是这个时代最大的生意》 | 116.0s | 造梦气泡、流水线、投流杠杆、筛子、画圆碎裂 | ✅ 100% 交付已入剪映 | `26-hunt-ep05` |
| **EP.06** | 第六章《权力需要距离，不需要讨好》 | 116.0s | 社交重力场、洛希极限、杀鸡儆猴准星、单字「不」 | ✅ 100% 交付已入剪映 | `27-hunt-ep06` |
| **EP.07** | 第七章《神格：自己给自己加冕》 | 待定 | 自我神格化、王座几何、光芒内敛 | ⏳ 待启动 | 待规划 |
| **EP.08** | 第八章《恨是初始燃料，强大是终点》 | 待定 | 反应堆核裂变、初始推进力、星环轨道 | ⏳ 待启动 | 待规划 |

---

## 六、 本地关键工具与环境路径一览

- **FFmpeg 二进制路径**：  
  `/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1`
- **Chrome / Playwright 路径**：  
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`  
  Playwright 安装目录：`/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright`
- **15种 MG 动画参考库**：  
  `/Users/mlx/.gemini/antigravity/scratch/mg-styles-15/`
- **天秤 AI (Claude Opus 5.5 会话环境)**：  
  TaskSpace 35, `p1` 页面（已登录并持久化活跃）
