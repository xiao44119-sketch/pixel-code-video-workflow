# 《古希腊神话史诗重构》全剧 24 集总装工业化管线手册（Master Production Manual）

> **创作者 IP**：骁清Finn  
> **核心定位**：4 幕 24 集古希腊神话重构竖屏系列（每集 55.0 秒，30 FPS，1650 帧，1080×1920）  
> **主旨**：**“诸神是系统，凡人的唯一武器是清醒；清醒的尽头，是回家。”**  
> **总装管线分工**：
> - **L0 剧本**：前 9 轮定稿（每集 10 拍台词 + 时码 + 黄金关键词）
> - **L1 静帧垫片**：Nano Banana（每集 1~2 张 9:16 关键帧构图与质感锚点）
> - **L2 动态垫片**：Google Flow（图生视频，每集 1 条约 8 秒微动态物理运动素材）
> - **L3 抽帧序列**：ffmpeg 导出 PNG 序列（让垫片素材逐帧高精度确定性取用）
> - **L4 母版渲染**：Canvas / WebGL 确定性物理引擎（Clean Feed 无硬字幕纯净视频母版）
> - **L5 声音工程**：Azure TTS `zh-CN-YunxiNeural`（48kHz / 16bit WAV）+ 真人实录签名语
> - **L6 剪映 Pro**：视频轨、独立字幕轨（香槟金 `#ffd76a` 高光）、音频轨精准咬合交付

---

## 一、三条工业化落地总原则

1. **神话拍用 AI 垫片，现代映射拍一律用抽象粒子**：
   - 现代痛点场景（KPI 流程树、报表、外卖、热搜弹幕等）一律采用 Canvas/WebGL 抽象几何与粒子模拟，绝不使用写实现代 AI 生成图，彻底规避平台肖像、品牌与审核风险，保持冷峻的母版基调。
2. **神话人物一律做成“黑色大理石与冷金雕像”质感**：
   - 24 集所有人形统一为“风化黑色大理石雕像，肌理微渗冷金细纹”。既免除了跨集人脸一致性难题，又大幅降低写实人体的过审风险，更深度呼应第二幕的“雕像线”。
3. **垫片素材绝不直接作为成片裸露**：
   - 垫片在 Canvas 引擎中仅作为“背景底板”（压暗至 25%~45% 并调色至黑曜石色调）、“粒子目标采样图”或“空间遮罩”。最终画面均由物理引擎实时重构。

---

## 二、Bana / Google Flow 24 集垫片资产生成提示词库

### 1. 全局风格模板（Global Style Bible）
每条提示词均拼装以下风格后缀，保证 24 集调色与影调高度统一：

```text
【STYLE-EN】
Vertical 9:16 cinematic still, 35mm anamorphic look. Obsidian-black world, cold antique gold as the only accent color. Low-key chiaroscuro, one motivated rim light, thin volumetric haze, fine film grain. Human figures appear as weathered black-marble statues with faint gold veins; faces partly in shadow, no realistic skin. Restrained, monumental, documentary mood. Keep the lower quarter of the frame empty, fading to pure black. No text, letters, logos or watermarks. Avoid blood, wounds, nudity, gore, cartoon or children's-book style, and saturated colors.

【STYLE-ZH】
竖版 9:16 电影静帧，35mm 变形宽银幕质感。黑曜石般的暗黑世界，冷调古金是唯一点缀色。低调明暗对比，单一动机轮廓光，薄体积雾，细腻胶片颗粒。人物呈风化黑色大理石雕像质感，带淡金纹理，面部半隐于阴影，不出现写实皮肤。克制、宏大、纪录片气质。画面下方四分之一留空并渐隐为纯黑。不出现文字、字母、标志、水印。避免血迹、伤口、裸露、血腥、卡通或儿童绘本风格、高饱和色彩。

【FLOW-MOTION-SUFFIX】
8-second single shot, locked or very slow camera move, no shake, no cuts. Heavy, minimal motion; slow-motion haze and dust. Keep the composition and palette of the reference frame. No text.
```

---

### 2. 24 集核心构图与动效提示词总汇

#### 第一幕 · 荒谬与系统

