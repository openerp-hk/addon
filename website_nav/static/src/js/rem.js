(function (doc, win) {
    // if (window.screen.width > 880) {
    //     var oMeta = document.createElement('meta');
    //     oMeta.content = 'target-densitydpi=device-dpi, width=device-width, initial-scale=0.5, minimum-scale=0.1, maximum-scale=0.5, user-scalable=yes';
    //     oMeta.name = 'viewport';
    //     document.getElementsByTagName('head')[0].appendChild(oMeta);
    //     return false
    // }
    var docEl = doc.documentElement,
        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
        recalc = function () {
            var clientWidth = docEl.clientWidth;
            if (!clientWidth) return;
            if (clientWidth >= 750) {
                docEl.style.fontSize = '100px';
            } else {
                docEl.style.fontSize = 100 * (clientWidth / 750) + 'px';
            }
        };
    if (!doc.addEventListener) return;
    win.addEventListener(resizeEvt, recalc, false);
    doc.addEventListener('DOMContentLoaded', recalc, false);
})(document, window);
