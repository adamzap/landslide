// Gifffer, for controlling GIFs
(function webpackUniversalModuleDefinition(root,factory){if(typeof exports==="object"&&typeof module==="object")module.exports=factory();else if(typeof define==="function"&&define.amd)define("Gifffer",[],factory);else if(typeof exports==="object")exports["Gifffer"]=factory();else root["Gifffer"]=factory()})(this,function(){var d=document;var playSize=60;var Gifffer=function(options){var images,i=0,gifs=[];images=d.querySelectorAll("[data-gifffer]");for(;i<images.length;++i)process(images[i],gifs,options);return gifs};function formatUnit(v){return v+(v.toString().indexOf("%")>0?"":"px")}function parseStyles(styles){var stylesStr="";for(prop in styles)stylesStr+=prop+":"+styles[prop]+";";return stylesStr}function createContainer(w,h,el,altText,opts){var alt;var con=d.createElement("BUTTON");var cls=el.getAttribute("class");var id=el.getAttribute("id");var playButtonStyles=opts&&opts.playButtonStyles?parseStyles(opts.playButtonStyles):["width:"+playSize+"px","height:"+playSize+"px","border-radius:"+playSize/2+"px","background:rgba(0, 0, 0, 0.3)","position:absolute","top:50%","left:50%","margin:-"+playSize/2+"px"].join(";");var playButtonIconStyles=opts&&opts.playButtonIconStyles?parseStyles(opts.playButtonIconStyles):["width: 0","height: 0","border-top: 14px solid transparent","border-bottom: 14px solid transparent","border-left: 14px solid rgba(0, 0, 0, 0.5)","position: absolute","left: 26px","top: 16px"].join(";");cls?con.setAttribute("class",el.getAttribute("class")):null;id?con.setAttribute("id",el.getAttribute("id")):null;con.setAttribute("style","position:relative;cursor:pointer;background:none;border:none;padding:0;");con.setAttribute("aria-hidden","true");var play=d.createElement("DIV");play.setAttribute("class","gifffer-play-button");play.setAttribute("style",playButtonStyles);var trngl=d.createElement("DIV");trngl.setAttribute("style",playButtonIconStyles);play.appendChild(trngl);if(altText){alt=d.createElement("p");alt.setAttribute("class","gifffer-alt");alt.setAttribute("style","border:0;clip:rect(0 0 0 0);height:1px;overflow:hidden;padding:0;position:absolute;width:1px;");alt.innerText=altText+", image"}con.appendChild(play);el.parentNode.replaceChild(con,el);altText?con.parentNode.insertBefore(alt,con.nextSibling):null;return{c:con,p:play}}function calculatePercentageDim(el,w,h,wOrig,hOrig){var parentDimW=el.parentNode.offsetWidth;var parentDimH=el.parentNode.offsetHeight;var ratio=wOrig/hOrig;if(w.toString().indexOf("%")>0){w=parseInt(w.toString().replace("%",""));w=w/100*parentDimW;h=w/ratio}else if(h.toString().indexOf("%")>0){h=parseInt(h.toString().replace("%",""));h=h/100*parentDimW;w=h*ratio}return{w:w,h:h}}function process(el,gifs,options){var url,con,c,w,h,duration,play,gif,playing=false,cc,isC,durationTimeout,dims,altText;url=el.getAttribute("data-gifffer");w=el.getAttribute("data-gifffer-width");h=el.getAttribute("data-gifffer-height");duration=el.getAttribute("data-gifffer-duration");altText=el.getAttribute("data-gifffer-alt");el.style.display="block";c=document.createElement("canvas");isC=!!(c.getContext&&c.getContext("2d"));if(w&&h&&isC)cc=createContainer(w,h,el,altText,options);el.onload=function(){if(!isC)return;w=w||el.width;h=h||el.height;if(!cc)cc=createContainer(w,h,el,altText,options);con=cc.c;play=cc.p;dims=calculatePercentageDim(con,w,h,el.width,el.height);gifs.push(con);con.addEventListener("click",function(){clearTimeout(durationTimeout);if(!playing){playing=true;gif=document.createElement("IMG");gif.setAttribute("style","width:100%;height:100%;");gif.setAttribute("data-uri",Math.floor(Math.random()*1e5)+1);setTimeout(function(){gif.src=url},0);con.removeChild(play);con.removeChild(c);con.appendChild(gif);if(parseInt(duration)>0){durationTimeout=setTimeout(function(){playing=false;con.appendChild(play);con.removeChild(gif);con.appendChild(c);gif=null},duration)}}else{playing=false;con.appendChild(play);con.removeChild(gif);con.appendChild(c);gif=null}});c.width=dims.w;c.height=dims.h;c.getContext("2d").drawImage(el,0,0,dims.w,dims.h);con.appendChild(c);con.setAttribute("style","position:relative;cursor:pointer;width:"+dims.w+"px;height:"+dims.h+"px;background:none;border:none;padding:0;");c.style.width="100%";c.style.height="100%";if(w.toString().indexOf("%")>0&&h.toString().indexOf("%")>0){con.style.width=w;con.style.height=h}else if(w.toString().indexOf("%")>0){con.style.width=w;con.style.height="inherit"}else if(h.toString().indexOf("%")>0){con.style.width="inherit";con.style.height=h}else{con.style.width=dims.w+"px";con.style.height=dims.h+"px"}};el.src=url}return Gifffer});