- **EP.01 西西弗斯**（挂载 p0–p1、p7）：
  - **IMG-EN**: Low-angle shot on a steep barren slope at night. A lone statue-like man presses both palms against a colossal rough boulder, shoulder braced, seen from a rear three-quarter view. A thin line of cold gold light traces the boulder's edge. The summit is lost in darkness; loose gravel and dust hang in the air.
  - **IMG-ZH**: 夜色陡坡仰拍。石像质感的男子背侧身，双掌抵住巨石、肩膀顶住；巨石边缘一线冷金光；山顶隐没在黑暗里，碎石与尘埃悬浮。
  - **FLOW**: Very slow push-in toward the hands; dust drifts upward; the boulder creeps forward a few centimeters, then holds.
- **EP.02 普罗米修斯**（挂载 p2、p5）：
  - **IMG-EN**: A chained titan statue on a high black cliff holds a small ember in his open palm; its light reaches his own wide-open eyes. Far below, tiny figures sit around warm campfires, not looking up. A great eagle's shadow glides across storm clouds.
  - **IMG-ZH**: 被缚的泰坦石像立于黑色高崖，掌心托着一点火种，火光映亮他睁大的双眼；崖下远处小小人影围坐暖色篝火，无人抬头；巨鹰的影子掠过云层。
  - **FLOW**: The ember pulses like a heartbeat; campfire smoke rises below; the eagle's shadow crosses the clouds once; static camera.
- **EP.03 潘多拉**（挂载 p0–p2）：
  - **IMG-EN**: Close-up of a huge ancient Greek clay storage jar (pithos) with relief bands in a dark stone chamber. The heavy lid is sliding shut; a sliver of warm light still glows inside. Ash-dark moths swirl up and away from the rim.
  - **IMG-ZH**: 幽暗石室中一只带浮雕环带的巨型古希腊陶罐特写。厚重罐盖正在合上，缝隙里仍透着一线暖光；灰黑色飞蛾从罐口盘旋飞散。
  - **FLOW**: The lid slowly closes, sealing in the warm light; the last moths escape; dust settles; static camera.
- **EP.04 坦塔罗斯**（挂载 p1–p2、p6）：
  - **IMG-EN**: A gaunt king statue stands neck-deep in still black water inside a cavern. The water recedes from his lips in rings. Above him, a branch heavy with golden fruit hangs just out of reach.
  - **IMG-ZH**: 洞窟中，一位消瘦的国王石像齐颈站在静止的黑水里，水面以同心圆从唇边退去；头顶一枝挂满金色果实的枝条，差一寸够不着。
  - **FLOW**: As he leans forward, the water withdraws in concentric rings and the branch lifts away by a hand's width; slow motion.
- **EP.05 达那伊得斯**（挂载 p1–p2）：
  - **IMG-EN**: An underworld riverbank in blue-black darkness. A line of veiled women statues in long robes pours water from amphorae into a tall cracked jar; silver threads of water leak from its base into the sand. The repetition recedes into fog.
  - **IMG-ZH**: 蓝黑色的冥河岸边，一列身着长袍、头覆面纱的女性石像，用双耳瓶往一只开裂的高瓮里倒水；瓮底漏出银色水线渗入沙中；队列向雾里无限延伸。
  - **FLOW**: The pouring continues in a slow loop; silver water leaks from the cracks; the camera tracks slowly along the line.
- **EP.06 阿特拉斯**（挂载 p0–p1、p8）：
  - **IMG-EN**: A kneeling titan statue bears a vast celestial sphere of stars on his shoulders. From the knees down his body is already turning into a mist-covered rocky mountain. Stars glow faintly on the sphere.
  - **IMG-ZH**: 跪地的泰坦石像双肩扛着巨大的星空天球；膝盖以下已化为云雾缭绕的岩山；天球上星光微亮。
  - **FLOW**: Stone texture creeps slowly up the legs; stars rotate on the sphere; extremely slow tilt up.

---

#### 第二幕 · 欲望与自我

