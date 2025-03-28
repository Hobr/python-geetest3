function Track(track) {
    function n(t) {
        var e = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr";
        var n = e.length;
        var r = "";
        var i = Math.abs(t);
        var o = parseInt(i / n);
        n <= o && (o = n - 1);
        o && (r = e.charAt(o));
        var s = "";
        return t < 0 && (s += "!"),
            r && (s += "$"),
            s + r + e.charAt(i %= n);
    }
    var t = function(t) {
        for (var e, n, r, i = [], o = 0, s = 0, a = t.length - 1; s < a; s++) {
            e = Math.round(t[s + 1][0] - t[s][0]);
            n = Math.round(t[s + 1][1] - t[s][1]);
            r = Math.round(t[s + 1][2] - t[s][2]);
            0 == e && 0 == n && 0 == r || (0 == e && 0 == n ? o += r : (i.push([e, n, r + o]),
                o = 0));
        }
        return 0 !== o && i.push([e, n, o]),
            i;
    }(track);
    var r = [];
    var i = [];
    var o = [];

    return new ct(t)["$_CAE"](function(t) {
            var e = function(t) {
                for (var e = [
                        [1, 0],
                        [2, 0],
                        [1, -1],
                        [1, 1],
                        [0, 1],
                        [0, -1],
                        [3, 0],
                        [2, -1],
                        [2, 1]
                    ], n = 0, r = e.length; n < r; n++)
                    if (t[0] == e[n][0] && t[1] == e[n][1])
                        return "stuvwxyz~" [n];
                return 0;
            }(t);
            e ? i.push(e) : (r.push(n(t[0])),
                i.push(n(t[1])));
            o.push(n(t[2]));
        }),
        r.join("") + "!!" + i.join("") + "!!" + o.join("");
}

function ct(t) {
    this['$_BCAO'] = t || [];
}

ct.prototype = {
    '$_CAE': function(t) {
        var e = this['$_BCAO'];
        if (e.map)
            return new ct(e.map(t));
        for (var n = [], r = 0, i = e.length; r < i; r += 1)
            n[r] = t(e[r], r, this);
        return new ct(n);
    }
}

function AA(t, e, n) {
    if (!e || !n)
        return t;
    var r, i = 0,
        o = t,
        s = e[0],
        a = e[2],
        _ = e[4];
    while (r = n.substr(i, 2)) {
        i += 2;
        var c = parseInt(r, 16),
            u = String.fromCharCode(c),
            l = (s * c * c + a * c + _) % t.length;
        o = o.substr(0, l) + u + o.substr(l);
    }
    return o;
}

t = [
    [-34, -25, 0],
    [0, 0, 0],
    [1, 0, 27],
    [2, 0, 38],
    [3, 0, 43],
    [4, 0, 50],
    [5, 0, 54],
    [6, 0, 60],
    [8, 0, 66],
    [9, 0, 72],
    [11, 0, 77],
    [12, 0, 83],
    [14, 0, 88],
    [16, 0, 94],
    [18, 0, 99],
    [21, 0, 105],
    [25, 0, 111],
    [30, 0, 116],
    [34, 0, 121],
    [38, 0, 127],
    [43, 0, 133],
    [49, 0, 138],
    [53, 0, 143],
    [58, 0, 150],
    [63, -2, 155],
    [68, -2, 161],
    [73, -2, 166],
    [79, -2, 172],
    [81, -2, 177],
    [85, -2, 183],
    [89, -2, 188],
    [91, -2, 193],
    [94, -3, 199],
    [96, -3, 205],
    [98, -3, 210],
    [102, -3, 216],
    [104, -3, 221],
    [107, -3, 227],
    [109, -3, 233],
    [114, -3, 238],
    [118, -3, 244],
    [122, -4, 249],
    [127, -4, 254],
    [132, -4, 260],
    [136, -6, 266],
    [139, -6, 271],
    [141, -7, 276],
    [144, -7, 283],
    [146, -7, 288],
    [147, -7, 294],
    [148, -7, 299],
    [149, -7, 305],
    [150, -7, 310],
    [151, -7, 322],
    [152, -7, 327],
    [153, -7, 339],
    [154, -7, 361],
    [155, -7, 393],
    [156, -7, 399],
    [157, -7, 416],
    [158, -7, 494],
    [159, -7, 505],
    [159, -8, 510],
    [160, -8, 516],
    [161, -8, 522],
    [162, -9, 533],
    [163, -9, 562],
    [163, -9, 769]
]

pre = Track(t)
console.log(pre)
aa = AA(pre, [12, 58, 98, 36, 43, 95, 62, 15, 12], "454c2847");
console.log(aa)