function main() {
    // Since we don't have the fallback of attachEvent and
    // other IE only stuff we won't try to run JS for IE.
    // It will run though when using Google Chrome Frame
    if (document.all) { return; }

    var currentSlideNo;
    var notesOn = false;
    var expanded = false;
    var hiddenContext = false;
    var blanked = false;
    var slides = document.getElementsByClassName('slide');
    var touchStartX = 0;
    var spaces = /\s+/, a1 = [''];
    var tocOpened = false;
    var helpOpened = false;
    var overviewActive = false;
    var modifierKeyDown = false;
    var scale = 1;
    var showingPresenterView = false;
    var presenterViewWin = null;
    var isPresenterView = false;
    var gifs = [];

    var str2array = function(s) {
        if (typeof s == 'string' || s instanceof String) {
            if (s.indexOf(' ') < 0) {
                a1[0] = s;
                return a1;
            } else {
                return s.split(spaces);
            }
        }
        return s;
    };

    var trim = function(str) {
        return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
    };

    var addClass = function(node, classStr) {
        classStr = str2array(classStr);
        var cls = ' ' + node.className + ' ';
        for (var i = 0, len = classStr.length, c; i < len; ++i) {
            c = classStr[i];
            if (c && cls.indexOf(' ' + c + ' ') < 0) {
                cls += c + ' ';
            }
        }
        node.className = trim(cls);
    };

    var removeClass = function(node, classStr) {
        var cls;
        if (!node) {
            throw 'no node provided';
        }
        if (classStr !== undefined) {
            classStr = str2array(classStr);
            cls = ' ' + node.className + ' ';
            for (var i = 0, len = classStr.length; i < len; ++i) {
                cls = cls.replace(' ' + classStr[i] + ' ', ' ');
            }
            cls = trim(cls);
        } else {
            cls = '';
        }
        if (node.className != cls) {
            node.className = cls;
        }
    };

    var getSlideEl = function(slideNo) {
        if (slideNo > 0) {
            return slides[slideNo - 1];
        } else {
            return null;
        }
    };

    var getSlideTitle = function(slideNo) {
        var el = getSlideEl(slideNo);
        if (el) {
            var headers = el.getElementsByTagName('header');
            if (headers.length > 0) {
                return el.getElementsByTagName('header')[0].innerText;
            }
        }
        return null;
    };

    var getSlidePresenterNote = function(slideNo) {
        var el = getSlideEl(slideNo);
        if (el) {
            var n = el.getElementsByClassName('presenter_notes');
            if (n.length > 0) {
                return n[0];
            }
        }
        return null;
    };

    var changeSlideElClass = function(slideNo, className) {
        var el = getSlideEl(slideNo);
        if (el) {
            removeClass(el, 'far-past past current future far-future');
            addClass(el, className);
        }
    };

    var updateSlideClasses = function(updateOther) {
        window.location.hash = (isPresenterView ? "presenter" : "slide") + currentSlideNo;

        for (var i=1; i<currentSlideNo-1; i++) {
            changeSlideElClass(i, 'far-past');
        }

        changeSlideElClass(currentSlideNo - 1, 'past');
        changeSlideElClass(currentSlideNo, 'current');
        changeSlideElClass(currentSlideNo + 1, 'future');

        for (i=currentSlideNo+2; i<slides.length+1; i++) {
            changeSlideElClass(i, 'far-future');
        }

        highlightCurrentTocLink();

        processContext();

        document.getElementsByTagName('title')[0].innerText = getSlideTitle(currentSlideNo);

        updatePresenterNotes();
        handleAutoplays();

        if (updateOther) { updateOtherPage(); }
    };

    var updatePresenterNotes = function() {
        if (!isPresenterView) { return; }

        var existingNote = document.getElementById('current_presenter_notes');
        var currentNote = getSlidePresenterNote(currentSlideNo).cloneNode(true);
        currentNote.setAttribute('id', 'presenter_note');

        existingNote.replaceChild(currentNote, document.getElementById('presenter_note'));
    };

    var highlightCurrentTocLink = function() {
        var toc = document.getElementById('toc');

        if (toc) {
            var tocRows = toc.getElementsByTagName('tr');
            for (var i=0; i<tocRows.length; i++) {
                removeClass(tocRows.item(i), 'active');
            }

            var currentTocRow = document.getElementById('toc-row-' + currentSlideNo);
            if (currentTocRow) {
                addClass(currentTocRow, 'active');
            }
        }
    };

    var updateOtherPage = function() {
        if (!showingPresenterView) { return; }

        var w = isPresenterView ? window.opener : presenterViewWin;
        w.postMessage('slide#' + currentSlideNo, '*');
    };

    var nextSlide = function() {
        if (currentSlideNo < slides.length) {
            currentSlideNo++;
        }
        updateSlideClasses(true);
    };

    var prevSlide = function() {
        if (currentSlideNo > 1) {
            currentSlideNo--;
        }
        updateSlideClasses(true);
    };
    
    var gotoSlide = function(slideNumber) {
        currentSlideNo = slideNumber;
        updateSlideClasses(true);
    }
    main.gotoSlide = gotoSlide;

    var showNotes = function() {
        var notes = getSlideEl(currentSlideNo).getElementsByClassName('notes');
        for (var i = 0, len = notes.length; i < len; i++) {
            notes.item(i).style.display = (notesOn) ? 'none':'block';
        }
        notesOn = !notesOn;
    };

    var showSlideNumbers = function() {
        var asides = document.getElementsByClassName('page_number');
        var hidden = asides[0].style.display != 'block';
        for (var i = 0; i < asides.length; i++) {
            asides.item(i).style.display = hidden ? 'block' : 'none';
        }
    };

    var showSlideSources = function() {
        var asides = document.getElementsByClassName('source');
        var hidden = asides[0].style.display != 'block';
        for (var i = 0; i < asides.length; i++) {
            asides.item(i).style.display = hidden ? 'block' : 'none';
        }
    };

    var showToc = function() {
        if (helpOpened) {
                showHelp();
        }
        var toc = document.getElementById('toc');
        if (toc) {
            toc.style.marginLeft = tocOpened ? '-' + (toc.clientWidth + 20) + 'px' : '0px';
            tocOpened = !tocOpened;
        }
        updateOverview();
    };

    var showHelp = function() {
        if (tocOpened) {
                showToc();
        }

        var help = document.getElementById('help');

        if (help) {
            help.style.marginLeft = helpOpened ? '-' + (help.clientWidth + 20) + 'px' : '0px';
            helpOpened = !helpOpened;
        }
    };

    var showPresenterView = function() {
        if (isPresenterView) { return; }

        if (showingPresenterView) {
            presenterViewWin.close();
            presenterViewWin = null;
            showingPresenterView = false;
        } else {
            presenterViewWin = open(window.location.pathname + "#presenter" + currentSlideNo, 'presenter_notes',
                                                                    'directories=no,location=no,toolbar=no,menubar=no,copyhistory=no');
            showingPresenterView = true;
        }
    };

    var switch3D = function() {
        if (document.body.className.indexOf('three-d') == -1) {
            document.getElementsByClassName('presentation')[0].style.webkitPerspective = '1000px';
            document.body.className += ' three-d';
        } else {
            window.setTimeout('document.getElementsByClassName(\'presentation\')[0].style.webkitPerspective = \'0\';', 2000);
            document.body.className = document.body.className.replace(/three-d/, '');
        }
    };

    var toggleOverview = function() {
        if (!overviewActive) {
            addClass(document.body, 'expose');
            overviewActive = true;
            setScale(1);
        } else {
            removeClass(document.body, 'expose');
            overviewActive = false;
            if (expanded) {
                setScale(scale);    // restore scale
            }
        }
        processContext();
        updateOverview();
    };

    var updateOverview = function() {
        try {
            var presentation = document.getElementsByClassName('presentation')[0];
        } catch (e) {
            return;
        }

        if (isPresenterView) {
            var action = overviewActive ? removeClass : addClass;
            action(document.body, 'presenter_view');
        }

        var toc = document.getElementById('toc');

        if (!toc) {
            return;
        }

        if (!tocOpened || !overviewActive) {
            presentation.style.marginLeft = '0px';
            presentation.style.width = '100%';
        } else {
            presentation.style.marginLeft = toc.clientWidth + 'px';
            presentation.style.width = (presentation.clientWidth - toc.clientWidth) + 'px';
        }
    };

    var computeScale = function() {
        var cSlide = document.getElementsByClassName('current')[0];
        var sx = cSlide.clientWidth / window.innerWidth;
        var sy = cSlide.clientHeight / window.innerHeight;
        return 1 / Math.max(sx, sy);
    };

    var setScale = function(scale) {
        var presentation = document.getElementsByClassName('slides')[0];
        var transform = 'scale(' + scale + ')';
        presentation.style.MozTransform = transform;
        presentation.style.WebkitTransform = transform;
        presentation.style.OTransform = transform;
        presentation.style.msTransform = transform;
        presentation.style.transform = transform;
    };

    var expandSlides = function() {
        if (overviewActive) {
            return;
        }
        if (expanded) {
            setScale(1);
            expanded = false;
        } else {
            scale = computeScale();
            setScale(scale);
            expanded = true;
        }
        
    };

    var showContext = function() {
        try {
            var presentation = document.getElementsByClassName('slides')[0];
            removeClass(presentation, 'nocontext');
        } catch (e) {}
    };

    var hideContext = function() {
        if (!isPresenterView) {
            try {
                var presentation = document.getElementsByClassName('slides')[0];
                addClass(presentation, 'nocontext');
            } catch (e) {}
        }
    };

    var processContext = function() {
        if (hiddenContext) {
            hideContext();
        } else {
            showContext();
        }
    };

    var toggleContext = function() {
        hiddenContext = !hiddenContext;
        processContext();
    };

    var toggleBlank = function() {
        blank_elem = document.getElementById('blank');

        blank_elem.style.display = blanked ? 'none' : 'block';

        blanked = !blanked;
    };

    var isModifierKey = function(keyCode) {
        switch (keyCode) {
            case 16: // shift
            case 17: // ctrl
            case 18: // alt
            case 91: // command
                return true;
                break;
            default:
                return false;
                break;
        }
    };

    var checkModifierKeyUp = function(event) {
        if (isModifierKey(event.keyCode)) {
            modifierKeyDown = false;
        }
    };

    var checkModifierKeyDown = function(event) {
        if (isModifierKey(event.keyCode)) {
            modifierKeyDown = true;
        }
    };

    var handleBodyKeyDown = function(event) {
        switch (event.keyCode) {
            case 13: // Enter
                if (overviewActive) {
                    toggleOverview();
                }
                break;
            case 27: // ESC
                toggleOverview();
                break;
            case 37: // left arrow
            case 33: // page up
                event.preventDefault();
                prevSlide();
                break;
            case 39: // right arrow
            case 32: // space
            case 34: // page down
                event.preventDefault();
                nextSlide();
                break;
            case 50: // 2
                if (!modifierKeyDown) {
                        showNotes();
                }
                break;
            case 51: // 3
                if (!modifierKeyDown && !overviewActive) {
                    switch3D();
                }
                break;
            case 190: // .
            case 48: // 0
            case 66: // b
                if (!modifierKeyDown && !overviewActive) {
                    toggleBlank();
                }
                break;
            case 67: // c
                if (!modifierKeyDown && !overviewActive) {
                    toggleContext();
                }
                break;
            case 69: // e
                if (!modifierKeyDown && !overviewActive) {
                    expandSlides();
                }
                break;
            case 72: // h
                showHelp();
                break;
            case 78: // n
                if (!modifierKeyDown && !overviewActive) {
                    showSlideNumbers();
                }
                break;
            case 80: // p
                if (!modifierKeyDown && !overviewActive) {
                    showPresenterView();
                }
                break;
            case 83: // s
                if (!modifierKeyDown && !overviewActive) {
                    showSlideSources();
                }
                break;
            case 84: // t
                showToc();
                break;
        }
    };

    var handleWheel = function(event) {
        if (tocOpened || helpOpened || overviewActive) {
            return;
        }

        var delta = 0;

        if (!event) {
            event = window.event;
        }

        if (event.wheelDelta) {
            delta = event.wheelDelta/120;
            if (window.opera) delta = -delta;
        } else if (event.detail) {
            delta = -event.detail/3;
        }

        if (delta && delta <0) {
            nextSlide();
        } else if (delta) {
            prevSlide();
        }
    };

    var addSlideClickListeners = function() {
        for (var i=0; i < slides.length; i++) {
            var slide = slides.item(i);
            slide.num = i + 1;
            slide.addEventListener('click', function(e) {
                if (overviewActive) {
                    currentSlideNo = this.num;
                    toggleOverview();
                    updateSlideClasses(true);
                    e.preventDefault();
                }
                return false;
            }, true);
        }
    };

    var addRemoteWindowControls = function() {
        window.addEventListener("message", function(e) {
            if (e.data.indexOf("slide#") != -1) {
                    currentSlideNo = Number(e.data.replace('slide#', ''));
                    updateSlideClasses(false);
            }
        }, false);
    };

    var addTouchListeners = function() {
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.touches[0].pageX;
        }, false);
        document.addEventListener('touchend', function(e) {
            var pixelsMoved = touchStartX - e.changedTouches[0].pageX;
            var SWIPE_SIZE = 150;
            if (pixelsMoved > SWIPE_SIZE) {
                nextSlide();
            }
            else if (pixelsMoved < -SWIPE_SIZE) {
             prevSlide();
            }
        }, false);
    };

    var addTocLinksListeners = function() {
        var toc = document.getElementById('toc');
        if (toc) {
            var tocLinks = toc.getElementsByTagName('a');
            for (var i=0; i < tocLinks.length; i++) {
                tocLinks.item(i).addEventListener('click', function(e) {
                    currentSlideNo = Number(this.attributes['href'].value.replace('#slide', ''));
                    updateSlideClasses(true);
                    e.preventDefault();
                }, true);
            }
        }
    };
    
    var setPlayStatuses = function(medias) {
        var cSlide = document.getElementsByClassName('current')[0];
        
        for (var i = 0; i < medias.length; i++) {
            if (medias[i].hasAttribute('autoplay')) {
                if (isPresenterView) {
                    medias[i].pause();
                    medias[i].currentTime = 0;
                }
                else {
                    if (cSlide.contains(medias[i])) {
                        medias[i].play();
                    }
                    else {
                        medias[i].pause();
                        medias[i].currentTime = 0;
                    }
                }
            }
        }
    };
    
    var handleAutoplays = function() {
        // Stop autoplaying video and audio on all slides except current
        var videos = document.getElementsByTagName('video');
        setPlayStatuses(videos);
        
        var audios = document.getElementsByTagName('audio');
        setPlayStatuses(audios);
        
        var cSlide = document.getElementsByClassName('current')[0];
        for (var i = 0; i < gifs.length; i++) {
            if (isPresenterView) {
                if (gifs[i].hasAttribute('playing')) {
                    gifs[i].click();
                    gifs[i].removeAttribute('playing');
                }
            }
            else {
                if (cSlide.contains(gifs[i])) {
                    gifs[i].click();
                    gifs[i].setAttribute('playing', '');
                }
                else {
                    if (gifs[i].hasAttribute('playing')) {
                        gifs[i].click();
                        gifs[i].removeAttribute('playing');
                    }
                }
            }
        }
    };
    
    var setupGIFs = function() {
        var images = document.getElementsByTagName('img');
        for (var i = 0; i < images.length; i++) {
            var src = images[i].src;
            var src_end = src.slice(src.length - 3, src.length);
            
            var alt = images[i].alt;
            var alt_end = alt.slice(alt.length - 3, alt.length);
            if (src_end == 'gif' || alt_end == 'gif') {
                images[i].setAttribute('data-gifffer', src);
                images[i].removeAttribute('src');
            }
        }
        gifs = Gifffer({playButtonStyles: {}, playButtonIconStyles: {}});
    };
    
    var setInternalTargets = function(refs) {
        for (var i = 0; i < refs.length; i++) {
            var parts = refs[i].href.split('#');
            var target_id = parts[parts.length - 1];
            var target = document.getElementById(target_id);
            for (var x = 0; x < slides.length; x++) {
                if (slides[x].contains(target)) {
                    var slideNumber = (x + 1).toString();
                    refs[i].href = 'javascript:main.gotoSlide(' + slideNumber + ');';
                    break;
                }
            }
        }
    };
    
    var adaptInternalHyperlinks = function() {
        // Set internal hyperlink (like footnotes) to goto target slide
        var forwardRefs = document.getElementsByClassName('footnote-reference');
        setInternalTargets(forwardRefs);
        
        var forwardCites = document.getElementsByClassName('citation-reference');
        setInternalTargets(forwardCites);
        
        var backRefs = document.getElementsByClassName('fn-backref');
        setInternalTargets(backRefs);
    };

    // initialize

    (function() {
        if (window.location.hash == "") {
            currentSlideNo = 1;
        } else if (window.location.hash.indexOf("#presenter") != -1) {
            currentSlideNo = Number(window.location.hash.replace('#presenter', ''));
            isPresenterView = true;
            showingPresenterView = true;
            presenterViewWin = window;
            addClass(document.body, 'presenter_view');
        } else {
            currentSlideNo = Number(window.location.hash.replace('#slide', ''));
        }

        document.addEventListener('keyup', checkModifierKeyUp, false);
        document.addEventListener('keydown', handleBodyKeyDown, false);
        document.addEventListener('keydown', checkModifierKeyDown, false);
        document.addEventListener('DOMMouseScroll', handleWheel, false);

        document.onmousewheel = handleWheel;
        window.onresize = expandSlides;

        for (var i = 0, el; el = slides[i]; i++) {
            addClass(el, 'slide far-future');
        }
        updateSlideClasses(false);

        // add support for finger events (filter it by property detection?)
        addTouchListeners();

        addTocLinksListeners();

        addSlideClickListeners();

        addRemoteWindowControls();
        
        setupGIFs();
        handleAutoplays();
        adaptInternalHyperlinks();

    })();
}