- **EP.07 伊卡洛斯**（挂载 p2、p8）：
  - **IMG-EN**: A winged youth statue glides in a narrow luminous corridor between a blazing pale sun at the top of the frame and a dark heaving sea at the bottom. Feathers are bound with glinting wax; a few drift loose.
  - **IMG-ZH**: 生翼少年石像在一条狭窄的光带中滑翔：画面上方是灼白烈日，下方是翻涌的暗海；羽毛以发亮的蜡粘合，几根正在脱落。
  - **FLOW**: He glides steadily along the corridor; the sun flare breathes; the sea swells below; a single feather falls; the camera follows sideways.
- **EP.08 纳西索斯**（挂载 p1、p8）：
  - **IMG-EN**: A young man statue kneels at the edge of a perfectly still forest pool. His reflection is brighter, smoother and more perfect than he is. Pale narcissus flowers line the edge; a faint woman's silhouette is half-hidden among the trees behind him.
  - **IMG-ZH**: 少年石像跪在一池绝对静止的林中水边；倒影比他本人更明亮、更光滑、更完美；水边开着淡色水仙；身后树影间隐约有一个女子的轮廓。
  - **FLOW**: A single tear drops; the reflection shatters into ripples and struggles to re-form; static, slightly top-down camera.
- **EP.09 迈达斯**（挂载 p1–p2、p8）：
  - **IMG-EN**: A dim royal banquet table. A king's hand, gold up to the wrist, touches bread and grapes; gold spreads outward from the point of contact, freezing the food into metal. The candlelight turns cold.
  - **IMG-ZH**: 昏暗的王宫宴桌。一只金化到手腕的国王之手触碰面包和葡萄，金色从触点向外蔓延，把食物凝成金属；烛光转冷。
  - **FLOW**: A wave of gold spreads slowly across the tabletop from the fingertips; candle flames stop flickering as the gold passes; slow macro push-in.
- **EP.10 法厄同**（挂载 p3–p4）：
  - **IMG-EN**: Four fiery horses drag a sun chariot off its arc across the night sky; the reins have snapped and whip in the air; the empty chariot tilts. Far below, the curved earth begins to glow orange along a single line. Stylized, no people burning.
  - **IMG-ZH**: 四匹烈焰神驹拖着太阳车偏离夜空的弧形轨道，缰绳断裂、甩在空中，空车倾斜；下方弧形的大地沿一条线开始泛起橙光。风格化处理，不出现燃烧的人。
  - **FLOW**: The horses veer away; the snapped reins flail; a glowing line spreads across the land below; slow motion.
- **EP.11 厄律西克同**（挂载 p1–p3）：
  - **IMG-EN**: A colossal ancient oak hung with ribbons and votive tablets, so large it feels like a forest. At its base a tiny man statue raises an axe. A pale, gaunt female figure made of mist hovers in the branches.
  - **IMG-ZH**: 一棵挂满彩带和还愿牌的巨型古橡树，大到如同一整片森林；树下一个渺小的男子石像举起斧头；枝间悬浮着一个由雾气构成、苍白消瘦的女性身影。
  - **FLOW**: Wind moves the ribbons; the mist figure drifts down toward the man; the axe stays raised; slow tilt down.
- **EP.12 皮格马利翁**（挂载 p1、p4–p5）：
  - **IMG-EN**: A sculptor's dim studio with marble dust in the air. A fully draped ivory statue of a young woman; warmth spreads from her fingertips, and her eyes are just opening with two faint points of light. The sculptor's hand is withdrawn at the edge of the frame.
  - **IMG-ZH**: 幽暗的雕刻工坊，空中飘着石粉。一尊衣袍完整的象牙少女雕像，暖意从指尖蔓延，双眼刚刚睁开，亮起两点微光；雕刻者的手退到画框边缘。
  - **FLOW**: The ivory warms in tone from the fingertips upward; the eyelids lift; two small points of light appear in the eyes; static close-up.

---

#### 第三幕 · 命运与认知

- **EP.13 俄狄浦斯**（挂载 p1、p4–p5）：
  - **IMG-EN**: A traveler statue with a walking staff stands at a misty three-way crossroads in rocky hills. Three paths split ahead; only one is already faintly lit in cold gold. A sphinx silhouette sits on a distant ridge.
  - **IMG-ZH**: 拄杖的旅人石像站在山间雾中的三岔路口；三条路在前方分开，只有一条早已泛着冷金微光；远处山脊上蹲着斯芬克斯的剪影。
  - **FLOW**: Fog drifts across the crossroads; the lit path brightens as he steps toward it; static high-angle camera.
