
require('./env.js')
require('./xhs_code_439.js')
const crypto = require('crypto');
function md5Encrypt(data) {
    return crypto.createHash('md5').update(data).digest('hex');
}

function encodeUtf8(e) {
    for (var a = encodeURIComponent(e), r = [], c = 0; c < a.length; c++) {
        var d = a.charAt(c);
        if ("%" === d) {
            var s = parseInt(a.charAt(c + 1) + a.charAt(c + 2), 16);
            r.push(s),
            c += 2
        } else
            r.push(d.charCodeAt(0))
    }
    return r
}

function base64Encode(param) {
    for (var c = [], d = "ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5", s = 0, f = d.length; s < f; ++s)
    c[s] = d[s];
    function tripletToBase64(e) {
        return c[e >> 18 & 63] + c[e >> 12 & 63] + c[e >> 6 & 63] + c[63 & e]
    }
    function encodeChunk(e, a, r) {
        for (var c, d = [], s = a; s < r; s += 3)
            c = (e[s] << 16 & 0xff0000) + (e[s + 1] << 8 & 65280) + (255 & e[s + 2]),
            d.push(tripletToBase64(c));
        return d.join("")
    }
    function b64Encode(e) {
        for (var a, r = e.length, d = r % 3, s = [], f = 16383, u = 0, l = r - d; u < l; u += f)
            s.push(encodeChunk(e, u, u + f > l ? l : u + f));
        return 1 === d ? (a = e[r - 1],
        s.push(c[a >> 2] + c[a << 4 & 63] + "==")) : 2 === d && (a = (e[r - 2] << 8) + e[r - 1],
        s.push(c[a >> 10] + c[a >> 4 & 63] + c[a << 2 & 63] + "=")),
        s.join("")
    }
    return b64Encode(param)
}


function seccore_signv2(e, a) {
    // try {
    if (typeof a === 'string') {
        a = JSON.parse(a);
    }
    var r = window.toString
      , c = e;
    "[object Object]" === r.call(a) || "[object Array]" === r.call(a) || (void 0 === a ? "undefined" : (0,
    h._)(a)) === "object" && null !== a ? c += JSON.stringify(a) : "string" == typeof a && (c += a);

    var d = md5Encrypt([c].join(""))
      , f = md5Encrypt(e)
      , s = window.mnsv2(c, d, f);
    console.log('c-->', c)
    console.log('d-->', d)
    console.log('s-->', s)
    // s_js = "mns0201_ZytDf1UWmtPNpvdxHpenwoRZ/+QsHLJ/keXJ8rnT1Uyfvte3o20FEeX/so80R6DctWF/OXRE/7WC6aGo4dxXNb9FvM4SbgdZEBSWyeRbs0u/iKqTETWU4d+tSOhuwDsS/mcHjsX6wtvsLp/jcadeBmNLU560GyqcYJOMZi4kdaH="
    // s_console = "mns0301_gRaKquPU/aLBDfToEt0idE5QscSsR85VHgjxYGYI2j5K7I4dVP6koDketD7Qyp4+tJWlcqxt0b6hyQel4uyQRhYAnhhkwC1yOz4C+84xEbz2wq7X9gKA0JHKXSgYL86o1CMCnpsRzRJPUaT3l7FKSndVZlciE0JRIk0OHNRRTMrz2gVFdtd+6n6oXwJUrWtf"
    f = {
        x0: "4.3.9",
        x1: "xhs-pc-web",
        x2: "Windows",
        x3: s,
        x4: a ? void 0 === a ? "undefined" : "object" : "",
        x5: d
    };
    return "XYS_" + (0,
    base64Encode)((0,
    encodeUtf8)(JSON.stringify(f)))
}


url_param = "/api/sns/web/v2/comment/sub/page?note_id=69b532c7000000002102f791&root_comment_id=69b62713000000001500b266&num=10&cursor=69b6316e0000000019002ef5&image_formats=jpg,webp,avif&top_comment_id=&xsec_token=ABRsGRVKYeGhjEPkTJ1i-1NaZ8ZKJ2dMTVujsZ9l8pJVs%3D"
json_data = undefined
x_s = seccore_signv2(url_param, json_data)
console.log('x-s:', x_s.length, x_s)