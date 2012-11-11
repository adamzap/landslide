/*
 * classList.js: Implements a cross-browser element.classList getter.
 * 2010-09-06
 *
 * By Eli Grey, http://eligrey.com
 * Public Domain.
 * NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
 */

"use strict";

if (typeof Element !== "undefined") {

(function () {

var
      classListProp = "classList"
    , protoProp = "prototype"
    , elemCtrProto = Element[protoProp]
    , objCtr = Object
;
if (!objCtr.hasOwnProperty.call(elemCtrProto, classListProp)) {
    var
          strTrim = String[protoProp].trim || function () {
            return this.replace(/^\s+|\s+$/g, "");
        }
        , arrIndexOf = Array[protoProp].indexOf || function (item) {
            for (var i = 0, len = this.length; i < len; i++) {
                if (i in this && this[i] === item) {
                    return i;
                }
            }
            return -1;
        }
        , checkTokenAndGetIndex = function (classList, token) {
            if (token === "") {
                throw "SYNTAX_ERR";
            }
            if (/\s/.test(token)) {
                throw "INVALID_CHARACTER_ERR";
            }
            return arrIndexOf.call(classList, token);
        }
        , ClassList = function (elem) {
            var
                  trimmedClasses = strTrim.call(elem.className)
                , classes = trimmedClasses ? trimmedClasses.split(/\s+/) : []
            ;
            for (var i = 0, len = classes.length; i < len; i++) {
                this.push(classes[i]);
            }
            this.updateClassName = function () {
                elem.className = this.toString();
            };
        }
        , classListProto = ClassList[protoProp] = []
        , classListGetter = function () {
            return new ClassList(this);
        }
    ;
    classListProto.item = function (i) {
        return this[i] || null;
    };
    classListProto.contains = function (token) {
        token += "";
        return checkTokenAndGetIndex(this, token) !== -1;
    };
    classListProto.add = function (token) {
        token += "";
        if (checkTokenAndGetIndex(this, token) === -1) {
            this.push(token);
            this.updateClassName();
        }
    };
    classListProto.remove = function (token) {
        token += "";
        var index = checkTokenAndGetIndex(this, token);
        if (index !== -1) {
            this.splice(index, 1);
            this.updateClassName();
        }
    };
    classListProto.toggle = function (token) {
        token += "";
        if (checkTokenAndGetIndex(this, token) === -1) {
            this.add(token);
        } else {
            this.remove(token);
        }
    };
    classListProto.toString = function () {
        return this.join(" ");
    };
    
    if (objCtr.defineProperty) {
        var classListDescriptor = {
              get: classListGetter
            , enumerable: true
            , configurable: true
        };
        try {
            objCtr.defineProperty(elemCtrProto, classListProp, classListDescriptor);
        } catch (ex) { // IE 8 doesn't support enumerable:true
            if (ex.number === -0x7FF5EC54) {
                classListDescriptor.enumerable = false;
                objCtr.defineProperty(elemCtrProto, classListProp, classListDescriptor);
            }
        }
    } else if (objCtr[protoProp].__defineGetter__) {
        elemCtrProto.__defineGetter__(classListProp, classListGetter);
    }
}

}());

}