- **EP.14 卡珊德拉**（挂载 p3–p4）：
  - **IMG-EN**: Night on the wall of an ancient city. Behind the gates, a huge wooden horse is surrounded by warm festive torches and celebrating silhouettes. On the wall, a cloaked woman stands alone, lit only by cold blue light, facing the viewer.
  - **IMG-ZH**: 古城城墙之夜。城门内一匹巨大的木马被暖色火把和狂欢人影包围；城墙上一位披斗篷的女子独自伫立，只被冷蓝光照亮，正面望向镜头。
  - **FLOW**: The torches flicker warmly; she stays still; the cold blue light holds on her; slow push-in.
- **EP.15 普罗克路斯忒斯**（挂载 p3–p4）：
  - **IMG-EN**: An empty stone hall under cold top light. Two iron beds stand side by side, one oversized and one too small, with a measuring rod lying across them. Loose chains and leather straps hang down. No people.
  - **IMG-ZH**: 空无一人的石厅，冷顶光。一大一小两张铁床并排，一根量尺横放其上；锁链和皮带松垂。不出现人物。
  - **FLOW**: A thin horizontal scanning light sweeps across both beds again and again; dust floats in the beam; static.
- **EP.16 代达罗斯**（挂载 p3、p6）：
  - **IMG-EN**: Top-down view of a vast labyrinth carved from black stone. At its center a tiny man statue looks straight up toward the camera; above him, the open starry sky; feathers float up toward his shoulders.
  - **IMG-ZH**: 俯拍黑石雕成的巨大迷宫；中心一个渺小的男子石像仰头直视镜头；上方是敞开的星空，羽毛正向他肩头飘聚。
  - **FLOW**: The camera tilts from the top-down labyrinth up into the open starry sky; feathers gather; slow and smooth.
- **EP.17 美杜莎**（挂载 p7–p8）：
  - **IMG-EN**: A dark marble bust of a calm woman with a crown of carved serpents for hair, looking straight into the lens with a faint, serene smile. Behind her, a polished bronze shield reflects her. Warm light breaks through cracks in a layer of grey stone dust.
  - **IMG-ZH**: 一尊黑色大理石女性胸像，发间盘着雕刻的蛇，神情平静，带着淡淡的微笑直视镜头；身后一面磨亮的青铜盾映出她的轮廓；暖光从灰色石尘的裂缝中透出。
  - **FLOW**: Grey stone dust peels away from the face to reveal a warm tone; the serpents barely move; she holds eye contact; static.
- **EP.18 阿拉克涅**（挂载 p3–p6）：
  - **IMG-EN**: A weaver's workshop with two large tapestries side by side on looms: one ordered and imperial, the other dense with dark mythic motifs (a bull, a swan, golden rain, a serpent-haired woman) shown only as abstract patterns. Torn golden threads hang suspended in the air; a glistening spider web fills one corner.
  - **IMG-ZH**: 织坊里两幅巨大织锦并排挂在织机上：一幅秩序森严、充满帝王气象；另一幅密布暗色神话纹样（公牛、天鹅、金雨、蛇发女子），只以抽象图案呈现。撕裂的金线悬停在空中，角落里一张蛛网闪着微光。
  - **FLOW**: The torn threads hang in the air, then slowly drift and begin weaving into a web in the corner; dew catches the light.

---

#### 第四幕 · 力量与终局

- **EP.19 阿喀琉斯**（挂载 p4、p8）：
  - **IMG-EN**: Inside a dim tent lit by a single oil lamp, an old king and a young warrior, both as statues, kneel facing each other with lowered foreheads; golden armor lies set aside on the ground. A tear-like glint between them.
  - **IMG-ZH**: 一盏油灯照亮的昏暗营帐里，老国王与青年战士（均为石像）相对跪坐、额头低垂；金色盔甲卸在地上；两人之间一点泪光般的闪光。
  - **FLOW**: The lamp flame breathes; gold flakes fall slowly from the armor; very slow push-in.
