# 金门大桥测试任务 Prompt

完整Prompt，直接复制使用：

```
Objective
Build a visually stunning, high-fidelity 3D voxel-style simulation of the Golden Gate Bridge in Three.js.
Prioritize complex visuals (not simple blocks), strong atmosphere depth, and smooth ~60FPS.

Visuals & Atmosphere
- Lighting: a Time-of-day slider (0–24h) that controls sun position, intensity, sky color, and fog tint.
- Fog: volumetric-feeling fog using lightweight sprite particles; slider 0–100 (0 = crystal clear, 100 = dense but not pure whiteout).
- Water: custom shader for waves + specular reflections; blend horizon with distance-based fog (exp2) so the far water merges naturally.
- Post: ACES filmic tone mapping + optimized bloom (night lights glow but keep performance).

Scene Details
- Bridge: recognizable art-deco towers, main span cables + suspenders, piers/anchors consistent with suspension bridge structure.
- Terrain: simple but convincing Marin Headlands + SF side peninsula silhouettes.
- Skyline: procedural/instanced city blocks on the SF side to suggest depth.
- Traffic: up to ~400 cars via InstancedMesh, properly aligned on the deck (avoid clipping). Headlights/taillights emissive at night.
- Ships: a few procedural cargo ships with navigation lights moving across the bay.
- Nature: a small flock of animated birds (lightweight flocking).

Night Mode
At night, enable city lights, bridge beacons, street lights, vehicle lights, ship nav lights.

Tech & Controls (Important)
- Output MUST be a single self-contained HTML file (e.g., golden_gate_bridge.html) that runs by opening in Chrome.
- No build tools (no Vite/Webpack). Pure HTML + JS.
- Import Three.js and addons via CDN using ES Modules + importmap.
- UI: nice-looking sliders for Time (0–24), Fog Density (0–100), Traffic Density (0–100), Camera Zoom.
- Optimization: use InstancedMesh for repeated items (cars/lights/birds), avoid heavy geometry, keep draw calls low.
```

## 评估维度

| 维度 | 考察点 | 评分标准 |
|------|--------|----------|
| 一次成功率 | 能否无修改运行 | 是/需1次修复/需多次修复/失败 |
| 视觉细节 | 桥塔、缆绳、车辆 | 精细/一般/粗糙 |
| 交互体验 | 滑块、缩放、旋转 | 流畅/卡顿/不可用 |
| 性能 | 帧率、内存 | 60FPS/30FPS/卡顿 |
| 代码质量 | 可读性、模块化 | 优/良/差 |

## 已知表现

| 模型 | 一次成功 | 视觉 | 性能 | 备注 |
|------|----------|------|------|------|
| GPT-5.2-Codex | ✅ | 精细 | 60FPS | 综合最佳 |
| Gemini 3 Pro | ✅ | 精细 | 60FPS | 前端强项 |
| Claude Opus 4.5 | 需1次修复 | 一般 | 60FPS | 需评审后优化 |
| GLM-4.7 | 需多次修复 | 一般 | 卡顿 | 国产中较好 |
