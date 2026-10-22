/* CameraRig —— 全片共享一台摄像机。
 *
 * 为什么不用整页 scale()：
 *   物体缩小、场景拉远、摄像机后移是三件不同的事。
 *   scale(0.7) 把主体比例、纹理密度、元素间距、视差全部等比缩放，
 *   看起来像"缩小了一张图片"，而不是镜头后移。
 *
 * 真正的后移 = 所有元素的 z 增加。近的缩得快、远的缩得慢，视差自然产生。
 */
(function (global) {
  "use strict";

  function CameraRig(opts) {
    opts = opts || {};
    this.focal = opts.focal != null ? opts.focal : 1200; // 焦距，越大透视越弱
    this.cx = opts.cx != null ? opts.cx : 960; // 灭点 x
    this.cy = opts.cy != null ? opts.cy : 540; // 灭点 y
    this.z = opts.z != null ? opts.z : 0; // 摄像机位置，增大 = 后移
  }

  /**
   * 世界坐标 -> 屏幕坐标
   * @returns {{x:number, y:number, scale:number, depth:number}}
   *   scale 用来驱动该元素的大小；depth 可用于景深、雾气、排序
   */
  CameraRig.prototype.project = function (x, y, z) {
    var depth = z + this.focal + this.z;
    if (depth <= 1) depth = 1; // 防止穿过摄像机时炸掉
    var s = this.focal / depth;
    return {
      x: this.cx + x * s,
      y: this.cy - y * s,
      scale: s,
      depth: depth
    };
  };

  /** 后移 dz（正数远离画面）。放进 GSAP 时间轴驱动即可得到真实推拉。 */
  CameraRig.prototype.dolly = function (dz) {
    this.z += dz;
    return this;
  };

  /** 供 GSAP 直接 tween 的对象：gsap.to(cam, { z: 800, duration: 2 }) */
  CameraRig.prototype.state = function () {
    return { focal: this.focal, cx: this.cx, cy: this.cy, z: this.z };
  };

  global.HF = global.HF || {};
  global.HF.CameraRig = CameraRig;
})(window);