- **EP.20 克洛诺斯**（挂载 p4–p5、p8）：
  - **IMG-EN**: A colossal hooded titan statue sits on a stone throne holding a swaddled stone; an adamant sickle leans against the throne. Behind him, a giant celestial ring like a clock dial, with the sickle's shadow as its hand.
  - **IMG-ZH**: 戴兜帽的巨型泰坦石像坐在石座上，双手捧着一块襁褓包裹的石头；一把坚不可摧的镰刀斜靠在石座旁；身后一圈巨大的天体圆环如同表盘，镰刀的影子就是表针。
  - **FLOW**: The ring rotates very slowly, the sickle's shadow sweeping across it like a clock hand; static.
- **EP.21 赫拉克勒斯**（挂载 p3、p7）：
  - **IMG-EN**: A hero statue wearing a lion skin stands on a mountain ridge drawing a bow upward. High on a distant cliff, the chains binding a titan are breaking apart in light; an eagle silhouette falls away. Stylized, no blood.
  - **IMG-ZH**: 身披狮皮的英雄石像立于山脊，向上拉弓；远方高崖上，缚住泰坦的锁链在光中崩断；一只鹰的剪影坠落远去。风格化处理，不出现血迹。
  - **FLOW**: An arrow of light streaks upward; the chains shatter into gold sparks; the eagle silhouette tumbles away into the clouds; slow motion.
- **EP.22 俄耳甫斯**（挂载 p3–p5）：
  - **IMG-EN**: A narrow misty mountain path climbs toward a cave mouth full of soft dawn light. A man with a lyre stands at the threshold, turning his head back over his shoulder. Behind him, a translucent pale-blue woman figure dissolves like sand into the darkness, one hand reaching out.
  - **IMG-ZH**: 雾中狭窄山道通向洒满晨光的洞口；抱琴男子站在光的门槛上回头；身后一个半透明的淡蓝女性身影正像沙一样溶入黑暗，一只手向前伸着。
  - **FLOW**: Warm light touches his shoulder; as he turns, the blue figure is pulled back into the dark like sand; her hand stays suspended; static.
- **EP.23 塞壬**（挂载 p5–p7）：
  - **IMG-EN**: Night sea, an ancient ship. A man statue is bound tightly to the mast with ropes; below, rowers with bowed heads keep rowing. Thin golden waves of sound ripple across the water toward the mast. No mermaids, no visible creatures.
  - **IMG-ZH**: 夜海上的古船。男子石像被绳索紧紧绑在桅杆上；下方桨手低头划桨；细细的金色声波从海面荡向桅杆。不出现美人鱼或任何生物形象。
  - **FLOW**: The golden sound waves approach; he strains; another loop of rope tightens; the rowers keep rowing; the camera slowly circles the mast.
- **EP.24 奥德修斯**（挂载 p0–p5、p8 & 片尾）：
  - **IMG-EN**: A man statue sits on a seaside rock on a silent island. The sea is perfectly still like glass, foam frozen mid-air, leaves suspended. A half-built wooden raft and an axe lie on the shore. Endless dusk.
  - **IMG-ZH**: 寂静岛屿的海边礁石上坐着一个男子石像；海面如玻璃般绝对静止，浪花凝在半空，树叶悬停；岸边是一只造到一半的木筏和一把斧头；永恒的黄昏。
  - **FLOW**: Everything holds frozen; then the raft pushes off, the frozen foam falls, the waves begin to move and wind fills a small sail; static camera, then a slow pull-back.
  - **IMG-ALT（终局彩蛋床）**: The roots of a living olive tree grow through the frame of an ancient wooden bed in a stone bedroom, roots glowing faintly gold as they sink into the earth. (石砌卧室里，一棵活橄榄树的根系穿过古老木床的床架，根须泛着淡金微光扎入大地。)

---

## 三、Canvas / WebGL 渲染管线与 Clean Feed 严苛标准

### 1. 核心画面分区（Safe Zones）

