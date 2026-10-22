/* 资产加载器。
 *
 * 渲染器会 seek 到任意时刻再截图。图片如果在截图之后才到，成片里就是一个空帧，
 * 而且预览时看不出来。所以所有图必须在首次绘制前 decode 完成。
 *
 * 绝对不要在 img.onload 里触发重绘 —— 那是轮询式写法，会被确定性检查拦下。
 */
(function (global) {
  "use strict";

  var images = Object.create(null);

  /**
   * @param {Object<string,string>} manifest  { key: 路径 }
   * @returns {Promise<Object<string,HTMLImageElement>>}
   */
  function loadImages(manifest) {
    var keys = Object.keys(manifest || {});
    return Promise.all(
      keys.map(function (key) {
        var img = new Image();
        img.src = manifest[key];
        // decode() 在位图真正可绘制时才 resolve，比 onload 更严格
        return img.decode().then(
          function () {
            images[key] = img;
          },
          function (err) {
            console.error("[HF] 图片加载失败：" + manifest[key], err);
            throw err;
          }
        );
      })
    ).then(function () {
      return images;
    });
  }

  /** 取一张已加载的图；没加载过直接抛错，不静默返回 undefined */
  function img(key) {
    var found = images[key];
    if (!found) throw new Error("[HF] 图片未加载：" + key + "（是否漏在 manifest 里？）");
    return found;
  }

  global.HF = global.HF || {};
  global.HF.loadImages = loadImages;
  global.HF.img = img;
  global.HF.images = images;
})(window);
