const crypto = require('crypto');

function zN(input) {  
  if (typeof input !== 'string') input = input.toString();
  return crypto.createHash('md5').update(input).digest('hex');
}

const t = {
  stringToBytes: function(str) {
    return new Uint8Array(Buffer.from(str, 'utf-8'));
  }
};

const r = {
  stringToBytes: function(str) {
    const bytes = new Uint8Array(str.length);
    for (let i = 0; i < str.length; i++) {
      bytes[i] = str.charCodeAt(i) & 0xff;
    }
    return bytes;
  }
};

function n(obj) {
  return obj instanceof ArrayBuffer ||
         obj instanceof Uint8Array ||
         obj instanceof Uint8ClampedArray ||
         obj instanceof Int8Array ||
         obj instanceof Uint16Array ||
         obj instanceof Int16Array ||
         obj instanceof Uint32Array ||
         obj instanceof Int32Array ||
         obj instanceof Float32Array ||
         obj instanceof Float64Array;
}

const e = {
  bytesToWords: function(bytes) {
    const words = [];
    for (let i = 0, b = 0; i < bytes.length; i++, b += 8) {
      words[b >>> 5] |= bytes[i] << (24 - b % 32);
    }
    return words;
  },
  wordsToBytes: function(words) {
    const bytes = [];
    for (let i = 0; i < words.length * 32; i += 8) {
      bytes.push((words[i >>> 5] >>> (24 - i % 32)) & 0xff);
    }
    return bytes;
  },
  bytesToHex: function(bytes) {
    return Buffer.from(bytes).toString('hex');
  },
  endian: function(words) {
    return words; // little-endian，直接返回
  }
};


function ff(i, s, a, c, l, u, d) {
  var f = i + (s & a | ~s & c) + (l >>> 0) + d;
  return (f << u | f >>> 32 - u) + s;
}

function gg(i, s, a, c, l, u, d) {
  var f = i + (s & c | a & ~c) + (l >>> 0) + d;
  return (f << u | f >>> 32 - u) + s;
}

function hh(i, s, a, c, l, u, d) {
  var f = i + (s ^ a ^ c) + (l >>> 0) + d;
  return (f << u | f >>> 32 - u) + s;
}

function ii(i, s, a, c, l, u, d) {
  var f = i + (a ^ (s | ~c)) + (l >>> 0) + d;
  return (f << u | f >>> 32 - u) + s;
}


function KN(key) {
  const positions = [46,47,18,2,53,8,23,32,15,50,10,31,58,3,45,35,27,43,5,49,33,9,42,19,29,28,14,39,12,38,41,13,37,48,7,16,24,55,40,61,26,17,0,1,60,51,30,4,22,25,54,21,56,59,6,63,57,62,11,36,20,34,44,52];
  let result = '';
  positions.forEach(pos => {
    if (pos < key.length) {
      result += key.charAt(pos);
    }
  });
  return result.slice(0, 32);
}

function YN(config) {
  if (config.useAssignKey) {
    return {
      imgKey: config.wbiImgKey,
      subKey: config.wbiSubKey
    };
  }

  const stored = null; // GN("wbi_img_urls") 返回 null
  const parts = stored ? stored.split("-") : [];
  return {
    imgKey: parts[0] || config.wbiImgKey,
    subKey: parts[1] || config.wbiSubKey
  };
}

function XN(params, config = { wbiImgKey: "", wbiSubKey: "" }) {
  const { imgKey, subKey } = YN(config);
  if (!imgKey || !subKey) return null;

  const mixinKey = KN(imgKey + subKey);
  const wts = Math.round(Date.now() / 1000);

  const fullParams = { ...params, wts };
  const sortedKeys = Object.keys(fullParams).sort();
  const parts = [];

  for (let key of sortedKeys) {
    let value = fullParams[key];
    if (value != null) {
      if (typeof value === "string") {
        value = value.replace(/[!'()*]/g, "");
      }
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
    }
  }

  const query = parts.join("&");
  const toSign = query + mixinKey;
  const w_rid = zN(toSign);

  return {
    w_rid,
    wts: wts.toString()
  };
}

