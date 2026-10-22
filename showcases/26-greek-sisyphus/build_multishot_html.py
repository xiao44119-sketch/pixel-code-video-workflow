#!/usr/bin/env python3
"""
Generate the multi-shot cinematic WebGL master index.html for EP.01 Sisyphus
Featuring:
- 8 high-res cinematic plates loaded across 10 narrative beats (averaging ~5s per shot, eliminating monotony)
- Dynamic camera tracks per shot (pan, tilt, push, recoil, drift)
- Lightning flashes, chromatic aberration, heat refraction, shockwave burst at 37s, volumetric God rays
- Deterministic multi-stage particle physics (storm dust, blue underworld embers, sparks, dusk motes, high-energy burst, ascending dawn dust)
- 100% Clean feed (zero hardcoded text, bottom safe zone strictly obsidian)
"""

HTML_CONTENT = r'''<!-- File: index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EP.01 西西弗斯 · 电影级多镜头母版 v3</title>
<style>
  html, body {
    margin: 0;
    height: 100%;
    background: #000;
    color: #9a9286;
    font: 12px/1.4 system-ui, sans-serif;
    overflow: hidden;
  }
  #wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 8px;
  }
  #c {
    height: calc(100vh - 72px);
    width: auto;
    aspect-ratio: 9 / 16;
    background: #07080B;
    display: block;
  }
  #ui {
    display: flex;
    gap: 10px;
    align-items: center;
    width: min(90vw, 640px);
  }
  #ui button {
    background: #12151B;
    color: #c9c2b4;
    border: 1px solid #2a2e36;
    padding: 4px 14px;
    cursor: pointer;
  }
  #scrub { flex: 1; }
  #frameInfo { min-width: 120px; text-align: right; font-variant-numeric: tabular-nums; }
  #status { color: #b8935a; min-height: 16px; }
  body.render #ui,
  body.render #status { display: none; }
  body.render #wrap { display: block; }
  body.render #c { width: 1080px; height: 1920px; }
</style>
</head>
<body>
<div id="wrap">
  <canvas id="c" width="1080" height="1920"></canvas>
  <div id="ui">
    <button id="play">▶ 播放</button>
    <input id="scrub" type="range" min="0" max="1649" value="0" step="1">
    <span id="frameInfo">f 0 / 0.00s</span>
  </div>
  <div id="status"></div>
</div>

<script type="module">
// ============================================================
// 0. 全局配置：8个镜头资产与时间表
// ============================================================
const CONFIG = {
  plates: [
    "assets/shot0_fall.jpg",     // 0: 0.0~5.0s 巨石滚落/坠入深渊
    "assets/shot1_abyss.jpg",    // 1: 5.0~10.0s 孤独仰望/暴风雨云涡
    "assets/shot2_death.jpg",    // 2: 10.0~16.2s 幽冥锁死神/太想活着
    "assets/shot3_struggle.jpg", // 3: 16.2~22.2s 肌肉硬推/熔岩裂缝
    "assets/shot4_walkdown.jpg", // 4: 22.2~27.2s 加缪下山/从容漫步
    "assets/shot5_lucid.jpg",    // 5: 27.2~31.8s 大理石金纹特写/清醒凝视
    "assets/shot6_approach.jpg", // 6: 31.8~37.0s 再次逼近/风暴蓄势
    "assets/shot7_summit.jpg",   // 7: 37.0~55.0s 触石爆发/破晓神光/终极复仇
  ],
  fissure: [0.50, 0.52],   // Shot3 火星喷射点
  burst:   [0.50, 0.54],   // Shot7 37s 触石冲击波爆发点
  sun:     [0.50, 0.22],   // Shot7 破晓朝阳神光聚焦点
  seed: 20260101,
  counts: [1500, 1500, 1500, 2800, 1800], // 风暴微尘 / 熔岩火星 / 石粉 / 冲击爆散金粉 / 破晓升腾金粉
};

const W = 1080;
const H = 1920;
const FPS = 30;
const TOTAL = 1650;
const BURST_T = 37.0; // 第 1110 帧高能爆发点

// ============================================================
// 1. 确定性随机数与数学工具
// ============================================================
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const ss = (a, b, x) => {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};
const easeInOut = (x) => {
  const t = clamp01(x);
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
};
const win = (a, b, c, d, x) => ss(a, b, x) * (1 - ss(c, d, x));

function integ(fn, t0, t1) {
  if (t1 <= t0) return 0;
  const dt = 1 / 240;
  let sum = 0;
  for (let x = t0; x < t1; x += dt) {
    const h = Math.min(dt, t1 - x);
    sum += fn(x + h * 0.5) * h;
  }
  return sum;
}

// 粒子时间膨胀系统：p5 清醒时刻粒子速度降为 15%
const speed = (t) => 1.0 - 0.85 * win(27.2, 27.8, 31.0, 31.6, t);
const clock = (t) => integ(speed, 0, t);
const CLOCK_BURST = clock(BURST_T);

// 闪电时间点
const LIGHTNING = [[1.2, 0.4], [3.8, 0.8], [7.5, 0.5], [9.8, 0.9], [15.8, 0.95], [36.7, 0.7]];
function lightning(t) {
  let v = 0;
  for (const [te, s] of LIGHTNING) {
    const d = t - te;
    if (d < 0 || d > 0.8) continue;
    v += s * (Math.exp(-d * 18) + 0.5 * Math.exp(-(((d - 0.12) / 0.04) ** 2)));
  }
  return v;
}

// ============================================================
// 2. 8个镜头的动态运镜 [scale, offX, offY, rot]
// ============================================================
function getCam(shotIdx, tInShot, dur, tGlobal) {
  const u = clamp01(tInShot / dur);
  const e = easeInOut(u);

  if (shotIdx === 0) { // 巨石滚落：剧烈下沉与微震
    return [
      1.12 + 0.10 * e,
      0.005 * Math.sin(tGlobal * 40.0) * (1.0 - e * 0.5),
      -0.03 + 0.06 * e + 0.004 * Math.cos(tGlobal * 45.0),
      -0.006 * e
    ];
  } else if (shotIdx === 1) { // 深渊仰望：徐徐仰推
    return [
      1.10 + 0.08 * e,
      0.004 * Math.sin(tGlobal * 0.3),
      0.03 - 0.05 * e,
      0.003 * Math.sin(tGlobal * 0.2)
    ];
  } else if (shotIdx === 2) { // 锁死神：幽暗潜入推近
    return [
      1.14 + 0.12 * e,
      0.01 * (1.0 - e),
      0.01 - 0.02 * e,
      0.002 * Math.sin(tGlobal * 0.4)
    ];
  } else if (shotIdx === 3) { // 肌肉硬推：高阻力颤动与推力脉动
    const ph = ((tInShot % 2.5) / 2.5);
    const env = ph < 0.3 ? ss(0, 0.3, ph) : 1 - ss(0.3, 1, ph);
    const shake = env * 0.0025 * Math.sin(tGlobal * 60.0);
    return [
      1.15 + 0.12 * e + 0.018 * env,
      shake,
      0.01 * env,
      0.002 * Math.sin(tGlobal * 0.5)
    ];
  } else if (shotIdx === 4) { // 加缪下山：平稳从容下移跟随
    return [
      1.18 - 0.08 * e,
      -0.01 + 0.02 * e,
      -0.02 + 0.04 * e,
      0.002 * Math.cos(tGlobal * 0.3)
    ];
  } else if (shotIdx === 5) { // 清醒面庞：极缓微动悬浮
    return [
      1.16 + 0.05 * e,
      0.005 * Math.sin(tGlobal * 0.15),
      0.003 * Math.cos(tGlobal * 0.2),
      0.001 * Math.sin(tGlobal * 0.1)
    ];
  } else if (shotIdx === 6) { // 逼近巨石：风暴蓄势压迫推近
    return [
      1.15 + 0.14 * e,
      0.004 * Math.sin(tGlobal * 20.0) * e,
      -0.01 + 0.03 * e,
      0.003 * e
    ];
  } else { // 山巅破晓：37s 触石冲击波后座力 + 宏大拉远
    const b = tGlobal - BURST_T;
    if (b < 0) {
      return [1.20 + 0.04 * ss(36.5, 37.0, tGlobal), 0, 0.01, 0];
    }
    const kick = Math.exp(-b * 4.5);
    return [
      1.22 - 0.08 * (1.0 - Math.exp(-b * 4.0)) - 0.06 * ss(37.0, 55.0, tGlobal),
      0.008 * kick * Math.sin(b * 55.0),
      0.01 - 0.03 * ss(38.0, 55.0, tGlobal) + 0.006 * kick * Math.sin(b * 43.0),
      0.003 * kick * Math.sin(b * 30.0)
    ];
  }
}

// 8个镜头的起止区间
const SHOTS_TIMELINE = [
  { id: 0, start: 0.0,  end: 5.0  },
  { id: 1, start: 4.8,  end: 10.0 },
  { id: 2, start: 9.8,  end: 16.2 },
  { id: 3, start: 16.0, end: 22.2 },
  { id: 4, start: 22.0, end: 27.2 },
  { id: 5, start: 27.0, end: 31.8 },
  { id: 6, start: 31.6, end: 37.0 },
  { id: 7, start: 36.8, end: 55.0 },
];

function computeShotWeights(t) {
  const w = new Float32Array(8);
  for (let i = 0; i < 8; i++) {
    const s = SHOTS_TIMELINE[i];
    if (t >= s.start && t <= s.end) {
      let weight = 1.0;
      // 入场渐变
      if (i > 0 && t < s.start + 0.35) {
        weight *= ss(s.start, s.start + 0.35, t);
      }
      // 出场渐变
      if (i < 7 && t > s.end - 0.35) {
        weight *= 1.0 - ss(s.end - 0.35, s.end, t);
      }
      w[i] = weight;
    }
  }
  // 归一化权重
  let sum = 0;
  for (let i = 0; i < 8; i++) sum += w[i];
  if (sum > 0.0001) {
    for (let i = 0; i < 8; i++) w[i] /= sum;
  } else {
    w[7] = 1.0;
  }
  return w;
}

// ============================================================
// 3. 帧状态计算
// ============================================================
function frameState(f) {
  const t = f / FPS;
  const pt = clock(t);
  const b = t - BURST_T;
  const s = { t, pt, f };

  s.w = computeShotWeights(t);
  s.light = lightning(t);

  // 各镜头运镜参数
  s.cams = [];
  for (let i = 0; i < 8; i++) {
    const shot = SHOTS_TIMELINE[i];
    const tInShot = Math.max(0, t - shot.start);
    const dur = shot.end - shot.start;
    s.cams.push(getCam(i, tInShot, dur, t));
  }

  // 37s 冲击波高能状态
  s.shockAge = Math.max(0, b);
  s.shockOn = b >= 0 && b < 3.5 ? 1 : 0;
  s.flash = b >= 0 ? 0.90 * Math.exp(-b * 7.5) : 0;
  s.radius = b >= 0 ? 0.02 + 1.15 * (1.0 - Math.exp(-b * 3.2)) : 0;
  s.rays = ss(37.0, 38.6, t) * (1.0 - 0.3 * win(42.5, 43.5, 46.5, 47.5, t)) * (0.92 + 0.08 * Math.sin(t * 0.8));
  s.burstAge = b >= 0 ? pt - CLOCK_BURST : -1;
  s.dawn = ss(37.0, 39.5, t);

  s.vig = t < 36.5 ? 0.58 : b < 0 ? 0.58 + 0.25 * ss(36.5, 37.0, t) : 0.40 + 0.40 * Math.exp(-b * 3.0);
  s.ca = b < 0 ? 1.0 + 2.0 * ss(36.5, 37.0, t) : 1.0;
  s.grain = t < 16 ? 0.06 : t < 36.5 ? 0.052 : 0.042;
  s.fade = ss(0, 1.2, t) * (1 - ss(53.6, 55.0, t));
  return s;
}

// ============================================================
// 4. 着色器代码
// ============================================================
const VS_QUAD = `#version 300 es
layout(location = 0) in vec2 aPos;
out vec2 vUv;
void main() {
  vUv = aPos * 0.5 + 0.5;
  gl_Position = vec4(aPos, 0.0, 1.0);
}`;

const FS_SCENE = `#version 300 es
precision highp float;
in vec2 vUv;
out vec4 o;

uniform sampler2D uT0;
uniform sampler2D uT1;
uniform sampler2D uT2;
uniform sampler2D uT3;
uniform sampler2D uT4;
uniform sampler2D uT5;
uniform sampler2D uT6;
uniform sampler2D uT7;

uniform vec4 uCam0;
uniform vec4 uCam1;
uniform vec4 uCam2;
uniform vec4 uCam3;
uniform vec4 uCam4;
uniform vec4 uCam5;
uniform vec4 uCam6;
uniform vec4 uCam7;

uniform float uW[8];
uniform float uTime;
uniform float uLight;
uniform float uRadius;
uniform float uShockOn;
uniform float uDawn;

const float SA = 0.5625;
const vec3 OBS = vec3(0.027, 0.031, 0.043);

float hash(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}
float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
             mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}
float fbm(vec2 p) {
  float v = 0.0;
  float a = 0.5;
  for (int i = 0; i < 4; i++) {
    v += a * noise(p);
    p = p * 2.02 + vec2(1.7, 9.2);
    a *= 0.5;
  }
  return v;
}
float luma(vec3 c) { return dot(c, vec3(0.2126, 0.7152, 0.0722)); }
vec3 contrast(vec3 c, float k) { return clamp((c - 0.5) * k + 0.5, 0.0, 1.0); }

vec2 camUV(vec2 uvT, vec4 cam) {
  vec2 p = (uvT - 0.5) * vec2(SA, 1.0);
  float c = cos(cam.w);
  float s = sin(cam.w);
  p = mat2(c, -s, s, c) * p;
  p /= cam.x;
  p += cam.yz;
  return vec2(p.x / SA + 0.5, p.y + 0.5);
}

vec3 sampleShot(int idx, vec2 uvT) {
  vec2 uv;
  vec3 col = vec3(0.0);
  if (idx == 0) {
    uv = camUV(uvT, uCam0);
    col = texture(uT0, uv).rgb;
    col += uLight * 0.45 * vec3(0.65, 0.8, 1.0) * (1.0 - uv.y);
  } else if (idx == 1) {
    uv = camUV(uvT, uCam1);
    float sky = 1.0 - smoothstep(0.2, 0.65, uv.y);
    uv += (vec2(fbm(uv * 3.0 + uTime * 0.02), fbm(uv * 3.0 + 5.0)) - 0.5) * 0.01 * sky;
    col = texture(uT1, uv).rgb;
    col += uLight * 0.40 * vec3(0.6, 0.75, 1.0) * sky;
  } else if (idx == 2) {
    uv = camUV(uvT, uCam2);
    col = texture(uT2, uv).rgb;
    // 冥府冷蓝焰与金链光泽强化
    float blueMask = smoothstep(0.05, 0.35, col.b - col.r);
    col += vec3(0.2, 0.4, 0.9) * blueMask * 0.3;
  } else if (idx == 3) {
    uv = camUV(uvT, uCam3);
    float warm = smoothstep(0.1, 0.4, col.r - col.b);
    uv += (vec2(noise(uv * 35.0 - uTime * 1.5), noise(uv * 35.0 + 6.0)) - 0.5) * 0.003 * warm;
    col = texture(uT3, uv).rgb;
    col += vec3(1.0, 0.5, 0.15) * warm * 0.45;
  } else if (idx == 4) {
    uv = camUV(uvT, uCam4);
    col = texture(uT4, uv).rgb;
    col = contrast(col, 1.08) * vec3(0.95, 0.95, 1.02);
  } else if (idx == 5) {
    uv = camUV(uvT, uCam5);
    col = texture(uT5, uv).rgb;
    // 大理石金纹微光脉冲
    float goldVein = smoothstep(0.12, 0.45, col.r - col.b) * smoothstep(0.3, 0.8, luma(col));
    col += vec3(1.0, 0.8, 0.3) * goldVein * (0.35 + 0.25 * sin(uTime * 2.0));
  } else if (idx == 6) {
    uv = camUV(uvT, uCam6);
    col = texture(uT6, uv).rgb;
    col += uLight * 0.3 * vec3(0.8, 0.7, 0.5);
  } else {
    uv = camUV(uvT, uCam7);
    col = texture(uT7, uv).rgb;
    // 破晓朝阳光辉
    col = contrast(col * vec3(1.06, 0.98, 0.88), 1.08);
    col += vec3(1.0, 0.65, 0.25) * uDawn * 0.25;
  }
  return col;
}

void main() {
  vec2 uvT = vec2(vUv.x, 1.0 - vUv.y);
  vec3 col = vec3(0.0);

  for (int i = 0; i < 8; i++) {
    if (uW[i] > 0.001) {
      col += sampleShot(i, uvT) * uW[i];
    }
  }

  col = OBS + col * (1.0 - OBS);
  o = vec4(col, 1.0);
}`;

const VS_PART = `#version 300 es
precision highp float;
layout(location = 0) in vec4 aSeed;
layout(location = 1) in float aKind;

uniform float uPT;
uniform float uBurstAge;
uniform float uDawn;
uniform vec2 uBurst;
uniform vec2 uFissure;
uniform float uW[8];

out vec4 vCol;
out float vSoft;

const vec2 RES = vec2(1080.0, 1920.0);
const float PI = 3.14159265;
float h(float x) { return fract(sin(x) * 43758.5453); }

void main() {
  vec2 p = vec2(-9999.0);
  float a = 0.0;
  float sz = 1.0;
  vec3 c = vec3(1.0);
  float soft = 0.5;
  int k = int(aKind + 0.5);

  if (k == 0) { // 风暴微尘 (Shot 0, 1, 6)
    float activeW = uW[0] + uW[1] + uW[6];
    float L = 6.0 + 4.0 * aSeed.x;
    float age = mod(uPT + aSeed.y * L, L);
    p.x = aSeed.z * RES.x + sin(uPT * 0.4 + aSeed.w * 6.28) * 30.0;
    p.y = RES.y * (0.2 + 0.8 * aSeed.w) - age * (15.0 + 30.0 * aSeed.x);
    float s = sin(PI * age / L);
    a = s * s * 0.35 * activeW;
    sz = 1.8 + 2.5 * aSeed.z;
    c = vec3(0.65, 0.75, 0.90);
  } else if (k == 1) { // 熔岩火星 (Shot 3)
    float activeW = uW[3];
    float L = 1.2 + 1.2 * aSeed.x;
    float cyc = uPT + aSeed.y * L * 6.0;
    float age = mod(cyc, L);
    float id = floor(cyc / L);
    float r1 = h((id + 1.0) * (aSeed.z * 91.7 + 3.1));
    float r2 = h((id + 1.0) * (aSeed.w * 57.3 + 7.7));
    vec2 e = uFissure * RES + vec2((r1 - 0.5) * 350.0, (r2 - 0.5) * 200.0);
    vec2 v = vec2((aSeed.z - 0.5) * 500.0, -(180.0 + 400.0 * aSeed.w));
    p = e + v * age + vec2(60.0 * age * age, 300.0 * age * age);
    float life = 1.0 - age / L;
    a = life * life * 0.85 * activeW;
    sz = 1.8 + 2.8 * aSeed.x * life;
    c = mix(vec3(1.0, 0.4, 0.1), vec3(1.0, 0.88, 0.5), life);
    soft = 0.35;
  } else if (k == 2) { // 冥府幽蓝微粒 (Shot 2) & 下山暮光微尘 (Shot 4, 5)
    float activeW = uW[2] * 0.9 + (uW[4] + uW[5]) * 0.6;
    float L = 5.0 + 4.0 * aSeed.x;
    float age = mod(uPT * 0.7 + aSeed.y * L, L);
    p = vec2(aSeed.z * RES.x + sin(age * 1.5 + aSeed.w * 6.28) * 16.0,
             RES.y * (0.3 + 0.6 * aSeed.w) - age * 12.0);
    a = sin(PI * age / L) * 0.3 * activeW;
    sz = 2.0 + 3.5 * aSeed.w;
    soft = 0.75;
    c = uW[2] > 0.5 ? vec3(0.3, 0.6, 1.0) : vec3(0.9, 0.75, 0.5);
  } else if (k == 3) { // 37s 触石高能冲击金粉爆发 (Shot 7)
    if (uBurstAge > 0.0) {
      float b = uBurstAge;
      float ang = aSeed.x * 6.2831853;
      float spd = 300.0 + 1900.0 * aSeed.y * aSeed.y;
      float kd = 1.5 + 1.4 * aSeed.z;
      float dist = spd / kd * (1.0 - exp(-kd * b));
      vec2 dir = vec2(cos(ang), sin(ang));
      p = uBurst * RES + dir * dist
        + vec2(sin(b * 0.9 + aSeed.w * 6.28) * 25.0 * b, -(20.0 + 45.0 * aSeed.w) * b);
      a = exp(-b * 0.25) * uW[7];
      sz = (1.6 + 3.8 * aSeed.w) * (1.0 + 1.8 * exp(-b * 3.0));
      c = mix(vec3(1.0, 0.95, 0.85), vec3(1.0, 0.72, 0.3), clamp(b * 0.6, 0.0, 1.0));
      soft = 0.35;
    }
  } else { // 破晓升腾万千金尘 (Shot 7 后半段)
    float L = 6.0 + 5.0 * aSeed.x;
    float age = mod(uPT + aSeed.y * L, L);
    p = vec2(aSeed.z * RES.x + sin(age * 0.8 + aSeed.w * 6.28) * 40.0,
             RES.y * (0.55 + 0.45 * aSeed.w) - age * (45.0 + 75.0 * aSeed.y));
    a = sin(PI * age / L) * 0.45 * uDawn * uW[7];
    bool bokeh = aSeed.x > 0.92;
    sz = bokeh ? 9.0 + 14.0 * aSeed.z : 1.6 + 2.8 * aSeed.z;
    if (bokeh) a *= 0.4;
    c = vec3(1.0, 0.82, 0.45);
    soft = bokeh ? 0.9 : 0.5;
  }

  if (a <= 0.002) {
    gl_Position = vec4(2.0, 2.0, 0.0, 1.0);
    gl_PointSize = 0.0;
    vCol = vec4(0.0);
    vSoft = 0.0;
    return;
  }
  gl_Position = vec4(p.x / RES.x * 2.0 - 1.0, 1.0 - p.y / RES.y * 2.0, 0.0, 1.0);
  gl_PointSize = sz;
  vCol = vec4(c, a);
  vSoft = soft;
}`;

const FS_PART = `#version 300 es
precision highp float;
in vec4 vCol;
in float vSoft;
out vec4 o;
void main() {
  vec2 q = gl_PointCoord * 2.0 - 1.0;
  float d = dot(q, q);
  if (d > 1.0) discard;
  float f = pow(1.0 - d, mix(3.0, 1.2, vSoft));
  o = vec4(vCol.rgb, vCol.a * f);
}`;

const FS_POST = `#version 300 es
precision highp float;
in vec2 vUv;
out vec4 o;

uniform sampler2D uScene;
uniform float uTime;
uniform float uFrame;
uniform float uShockAge;
uniform float uShockOn;
uniform float uRadius;
uniform float uRays;
uniform float uFlash;
uniform float uFade;
uniform float uVig;
uniform float uCA;
uniform float uGrain;
uniform vec2 uBurst;
uniform vec2 uSun;

const float SA = 0.5625;
const vec3 OBS = vec3(0.027, 0.031, 0.043);

vec3 S(vec2 u) { return texture(uScene, vec2(u.x, 1.0 - u.y)).rgb; }
float luma(vec3 c) { return dot(c, vec3(0.2126, 0.7152, 0.0722)); }
float grain(vec2 p, float fr) {
  uvec3 v = uvec3(uvec2(p), uint(fr));
  uint x = v.x * 1973u + v.y * 9277u + v.z * 26699u;
  x = (x >> 13u) ^ x;
  x = x * (x * x * 15731u + 789221u) + 1376312589u;
  return float(x & 0x7fffffffu) / 2147483647.0;
}

void main() {
  vec2 uvT = vec2(vUv.x, 1.0 - vUv.y);

  // 37s 冲击波折射环
  vec2 d = (uvT - uBurst) * vec2(SA, 1.0);
  float dist = length(d);
  vec2 dir = d / (dist + 1e-5);
  float band = uShockOn * exp(-pow((dist - uRadius) / 0.055, 2.0));
  float decay = exp(-uShockAge * 1.4);
  vec2 uvD = uvT - vec2(dir.x / SA, dir.y) * band * 0.055 * decay;

  // 动态色散
  vec2 cd = uvD - 0.5;
  float ca = uCA * 0.007 * length(cd)
           + band * 0.020 * decay
           + uShockOn * 0.012 * exp(-uShockAge * 3.0);
  vec3 col = vec3(S(uvD + cd * ca).r, S(uvD).g, S(uvD - cd * ca).b);

  // 辉光与丁达尔神光
  if (uRays > 0.001) {
    vec2 delta = (uvD - uSun) * (0.92 / 48.0);
    vec2 c = uvD;
    float ill = 1.0;
    float acc = 0.0;
    for (int i = 0; i < 48; i++) {
      c -= delta;
      vec3 s = S(c);
      float warm = clamp((s.r - s.b) * 2.0 + 0.4, 0.0, 1.0);
      acc += max(luma(s) - 0.5, 0.0) * warm * ill;
      ill *= 0.96;
    }
    vec2 sd = (uvD - uSun) * vec2(SA, 1.0);
    col += vec3(1.0, 0.80, 0.48) * acc * 0.12 * uRays;
    col += vec3(1.0, 0.85, 0.55) * exp(-length(sd) * 5.0) * 0.35 * uRays;
  }

  // 冲击白金闪光
  col += vec3(1.0, 0.85, 0.55) * band * decay * 0.95;
  col = mix(col, vec3(1.0, 0.95, 0.82), clamp(uFlash, 0.0, 1.0));

  // 电影级暗角
  vec2 vq = (uvT - vec2(0.5, 0.44)) * vec2(1.0, 0.78) * 1.35;
  float v = 1.0 - smoothstep(0.2, 1.05, length(vq));
  col *= mix(1.0 - uVig, 1.0, v);

  col *= uFade;

  // 胶片微粒
  float g = grain(gl_FragCoord.xy, uFrame) - 0.5;
  col += g * uGrain * (1.0 - 0.55 * luma(col));

  // 底部黑曜石安全区 (Y >= 1536)
  float py = uvT.y * 1920.0;
  float a = smoothstep(1344.0, 1536.0, py) * 0.96;
  if (py >= 1536.0) a = mix(0.97, 1.0, (py - 1536.0) / 384.0);
  vec3 obsZone = OBS * mix(1.0, 0.6, smoothstep(1536.0, 1920.0, py));
  col = mix(col, obsZone, a);

  o = vec4(clamp(col, 0.0, 1.0), 1.0);
}`;

// ============================================================
// 5. WebGL2 初始化与资源加载
// ============================================================
const params = new URLSearchParams(location.search);
const RENDER_MODE = params.get("render") === "1" || params.get("capture") === "1";
if (RENDER_MODE) document.body.classList.add("render");

const canvas = document.getElementById("c");
const statusEl = document.getElementById("status");
const gl = canvas.getContext("webgl2", {
  antialias: false,
  alpha: false,
  preserveDrawingBuffer: true,
  premultipliedAlpha: false,
});
if (!gl) throw new Error("当前环境不支持 WebGL2");

function compile(type, src) {
  const sh = gl.createShader(type);
  gl.shaderSource(sh, src);
  gl.compileShader(sh);
  if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(sh));
  }
  return sh;
}
function program(vs, fs) {
  const p = gl.createProgram();
  gl.attachShader(p, compile(gl.VERTEX_SHADER, vs));
  gl.attachShader(p, compile(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
    throw new Error(gl.getProgramInfoLog(p));
  }
  p._loc = {};
  return p;
}
function loc(p, name) {
  if (!(name in p._loc)) p._loc[name] = gl.getUniformLocation(p, name);
  return p._loc[name];
}
function setU(p, name, ...v) {
  const l = loc(p, name);
  if (l === null) return;
  if (v.length === 1) gl.uniform1f(l, v[0]);
  else if (v.length === 2) gl.uniform2f(l, v[0], v[1]);
  else if (v.length === 3) gl.uniform3f(l, v[0], v[1], v[2]);
  else gl.uniform4f(l, v[0], v[1], v[2], v[3]);
}
function setI(p, name, i) {
  const l = loc(p, name);
  if (l !== null) gl.uniform1i(l, i);
}

const progScene = program(VS_QUAD, FS_SCENE);
const progPart  = program(VS_PART, FS_PART);
const progPost  = program(VS_QUAD, FS_POST);

const quadVAO = gl.createVertexArray();
gl.bindVertexArray(quadVAO);
const quadBuf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
gl.enableVertexAttribArray(0);
gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

const rng = mulberry32(CONFIG.seed);
const totalParticles = CONFIG.counts.reduce((a, b) => a + b, 0);
const partData = new Float32Array(totalParticles * 5);
let pi = 0;
CONFIG.counts.forEach((n, kind) => {
  for (let i = 0; i < n; i++) {
    partData[pi++] = rng();
    partData[pi++] = rng();
    partData[pi++] = rng();
    partData[pi++] = rng();
    partData[pi++] = kind;
  }
});
const partVAO = gl.createVertexArray();
gl.bindVertexArray(partVAO);
const partBuf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, partBuf);
gl.bufferData(gl.ARRAY_BUFFER, partData, gl.STATIC_DRAW);
gl.enableVertexAttribArray(0);
gl.vertexAttribPointer(0, 4, gl.FLOAT, false, 20, 0);
gl.enableVertexAttribArray(1);
gl.vertexAttribPointer(1, 1, gl.FLOAT, false, 20, 16);
gl.bindVertexArray(null);

const sceneTex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, sceneTex);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, W, H, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
const fbo = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, sceneTex, 0);
gl.bindFramebuffer(gl.FRAMEBUFFER, null);

function loadImage(src) {
  return new Promise((resolve) => {
    const im = new Image();
    im.onload = () => resolve(im);
    im.onerror = () => resolve(null);
    im.src = src;
  });
}
function uploadTexture(source) {
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, source);
  gl.generateMipmap(gl.TEXTURE_2D);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  return tex;
}

const textures = [];
for (let i = 0; i < 8; i++) {
  const img = await loadImage(CONFIG.plates[i]);
  if (!img) throw new Error("缺少镜头素材: " + CONFIG.plates[i]);
  textures.push(uploadTexture(img));
}
statusEl.textContent = "8个电影级镜头资产加载完毕 · Clean Feed v3";

// ============================================================
// 6. 逐帧渲染与质检
// ============================================================
const qcFailures = [];
const qcBuf = new Uint8Array(W * 384 * 4);

function renderFrame(f) {
  const s = frameState(f);

  gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
  gl.viewport(0, 0, W, H);
  gl.disable(gl.BLEND);
  gl.useProgram(progScene);

  for (let i = 0; i < 8; i++) {
    gl.activeTexture(gl.TEXTURE0 + i);
    gl.bindTexture(gl.TEXTURE_2D, textures[i]);
    setI(progScene, "uT" + i, i);
    setU(progScene, "uCam" + i, ...s.cams[i]);
  }
  const uWLoc = loc(progScene, "uW[0]");
  if (uWLoc !== null) gl.uniform1fv(uWLoc, s.w);

  setU(progScene, "uTime", s.pt);
  setU(progScene, "uLight", s.light);
  setU(progScene, "uRadius", s.radius);
  setU(progScene, "uShockOn", s.shockOn);
  setU(progScene, "uDawn", s.dawn);

  gl.bindVertexArray(quadVAO);
  gl.drawArrays(gl.TRIANGLES, 0, 3);

  // 粒子系统
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
  gl.useProgram(progPart);
  setU(progPart, "uPT", s.pt);
  setU(progPart, "uBurstAge", s.burstAge);
  setU(progPart, "uDawn", s.dawn);
  setU(progPart, "uBurst", CONFIG.burst[0], CONFIG.burst[1]);
  setU(progPart, "uFissure", CONFIG.fissure[0], CONFIG.fissure[1]);
  const uWPartLoc = loc(progPart, "uW[0]");
  if (uWPartLoc !== null) gl.uniform1fv(uWPartLoc, s.w);

  gl.bindVertexArray(partVAO);
  gl.drawArrays(gl.POINTS, 0, totalParticles);
  gl.disable(gl.BLEND);

  // 后期合成与安全区压暗
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  gl.viewport(0, 0, W, H);
  gl.useProgram(progPost);
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, sceneTex);
  setI(progPost, "uScene", 0);
  setU(progPost, "uTime", s.pt);
  setU(progPost, "uFrame", f);
  setU(progPost, "uShockAge", s.shockAge);
  setU(progPost, "uShockOn", s.shockOn);
  setU(progPost, "uRadius", s.radius);
  setU(progPost, "uRays", s.rays);
  setU(progPost, "uFlash", s.flash);
  setU(progPost, "uFade", s.fade);
  setU(progPost, "uVig", s.vig);
  setU(progPost, "uCA", s.ca);
  setU(progPost, "uGrain", s.grain);
  setU(progPost, "uBurst", CONFIG.burst[0], CONFIG.burst[1]);
  setU(progPost, "uSun", CONFIG.sun[0], CONFIG.sun[1]);

  gl.bindVertexArray(quadVAO);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
  gl.bindVertexArray(null);

  if (f % 30 === 0) {
    gl.readPixels(0, 0, W, 384, gl.RGBA, gl.UNSIGNED_BYTE, qcBuf);
    let maxLum = 0;
    for (let i = 0; i < qcBuf.length; i += 4) {
      const l = (0.2126 * qcBuf[i] + 0.7152 * qcBuf[i + 1] + 0.0722 * qcBuf[i + 2]) / 255;
      if (l > maxLum) maxLum = l;
    }
    if (maxLum >= 0.08) qcFailures.push({ frame: f, maxLum });
  }
}

// 导出对外 API
window.renderFrame = (arg) => {
  const f = (typeof arg === "number" && arg > 0 && arg < 60 && !Number.isInteger(arg)) ? Math.round(arg * FPS) : (arg | 0);
  renderFrame(Math.max(0, Math.min(TOTAL - 1, f)));
};
window.__renderFrame = (n) => {
  renderFrame(Math.max(0, Math.min(TOTAL - 1, n | 0)));
  return canvas.toDataURL("image/png");
};
window.__qcReport = () => ({
  episode: "EP01",
  totalFrames: TOTAL,
  burstFrame: Math.round(BURST_T * FPS),
  cleanZone: "Y >= 1536",
  pass: qcFailures.length === 0,
  failures: qcFailures,
});

// 预览播放器
const playBtn = document.getElementById("play");
const scrub = document.getElementById("scrub");
const frameInfo = document.getElementById("frameInfo");
let playing = false;
let startPerf = 0;
let startFrame = 0;
let lastFrame = -1;

function show(f) {
  if (f === lastFrame) return;
  lastFrame = f;
  renderFrame(f);
  scrub.value = String(f);
  frameInfo.textContent = `f ${f} / ${(f / FPS).toFixed(2)}s`;
}
function tick(now) {
  if (!playing) return;
  const f = (startFrame + Math.floor(((now - startPerf) / 1000) * FPS)) % TOTAL;
  show(f);
  requestAnimationFrame(tick);
}
playBtn.addEventListener("click", () => {
  playing = !playing;
  playBtn.textContent = playing ? "❚❚ 暂停" : "▶ 播放";
  if (playing) {
    startPerf = performance.now();
    startFrame = lastFrame < 0 ? 0 : lastFrame;
    requestAnimationFrame(tick);
  }
});
scrub.addEventListener("input", () => {
  playing = false;
  playBtn.textContent = "▶ 播放";
  show(Number(scrub.value));
});
window.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    playBtn.click();
  }
});

show(0);
window.__ready = true;
</script>
</body>
</html>
'''

with open("/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus/index.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("✓ Updated index.html with 8-shot multi-camera cinematic pipeline")
