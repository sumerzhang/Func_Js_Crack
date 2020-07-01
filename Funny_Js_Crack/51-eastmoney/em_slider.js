var o = {
    copy: function (n, e) {
        var t = e || {};
        for (var r in n)
            t[r] = n[r];
        return t
    },
    toParam: function (n) {
        var e = [];
        for (var t in n)
            if (n.hasOwnProperty(t)) {
                var r = typeof n[t];
                "number" !== r && "string" !== r && "boolean" !== r || e.push(t + "=" + n[t])
            }
        return e.join("&")
    },
    isFunction: function (n) {
        return "function" == typeof n
    },
    random: function () {
        return parseInt(1e4 * Math.random()) + (new Date).valueOf()
    },
    inArray: function (n, e) {
        for (var t = 0; t < e.length; t++)
            if (e[t] == n)
                return t;
        return -1
    },
    removeProperty: function (n, e) {
        n[e] = void 0;
        try {
            delete n[e]
        } catch (n) {
        }
    },
    slice: function (n, e) {
        return n.slice(e)
    },
    arrayEqual: function (n, e) {
        if (n === e)
            return !0;
        if (null == n || null == e)
            return !1;
        if (n.length != e.length)
            return !1;
        for (var t = 0; t < n.length; t++)
            if (n[t] !== e[t])
                return !1;
        return !0
    },
    diff: function (n, e) {
        for (var t = [], r = 0; r < n.length; r++)
            t.push(n[r] - e[r]);
        return t
    },
    isArray: function (n) {
        return Array.isArray ? Array.isArray(n) : "[object Array]" === Object.prototype.toString.call(n)
    },
    log: function (n) {
        try {
            console && console.log(n)
        } catch (n) {
        }
    }
};

o.Utility = {
    map: function (n, e) {
        var t;
        if (o.isArray(n)) {
            t = [];
            for (var r = 0; r < n.length; r++)
                t[r] = e(r, n[r])
        } else
            for (var i in t = {},
                n)
                n.hasOwnProperty(i) && (t[i] = e(i, n[i]));
        return t
    },
    getLength: function (n) {
        var e = 0;
        if (o.isArray(n))
            e = n.length;
        else
            for (var t in n)
                n.hasOwnProperty(t) && (e += 1);
        return e
    }
};

o.base64Encode = function (n) {
    // if (window.btoa)
    //     return window.btoa(n);
    var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".split("");
    return function (n) {
        var t, r, i, o, a, s, c;
        for (r = i = 0,
                 o = n.length,
                 s = (o -= a = o % 3) / 3 << 2,
             a > 0 && (s += 4),
                 t = new Array(s); r < o;)
            c = n.charCodeAt(r++) << 16 | n.charCodeAt(r++) << 8 | n.charCodeAt(r++),
                t[i++] = e[c >> 18] + e[c >> 12 & 63] + e[c >> 6 & 63] + e[63 & c];
        return 1 == a ? (c = n.charCodeAt(r++),
            t[i++] = e[c >> 2] + e[(3 & c) << 4] + "==") : 2 == a && (c = n.charCodeAt(r++) << 8 | n.charCodeAt(r++),
            t[i++] = e[c >> 10] + e[c >> 4 & 63] + e[(15 & c) << 2] + "="),
            t.join("")
    }(n)
};

o.encrypt = function (n) {
    var e, t = 2654435769, r = "e98ae8878c264a7e";

    function i(n) {
        if (/^[\x00-\x7f]*$/.test(n))
            return n;
        for (var e = [], t = n.length, r = 0, i = 0; r < t; ++r,
            ++i) {
            var o = n.charCodeAt(r);
            if (o < 128)
                e[i] = n.charAt(r);
            else if (o < 2048)
                e[i] = String.fromCharCode(192 | o >> 6, 128 | 63 & o);
            else {
                if (!(o < 55296 || o > 57343)) {
                    if (r + 1 < t) {
                        var a = n.charCodeAt(r + 1);
                        if (o < 56320 && 56320 <= a && a <= 57343) {
                            var s = 65536 + ((1023 & o) << 10 | 1023 & a);
                            e[i] = String.fromCharCode(240 | s >> 18 & 63, 128 | s >> 12 & 63, 128 | s >> 6 & 63, 128 | 63 & s),
                                ++r;
                            continue
                        }
                    }
                    throw new Error("Malformed string")
                }
                e[i] = String.fromCharCode(224 | o >> 12, 128 | o >> 6 & 63, 128 | 63 & o)
            }
        }
        return e.join("")
    }

    function o(n) {
        return 4294967295 & n
    }

    function a(n, e, t, r, i, o) {
        return (t >>> 5 ^ e << 2) + (e >>> 3 ^ t << 4) ^ (n ^ e) + (o[3 & r ^ i] ^ t)
    }

    function s(n, e) {
        var t, r = n.length, i = r >> 2;
        0 != (3 & r) && ++i,
            e ? (t = new Array(i + 1))[i] = r : t = new Array(i);
        for (var o = 0; o < r; ++o)
            t[o >> 2] |= n.charCodeAt(o) << ((3 & o) << 3);
        return t
    }

    return null == n || 0 === n.length ? n : (n = i(n),
        r = i(r),
        function (n, e) {
            var t = n.length
                , r = t << 2;
            if (e) {
                var i = n[t - 1];
                if (i < (r -= 4) - 3 || i > r)
                    return null;
                r = i
            }
            for (var o = 0; o < t; o++)
                n[o] = String.fromCharCode(255 & n[o], n[o] >>> 8 & 255, n[o] >>> 16 & 255, n[o] >>> 24 & 255);
            var a = n.join("");
            return e ? a.substring(0, r) : a
        }(function (n, e) {
            var r, i, s, c, d, l, u = n.length, p = u - 1;
            for (i = n[p],
                     s = 0,
                     l = 0 | Math.floor(6 + 52 / u); l > 0; --l) {
                for (c = (s = o(s + t)) >>> 2 & 3,
                         d = 0; d < p; ++d)
                    r = n[d + 1],
                        i = n[d] = o(n[d] + a(s, r, i, d, c, e));
                r = n[0],
                    i = n[p] = o(n[p] + a(s, r, i, p, c, e))
            }
            return n
        }(s(n, !0), ((e = s(r, !1)).length < 4 && (e.length = 4),
            e)), !1))
};

o.Guid = function () {
    return "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, function (n) {
        var e = 16 * Math.random() | 0;
        return ("x" == n ? e : 3 & e | 8).toString(16)
    })
};

function encrypt(data) {
    return o.base64Encode(o.encrypt(data))
};

console.log(encrypt("appid=201802274651|ctxid=cf7eff26ecf7b586f3e035c723ddb529|a=18829040039|p=snsxusix|r=0.10322408746010114"));


function getMergeArray() {
    var a = function() {
        for (var n, e = "6_11_7_10_4_12_3_1_0_5_2_9_8".split("_"), t = [], r = 0; r < 52; r++)
            n = 2 * parseInt(e[parseInt(r % 26 / 2)]) + r % 2,
            parseInt(r / 2) % 2 || (n += r % 2 ? -1 : 1),
                n += r < 26 ? 26 : 0,
                t.push(n);
        return t
    }();
    var merge_array = [];
    for (var d = 0, l = a.length; d < l; d++) {
        merge_array.push({
            left: (a[d] % 26 * 12 + 1),
            top: (a[d] <= 25 ? (0 - "160") / 2 : 0)
        })
    }
    return merge_array
}

console.log(getMergeArray());
