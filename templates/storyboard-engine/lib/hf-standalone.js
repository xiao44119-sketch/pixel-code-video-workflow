/* 单镜头入口支撑。
 *
 * 分组合成文件把所有内容放在 <template> 里（挂载到总时间线时，<head> 会被丢弃）。
 * 直接在浏览器打开这个文件时 <template> 不会渲染，所以这里把它的内容克隆进 body。
 *
 * 这个脚本只在 <head> 里引入 —— 挂载到总时间线时 <head> 被丢弃，它不会执行，
 * 因此不会影响成片。
 */
(function () {
  "use strict";

  function boot() {
    var tpl = document.querySelector("body > template");
    if (!tpl) return;

    var frag = tpl.content.cloneNode(true);

    // 克隆出来的 <script> 不会执行，必须重建。
    var scripts = [];
    Array.prototype.forEach.call(frag.querySelectorAll("script"), function (old) {
      scripts.push(old);
      old.parentNode.removeChild(old);
    });

    document.body.appendChild(frag);

    scripts.forEach(function (old) {
      var s = document.createElement("script");
      Array.prototype.forEach.call(old.attributes, function (a) {
        s.setAttribute(a.name, a.value);
      });
      s.textContent = old.textContent;
      document.body.appendChild(s);
    });

    document.documentElement.setAttribute("data-hf-standalone", "1");
    window.__hfStandalone = true;
    document.dispatchEvent(new Event("hf:standalone-ready"));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