| 区域名称 | Y 轴区间 | 规则与用途 |
| :--- | :---: | :--- |
| **主画面区** | `0 ～ 1344` | 主体构图、高能冲击、关键粒子形态必须完全落在此区域内 |
| **字幕安全带** | `1340 ～ 1500` | 母版**零任何字幕**；剪映独立字幕轨中心线定在 `Y ≈ 1420` |
| **暗黑渐变过渡区** | `1344 ～ 1536` | Canvas 渲染不透明度从 0 线性渐变至 0.95，压暗至纯黑底色 |
| **硬净安全区 (Clean Feed)** | `1536 ～ 1920` | **绝对纯净黑曜石底色（#07080B）**，无任何文字、粒子高光或画面残留（留给手机端短视频 UI、账号名与交互栏） |
| **右侧按钮规避区** | `X > 900, Y 900~1650` | 字幕文本宽度最大限制在 720px（居中 `X: 180~900`），避免被点赞与分享键遮挡 |

### 2. 确定性渲染铁律 (Deterministic Rendering)
- **严禁使用非确定性函数**：禁用 `Math.random()`、`Date.now()`、`performance.now()`。
- **带种子伪随机数**：所有随机散布均采用 `mulberry32(seed)` 算法，种子写入各集配置文件。
- **时间纯粹由帧驱动**：`t = frame / 30.0`，严格 1650 帧（EP.01~23）及 1800 帧（EP.24）。
- **每集恰有且仅有一次 BURST 状态**：由自动化脚本执行校验，绝无随意震荡。

---

## 四、剪映 Pro 自动化工程轨线规范

### 1. 五层多轨精准排布架构

```
[ T3: 片尾字卡轨 ]  -----------------------------------> [ 骁清Finn 签名与引文字卡 (不念) ]
[ T2: 原文引文轨 ]  ----------------------------> [ 拉丁文/希腊文浮层 (如 ΗΜΑΤΑ ΠΑΝΤΑ) ]
[ T1: 口播字幕轨 ]  [ p0 字幕 ] [ p1 字幕 ] ... [ p8 字幕 ] [ p9 CTA 字幕 ] (香槟金 #ffd76a 高光)
[ V1: 视频母版轨 ]  ======================== 1650 帧 Clean Feed Master ========================
[ A1: 口播语音轨 ]  [ p0.wav ] [ p1.wav ] ... [ p8.wav ] [ p9.wav ] (YunxiNeural 48kHz)
[ A2: 真人签名轨 ]                                        [ "我是骁清Finn" 真人原声音频 ]
[ A3: 电影氛围底 ]  ~~~~~~~~~~~~~~~~~~~~ 深沉低频环境音底噪 (-20dB) ~~~~~~~~~~~~~~~~~~~~
[ A4: 高能冲击音 ]                 [ BURST 对应冲击低音炮 SFX ]
```

### 2. 音频参数与多音字纠偏规范
- **TTS 音色**：`zh-CN-YunxiNeural`，输出标准 `Riff48Khz16BitMonoPcm`。
- **声学响度**：综合响度 `-14 LUFS`，真峰值 $\le -1\text{ dBTP}$。
- **多音字纠错清单**（必须在 SSML 中使用拼音标注或严格检查）：
  - `周一重启`：**chóng**（EP.01）
  - `肝脏长回来`：**zhǎng**（EP.02）
  - `只差一寸`：**chà**（EP.04）
  - `长子长女`：**zhǎng**（EP.06）
  - `塞回大地`：**sāi**（EP.20）
  - `塞壬`：**sài**（EP.23）
  - `骁清`：**xiāo**（全集品牌词）

---

## 五、骁清Finn 创作者全系列寄语

> **二十四集，二十四件刑具，二十四件武器。**  
> 
> 我不是来讲神话的。神话里的每一块石头，今天都换了名字，压在我们身上：绩效、房贷、懂事、标准答案、为你推荐。诸神从来没有离开，他们只是学会了不露面。  
> 
> 这个系列没有廉价的答案。我只是把“看清”的过程拆开，做成你能带走的东西：蔑视、先见、卸下，拒绝那张床，守护你的软肋，然后选择有限。  
> 
> 第一集问你，你的石头叫什么名字。最后一集问你，你的家在哪里。中间这段路，是你自己走的。  
> 
> **诸神是系统。凡人唯一的武器，是清醒。清醒的尽头，是回家。**  
> 
> **我是骁清Finn。想清楚了，就出发。**
