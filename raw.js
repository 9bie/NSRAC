var i = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/~！@#￥%……&",
a = String.fromCharCode,
o = function(e) {
    if (e.length < 2) {
        var r = e.charCodeAt(0);
        return 128 > r ? e: 2048 > r ? a(192 | r >>> 6) + a(128 | 63 & r) : a(224 | r >>> 12 & 15) + a(128 | r >>> 6 & 63) + a(128 | 63 & r)
    }
    var r = 65536 + 1024 * (e.charCodeAt(0) - 55296) + (e.charCodeAt(1) - 56320);
    return a(240 | r >>> 18 & 7) + a(128 | r >>> 12 & 63) + a(128 | r >>> 6 & 63) + a(128 | 63 & r)
},
u = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g,
c = function(e) {
    return (e + "" + Math.random()).replace(u, o)
},
l = function(e) {
    var r = [0, 2, 1][e.length % 3],
    t = e.charCodeAt(0) << 16 | (e.length > 1 ? e.charCodeAt(1) : 0) << 8 | (e.length > 2 ? e.charCodeAt(2) : 0),
    n = [i.charAt(t >>> 18), i.charAt(t >>> 12 & 63), r >= 2 ? "=": i.charAt(t >>> 6 & 63), r >= 1 ? "=": i.charAt(63 & t)];
    return n.join("")
},
p = function(e) {
    return e.replace(/[\s\S]{1,3}/g, l)
},
d = function() {
    return p(c((new Date).getTime()))
},
g = function(e, r) {
    return r ? d(String(e)).replace(/[+\/]/g,
    function(e) {
        return "+" == e ? "-": "_"
    }).replace(/=/g, "") : d(String(e))
};
n(document).ajaxSend(function(e, r, t) {
    var n = "250528",
    i = g("baiduid"),
    a = 0,
    o = "&channel=chunlei";
    t.appid && (n = t.appid),
    t.clienttype && (a = t.clienttype),
    /channel=channel_web_director/.test(t.url) && (o = ""),
    t.url += /\?/.test(t.url) ? "&bdstoken=" + yunData.MYBDSTOKEN + o + "&web=1&app_id=" + n + "&logid=" + i: "?bdstoken=" + yunData.MYBDSTOKEN + o + "&web=1&app_id=" + n + "&logid=" + i;
    var u = location.pathname;
    "/disk/file-selector" === u && "guanjia" === disk.getParam("frm") || "/mbox/creategroup" === u ? (t.url = t.url.replace(/[\&]clienttype=[^&]*/g, ""), t.url += "&clienttype=8&version=4.9.9.9") : t.url += "&clienttype=" + a
}),
n.extend({
    stringify: function(e) {
        var r = typeof e;
        if ("object" != r || null === e) return "string" == r && (e = '"' + e + '"'),
        String(e);