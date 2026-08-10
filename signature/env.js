window = (function () {
    //定义函数toString
    var v_safe;
    !function () {
        var n = Function.toString, t = [], i = [], o = [].indexOf.bind(t), e = [].push.bind(t), r = [].push.bind(i);

        function u(n, t) {
            return -1 == o(n) && (e(n), r(`function ${t || n.name || ""}() { [native code] }`)), n
        }

        Object.defineProperty(Function.prototype, "toString", {
            enumerable: !1, configurable: !0, writable: !0, value: function () {
                return "function" == typeof this && i[o(this)] || n.call(this)
            }
        }),
            u(Function.prototype.toString, "toString"),
            v_safe = u
    }();

    //定义构造函数父子关系：t-->子构造函数，e-->父构造函数
    function _inherits(t, e) {
        t.prototype = Object.create(e.prototype, {
            constructor: {value: t, writable: !0, configurable: !0}
        }), e && Object.setPrototypeOf(t, e)
    }

    //实例化对象
    var v_new = function (v) {
        var temp = v_new_toggle;
        v_new_toggle = true;
        var r = new v;
        v_new_toggle = temp;
        return r
    }

    Object.defineProperty(Object.prototype, Symbol.toStringTag, {
        get() {
            return Object.getPrototypeOf(this).constructor.name
        }, configurable: true,
    });
    var v_new_toggle = true
    var v_console_log = function () {
        if (!v_new_toggle) {
            console.log.apply(this, arguments)
        }
    }

    // 定义常用基础环境及环境父子构造函数关系
    EventTarget = v_safe(function EventTarget() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    Window = v_safe(function Window() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
        this.outerHeight = 680;
        this.outerWidth = 1280;
    });
    _inherits(Window, EventTarget);
    Screen = v_safe(function Screen() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
        this.availHeight = 680;
        this.availLeft = 0;
        this.availTop = 0;
        this.availWidth = 1280;
        this.colorDepth = 24;
        this.height = 720;
        this.isExtended = false;
        this.pixelDepth = 24;
        this.width = 1280;
    });
    _inherits(Screen, EventTarget);
    Node = v_safe(function Node() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    _inherits(Node, EventTarget);
    Document = v_safe(function Document() {});
    _inherits(Document, Node);
    HTMLDocument = v_safe(function HTMLDocument() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    _inherits(HTMLDocument, Document);
    Element = v_safe(function Element() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    _inherits(Element, Node);
    HTMLElement = v_safe(function HTMLElement() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    _inherits(HTMLElement, Element);
    HTMLHtmlElement = v_safe(function HTMLHtmlElement() {
        this.tagName = 'HTML';
    });
    _inherits(HTMLHtmlElement, HTMLElement);
    Navigator = v_safe(function Navigator() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
        this.appCodeName = "Mozilla";
        this.appName = "Netscape";
        this.appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";
        this.platform = "Win32";
        this.product = "Gecko";
        this.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";
        this.vendor = "Google Inc.";
        this.language = "zh-CN";
        this.languages = ['zh-CN', 'zh'];
        this.webdriver = false;
        this.permissions = v_new(Permissions);
        this.userAgentData = v_new(NavigatorUAData);
    });
    History = v_safe(function History() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        }
        ;
    });
    Location = v_safe(function Location() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
        this.hash = "";
        this.host = "www.xiaohongshu.com";
        this.hostname = "www.xiaohongshu.com";
        this.href = "https://www.xiaohongshu.com/explore";
        this.origin = "https://www.xiaohongshu.com";
        this.pathname = "/explore";
        this.port = "";
        this.protocol = "https:";
    });
    Storage = v_safe(function Storage() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        }
        ;
    });
    HTMLCollection = v_safe(function HTMLCollection() {
        // 创建一个数组来存储元素
        this._elements = [];
        // 使 HTMLCollection 可迭代
        this[Symbol.iterator] = function* () {
            for (let element of this._elements) {
                yield element;
            }
        };
        // 添加 length 属性
        Object.defineProperty(this, 'length', {
            get: function () {
                return this._elements.length;
            }
        });
        // 添加 item 方法
        this.item = function (index) {
            return this._elements[index];
        };
        // 添加 namedItem 方法
        this.namedItem = function (name) {
            return this._elements.find(el => el.id === name || el.name === name) || null;
        };
    });
    HTMLAllCollection = v_safe(function HTMLAllCollection() {
        this.length = 964;
    });
    HTMLBodyElement = v_safe(function HTMLBodyElement() {
        this.tagName = 'BODY'
    });
    _inherits(HTMLBodyElement, HTMLElement);
    Permissions = v_safe(function Permissions() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    PermissionStatus = v_safe(function PermissionStatus() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
        this.name = 'video_capture';
        this.state = 'prompt';
    });
    NavigatorUAData = v_safe(function NavigatorUAData() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    XMLHttpRequestEventTarget = v_safe(function XMLHttpRequestEventTarget() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });
    _inherits(XMLHttpRequestEventTarget, EventTarget)
    XMLHttpRequest = v_safe(function XMLHttpRequest(){});
    _inherits(XMLHttpRequest, XMLHttpRequestEventTarget)
    Client = v_safe(function Client() {
        if (!v_new_toggle) {
            throw TypeError("Illegal constructor")
        };
    });

    Object.defineProperties(EventTarget.prototype, {
        [Symbol.toStringTag]: {value: "EventTarget", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Window.prototype, {
        [Symbol.toStringTag]: {value: "Window", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Screen.prototype, {
        [Symbol.toStringTag]: {value: "Screen", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Node.prototype, {
        [Symbol.toStringTag]: {value: "Node", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Document.prototype, {
        [Symbol.toStringTag]: {value: "Document", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(HTMLDocument.prototype, {
        [Symbol.toStringTag]: {value: "HTMLDocument", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Element.prototype, {
        [Symbol.toStringTag]: {value: "Element", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(HTMLElement.prototype, {
        [Symbol.toStringTag]: {value: "HTMLElement", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(HTMLHtmlElement.prototype, {
        [Symbol.toStringTag]: {value: "HTMLHtmlElement", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Navigator.prototype, {
        [Symbol.toStringTag]: {value: "Navigator", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(History.prototype, {
        [Symbol.toStringTag]: {value: "History", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Location.prototype, {
        [Symbol.toStringTag]: {value: "Location", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Storage.prototype, {
        [Symbol.toStringTag]: {value: "Storage", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(HTMLCollection.prototype, {
        [Symbol.toStringTag]: {value: "HTMLCollection", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(HTMLAllCollection.prototype, {
        [Symbol.toStringTag]: {value: "HTMLAllCollection", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(HTMLBodyElement.prototype, {
        [Symbol.toStringTag]: {value: "HTMLBodyElement", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Permissions.prototype, {
        [Symbol.toStringTag]: {value: "Permissions", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(PermissionStatus.prototype, {
        [Symbol.toStringTag]: {value: "PermissionStatus", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(NavigatorUAData.prototype, {
        [Symbol.toStringTag]: {value: "NavigatorUAData", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(XMLHttpRequestEventTarget.prototype, {
        [Symbol.toStringTag]: {value: "XMLHttpRequestEventTarget", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(XMLHttpRequest.prototype, {
        [Symbol.toStringTag]: {value: "XMLHttpRequest", writable: false, enumerable: false, configurable: true},
    })
    Object.defineProperties(Client.prototype, {
        [Symbol.toStringTag]: {value: "Client", writable: false, enumerable: false, configurable: true},
    })


    if (typeof __dirname != 'undefined') {
        __dirname = undefined
    }
    if (typeof __filename != 'undefined') {
        __filename = undefined
    }
    // if (typeof require != 'undefined'){ require = undefined }
    if (typeof exports != 'undefined') {
        exports = undefined
    }
    if (typeof module != 'undefined') {
        module = undefined
    }
    if (typeof Buffer != 'undefined') {
        Buffer = undefined
    }
    var avoid_log = ['Symbol', 'Object', 'Number', 'RegExp', 'Boolean', 'String', 'constructor']
    var __globalThis__ = typeof global != 'undefined' ? global : this
    var window = new Proxy(v_new(Window), {
        get(a, b) {
            if (b == 'global') {
                return
            }
            var r = a[b] || __globalThis__[b]
            if (typeof b !== 'symbol' && avoid_log.indexOf(b) == -1) {
                // v_console_log('  [*] [window get ' + b + '] ==>', r)
                var r_str = typeof r === 'string' ? r : String(r);
                v_console_log('  [*] [window get ' + b + '] ==>', r_str.length > 100 ? r_str.substring(0, 100) + '... (truncated)' : r_str)
            }
            return r
        },
        set(a, b, c) {
            if (b == 'onclick' && typeof c == 'function') {
                window.addEventListener('click', c)
            }
            if (b == 'onmousedown' && typeof c == 'function') {
                window.addEventListener('mousedown', c)
            }
            if (b == 'onmouseup' && typeof c == 'function') {
                window.addEventListener('mouseup', c)
            }
            __globalThis__[b] = a[b] = c
            return true
        },
    })

    function v_proxy(obj, name, func) {
        return new Proxy(obj, {
            get(a, b) {
                if (b == 'global') {
                    return
                }
                var r = a[b]
                if (typeof b !== 'symbol' && avoid_log.indexOf(b) == -1) {
                    v_console_log('  [*] [' + name + ' get ' + b + '] ==>', r)
                }
                if (func && typeof r == 'undefined') {
                    r = func(name)
                }
                return r
            },
            set(a, b, c) {
                if (typeof b !== 'symbol' && avoid_log.indexOf(b) == -1) {
                    v_console_log('  [*] [' + name + ' set ' + b + '] <--', c)
                }
                a[b] = c
                return true
            },
        })
    }

    var v_hasOwnProperty = Object.prototype.hasOwnProperty
    Object.prototype.hasOwnProperty = v_safe(function hasOwnProperty() {
        var r;
        if (this === window) {
            r = v_hasOwnProperty.apply(__globalThis__, arguments)
        } else {
            r = v_hasOwnProperty.apply(this, arguments)
        }
        v_console_log('  [*] [hasOwnProperty]', this === window ? window : this, [].slice.call(arguments), r)
        return r
    })
    Object.defineProperties(__globalThis__, {[Symbol.toStringTag]: {value: 'Window'}})
    Object.defineProperties(__globalThis__, Object.getOwnPropertyDescriptors(window))
    Object.setPrototypeOf(__globalThis__, Object.getPrototypeOf(window))
    window.parent = window
    window.top = window
    window.frames = window
    window.self = window
    window.document = v_proxy(v_new(HTMLDocument), "document")
    window.location = v_proxy(v_new(Location), "location")
    window.navigator = v_proxy(v_new(Navigator), "navigator")
    window.history = v_proxy(v_new(History), "history")
    window.screen = v_proxy(v_new(Screen), "screen")
    window.localStorage = v_proxy(v_new(Storage), "localStorage")
    window.HTMLElement = v_proxy(v_new(HTMLElement), "HTMLElement")
    window.insight = v_proxy(v_new(Client), "insight")
    window.addEventListener = v_safe(function addEventListener(args) {
        v_console_log('window.addEventListener--->', args)
    })
    window.MouseEvent = v_safe(function MouseEvent(args) {
        v_console_log('window.MouseEvent--->', args)
    })
    window.DeviceMotionEvent = v_safe(function DeviceMotionEvent(args) {
        v_console_log('window.DeviceMotionEvent--->', args)
    })
    window.DeviceOrientationEvent = v_safe(function DeviceOrientationEvent(args) {
        v_console_log('window.DeviceOrientationEvent--->', args)
    })
    window.chrome = {
        "app": {
            "isInstalled": false,
            "InstallState": {
                "DISABLED": "disabled",
                "INSTALLED": "installed",
                "NOT_INSTALLED": "not_installed"
            },
            "RunningState": {
                "CANNOT_RUN": "cannot_run",
                "READY_TO_RUN": "ready_to_run",
                "RUNNING": "running"
            }
        }
    }
    window.loadts = Date.now().toString()
    window.requestAnimationFrame = v_safe(function requestAnimationFrame(args) {
        v_console_log('window.requestAnimationFrame--->', args)
    })
    window.requestIdleCallback = v_safe(function requestIdleCallback(args) {
        v_console_log('window.requestIdleCallback--->', args)
    })
    window.xsecappid = 'xhs-pc-web'
    window._66062487cf103622475a2f9b17d8293e = 'mns0301'
    window.insight.sendCustomPoint = v_safe(function sendCustomPoint(args) {
        v_console_log('sendCustomPoint--->', args)
    })
    window.WebGLRenderingContext = v_safe(function WebGLRenderingContext(args) {
        v_console_log('window.WebGLRenderingContext--->', args)
    })
    window.localStorage.getItem = v_safe(function getItem(args) {
        v_console_log('localStorage.getItem--->', args)
    })
    document.querySelector = v_safe(function querySelector(args) {
        v_console_log('document.querySelector--->', args)
    })
    document.querySelectorAll = v_safe(function querySelectorAll(args) {
        v_console_log('document.querySelectorAll--->', args)
    })
    // window.XMLHttpRequest = v_proxy(v_new(XMLHttpRequest), "XMLHttpRequest")


    var win = {
        window: window,
        frames: window,
        parent: window,
        self: window,
        top: window,
    }

    function v_repair_this() {
        win = {
            window: __globalThis__,
            frames: __globalThis__,
            parent: __globalThis__,
            self: __globalThis__,
            top: __globalThis__,
        }
    }

    Object.defineProperties(window, {
        window: {
            get: function () {
                return win.window
            }, set: function (e) {
                return true
            }
        },
        frames: {
            get: function () {
                return win.frames
            }, set: function (e) {
                return true
            }
        },
        parent: {
            get: function () {
                return win.parent
            }, set: function (e) {
                return true
            }
        },
        self: {
            get: function () {
                return win.self
            }, set: function (e) {
                return true
            }
        },
        top: {
            get: function () {
                return win.top
            }, set: function (e) {
                return true
            }
        },
    })

    v_repair_this() // 修复 window 指向global
    v_new_toggle = false;

    !(function v_init_EventTarget() {
        EventTarget.prototype.addEventListener = v_safe(function (args) {
            v_console_log('EventTarget.addEventListener-->', args)
        })
    })();
    !(function v_init_Node() {
        Node.prototype.removeChild = v_safe(function (args) {
            v_console_log('Node.removeChild-->', args)
        })
    })();
    !(function v_init_Element() {
        Element.prototype.getAttribute = v_safe(function (args) {
            if (args === 'selenium' || args === 'webdriver' || args === 'driver') {
                return null
            }
            v_console_log('Element.getAttribute-->', args)
        })
    })();
    !(function v_init_Document() {
        Document.prototype.documentElement = v_proxy(v_new(HTMLHtmlElement), "documentElement")
        Document.prototype.getElementById = v_safe(function (args) {
            v_console_log('Document.getElementById-->', args)
        })
        Document.prototype.getElementsByTagName = v_safe(function (args) {
            v_console_log('Document.getElementsByTagName-->', args)
            if (args === '*') {
                return v_proxy(v_new(HTMLCollection), "HTMLCollection")
            }
        })
        Document.prototype.evaluate = v_safe(function (args) {
            v_console_log('Document.evaluate-->', args)
        })
        Document.prototype.all = v_proxy(v_new(HTMLAllCollection), "HTMLAllCollection")
        Document.prototype.body = v_proxy(v_new(HTMLBodyElement), "HTMLBodyElement")
        Document.prototype.cookie = 'abRequestId=f3739fb4-8307-5438-b9ea-6d0eefcc89fa; ets=1774572737212; webBuild=6.2.1; xsecappid=xhs-pc-web; loadts=1774572737305; a1=19d2cc7131fpi3gwmjgx5b4j8leb1cxs16ot0jrlk50000341047; webId=a82bb7352e318e2efd62de0d63814d82; gid=yjfJSSWJyyyjyjfJSSWyqKVFyiU3qkE6VkC2l1TD4VY1d928DySCM8888q4y84W8ydWDddW8; unread={%22ub%22:%2269b94564000000001f00183f%22%2C%22ue%22:%22699ed5ed0000000015032891%22%2C%22uc%22:62}; websectiga=cffd9dcea65962b05ab048ac76962acee933d26157113bb213105a116241fa6c'

    })();
    !(function v_init_Navigator() {
        Navigator.prototype.permissions = v_proxy(v_new(Permissions), "Permissions")
    })();
    !(function v_init_Permissions() {
        Permissions.prototype.query = v_safe(function (args) {
            v_console_log('Permissions.query-->', args)
            return Promise.resolve(v_proxy(v_new(PermissionStatus), "PermissionStatus"))
        })
    })();
    !(function v_init_XMLHttpRequest() {
        XMLHttpRequest.prototype.open = v_safe(function (args) {
            v_console_log('XMLHttpRequest.open-->', args)
        })
        XMLHttpRequest.prototype.send = v_safe(function (args) {
            v_console_log('XMLHttpRequest.send-->', args)
        })
        XMLHttpRequest.prototype.setRequestHeader = v_safe(function (args) {
            v_console_log('XMLHttpRequest.setRequestHeader-->', args)
        })
    })();


    v_console_log = function(){} // 关闭日志输出
    setTimeout = function(){} // 关闭定时器
    setInterval = function(){} // 关闭定时器
    return window
})();
