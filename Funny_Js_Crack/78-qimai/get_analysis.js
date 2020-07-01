function v(nn) {

			function n(t) {

				function a(t, e, n) {
	                if (!(a.TYPED_ARRAY_SUPPORT || this instanceof a))
	                    return new a(t,e,n);
	                if ("number" == typeof t) {
	                    if ("string" == typeof e)
	                        throw new Error("If encoding is specified then the first argument must be a string");
	                    return c(this, t)
	                }
	                return s(this, t, e, n)
	            }

	            a.from = function(t, e, n) {

	            	function s(t, e, n, i) {

	            		function d(t, e, n) {
	            			isEncoding = function(t) {
				                switch (String(t).toLowerCase()) {
				                case "hex":
				                case "utf8":
				                case "utf-8":
				                case "ascii":
				                case "latin1":
				                case "binary":
				                case "base64":
				                case "ucs2":
				                case "ucs-2":
				                case "utf16le":
				                case "utf-16le":
				                    return !0;
				                default:
				                    return !1
				                }
				            }

				            function q(t, e) {
				                e = e || 1 / 0;
				                for (var n, i = t.length, r = null, o = [], a = 0; a < i; ++a) {
				                    if ((n = t.charCodeAt(a)) > 55295 && n < 57344) {
				                        if (!r) {
				                            if (n > 56319) {
				                                (e -= 3) > -1 && o.push(239, 191, 189);
				                                continue
				                            }
				                            if (a + 1 === i) {
				                                (e -= 3) > -1 && o.push(239, 191, 189);
				                                continue
				                            }
				                            r = n;
				                            continue
				                        }
				                        if (n < 56320) {
				                            (e -= 3) > -1 && o.push(239, 191, 189),
				                            r = n;
				                            continue
				                        }
				                        n = 65536 + (r - 55296 << 10 | n - 56320)
				                    } else
				                        r && (e -= 3) > -1 && o.push(239, 191, 189);
				                    if (r = null,
				                    n < 128) {
				                        if ((e -= 1) < 0)
				                            break;
				                        o.push(n)
				                    } else if (n < 2048) {
				                        if ((e -= 2) < 0)
				                            break;
				                        o.push(n >> 6 | 192, 63 & n | 128)
				                    } else if (n < 65536) {
				                        if ((e -= 3) < 0)
				                            break;
				                        o.push(n >> 12 | 224, n >> 6 & 63 | 128, 63 & n | 128)
				                    } else {
				                        if (!(n < 1114112))
				                            throw new Error("Invalid code point");
				                        if ((e -= 4) < 0)
				                            break;
				                        o.push(n >> 18 | 240, n >> 12 & 63 | 128, n >> 6 & 63 | 128, 63 & n | 128)
				                    }
				                }
				                return o
				            }

				            function m(t, e) {
				                if ("undefined" != typeof ArrayBuffer && "function" == typeof ArrayBuffer.isView && (ArrayBuffer.isView(t) || t instanceof ArrayBuffer))
				                    return t.byteLength;
				                "string" != typeof t && (t = "" + t);
				                var n = t.length;
				                if (0 === n)
				                    return 0;
				                for (var i = !1; ; )
				                    switch (e) {
				                    case "ascii":
				                    case "latin1":
				                    case "binary":
				                        return n;
				                    case "utf8":
				                    case "utf-8":
				                    case void 0:
				                        return q(t).length;
				                    case "ucs2":
				                    case "ucs-2":
				                    case "utf16le":
				                    case "utf-16le":
				                        return 2 * n;
				                    case "hex":
				                        return n >>> 1;
				                    case "base64":
				                        return Y(t).length;
				                    default:
				                        if (i)
				                            return q(t).length;
				                        e = ("" + e).toLowerCase(),
				                        i = !0
				                    }
				            }

				            function o(t, e) {
				                if (2147483647 < e)
				                    throw new RangeError("Invalid typed array length");
				                return true ? (t = new Uint8Array(e),
				                t.__proto__ = a.prototype) : (null === t && (t = new a(e)),
				                t.length = e),
				                t
				            }

				            write = function(t, e, n, i) {

				            	function G(t) {
					                for (var e = [], n = 0; n < t.length; ++n)
					                    e.push(255 & t.charCodeAt(n));
					                return e
					            }

				            	function X(t, e, n, i) {
					                for (var r = 0; r < i && !(r + n >= e.length || r >= t.length); ++r)
					                    e[r + n] = t[r];
					                return r
					            }

				            	function M(t, e, n, i) {
					                return X(G(e), t, n, i)
					            }

				            	function C(t, e, n, i) {
					                return M(t, e, n, i)
					            }


				            	this.length = (function(obj){
				            		 var i = 0;
						            for(var j in obj){
						                if(j != undefined){
						                    i++;
						                }
						            }
						            return i;
				            	})(this);

				                if (void 0 === e)
				                    i = "utf8",
				                    n = this.length,
				                    e = 0;
				                else if (void 0 === n && "string" == typeof e)
				                    i = e,
				                    n = this.length,
				                    e = 0;
				                else {
				                    if (!isFinite(e))
				                        throw new Error("Buffer.write(string, encoding, offset[, length]) is no longer supported");
				                    e |= 0,
				                    isFinite(n) ? (n |= 0,
				                    void 0 === i && (i = "utf8")) : (i = n,
				                    n = void 0)
				                }
				                var r = this.length - e;
				                if ((void 0 === n || n > r) && (n = r),
				                t.length > 0 && (n < 0 || e < 0) || e > this.length)
				                    throw new RangeError("Attempt to write outside buffer bounds");
				                i || (i = "utf8");
				                for (var o = !1; ; )
				                    switch (i) {
				                    case "hex":
				                        return w(this, t, e, n);
				                    case "utf8":
				                    case "utf-8":
				                        return S(this, t, e, n);
				                    case "ascii":
				                        return M(this, t, e, n);
				                    case "latin1":
				                    case "binary":
				                        return C(this, t, e, n);
				                    case "base64":
				                        return T(this, t, e, n);
				                    case "ucs2":
				                    case "ucs-2":
				                    case "utf16le":
				                    case "utf-16le":
				                        return P(this, t, e, n);
				                    default:
				                        if (o)
				                            throw new TypeError("Unknown encoding: " + i);
				                        i = ("" + i).toLowerCase(),
				                        o = !0
				                    }
				            }


			                if ("string" == typeof n && "" !== n || (n = "utf8"),
			                !isEncoding(n))
			                    throw new TypeError('"encoding" must be a valid string encoding');
			                var i = 0 | m(e, n);
			                t = o(t, i);
			                var r = write.bind(t)(e, n);
			                return r !== i && (t = Array.prototype.slice.bind(t)(0, r)),
			                t
			            }


		                if ("number" == typeof e)
		                    throw new TypeError('"value" argument must not be a number');
		                return "undefined" != typeof ArrayBuffer && e instanceof ArrayBuffer ? f(t, e, n, i) : "string" == typeof e ? d(t, e, n) : p(t, e)
		            }


	                return s(null, t, e, n)
	            }


	            function arrToStr() {
	            	function fromByteArray(t) {
	            		var u = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","+","/"]


	            		function aa(t) {

				            return u[t >> 18 & 63] + u[t >> 12 & 63] + u[t >> 6 & 63] + u[63 & t]
				        }


	            		function s(t, e, n) {
				            for (var i, r = [], o = e; o < n; o += 3)
				                i = (t[o] << 16 & 16711680) + (t[o + 1] << 8 & 65280) + (255 & t[o + 2]),
				                r.push(aa(i));
				            return r.join("")
				        }



			            for (var e, n = t.length, i = n % 3, r = "", o = [], a = 16383, l = 0, c = n - i; l < c; l += a)
			                o.push(s(t, l, l + a > c ? c : l + a));
			            return 1 === i ? (e = t[n - 1],
			            r += u[e >> 2],
			            r += u[e << 4 & 63],
			            r += "==") : 2 === i && (e = (t[n - 2] << 8) + t[n - 1],
			            r += u[e >> 10],
			            r += u[e >> 4 & 63],
			            r += u[e << 2 & 63],
			            r += "="),
			            o.push(r),
			            o.join("")
			        }


	            	function k(t, e, n) {
		                return 0 === e && n === t.length ? fromByteArray(t) :fromByteArray(t.slice(e, n))
		            }


	            	function y(t, e, n) {
		                var i = !1;
		                if ((void 0 === e || e < 0) && (e = 0),
		                e > this.length)
		                    return "";
		                if ((void 0 === n || n > this.length) && (n = this.length),
		                n <= 0)
		                    return "";
		                if (n >>>= 0,
		                e >>>= 0,
		                n <= e)
		                    return "";
		                for (t || (t = "utf8"); ; )
		                    switch (t) {
		                    case "hex":
		                        return L(this, e, n);
		                    case "utf8":
		                    case "utf-8":
		                        return O(this, e, n);
		                    case "ascii":
		                        return D(this, e, n);
		                    case "latin1":
		                    case "binary":
		                        return I(this, e, n);
		                    case "base64":
		                        return k(this, e, n);
		                    case "ucs2":
		                    case "ucs-2":
		                    case "utf16le":
		                    case "utf-16le":
		                        return E(this, e, n);
		                    default:
		                        if (i)
		                            throw new TypeError("Unknown encoding: " + t);
		                        t = (t + "").toLowerCase(),
		                        i = !0
		                    }
		            }


	                var t = 0 | this.length;
	                return 0 === t ? "" : 0 === arguments.length ? O(this, 0, t) : y.apply(this, arguments)
	            }


                    var n;
                    return n = t instanceof a ? t : a.from(t.toString(), "binary"),n.arrToStr=arrToStr,
                    n.arrToStr("base64")
                }

            function m(n) {
                    var t = "fromCharCode";
                    return String[t](n)
                }

            return n(encodeURIComponent(nn)["replace"](/%([0-9A-F]{2})/g, function(a, n) {
                return m("0x" + n)
            }))
        }


        function k(a, n) {

        	function m(n) {
                    var t = "fromCharCode";
                    return String[t](n)
                }

            n || (n = s()),
            a = a["split"]("");
            for (var t = a["length"], e = n["length"], r = "charCodeAt", i = 0; i < t; i++)
                a[i] = m(a[i][r](0) ^ n[(i + 10) % e][r](0));
            return a["join"]("")
        }

		function get_analysis(url, params){
			var g = {
				'difftime': -1302
			}
			var n = {
				"params":params
			}
            var e = +new Date - (g['difftime'] ? g['difftime'] : 0) - 1515125653845
              , r = ""
              , m = [];
            return void 0 === n["params"] && (n["params"] = {}),
            Object.keys(n["params"])["forEach"](function(a) {
                if (a == "analysis")
                    return !S;
                n["params"]["hasOwnProperty"](a) && m["push"](n["params"][a])
            }),
            m = m['sort']()["join"](""),
            m = Object(v)(m),
            m += "@#" + url.replace("https://api.qimai.cn", ""),  // 每个排行榜的参数不一样
            m += "@#" + e,
            m += "@#" + 1,
            r = Object(v)(Object(k)(m, "00000008d78d46a"))
            return r;
		}