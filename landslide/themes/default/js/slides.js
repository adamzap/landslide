function main() {
  // Since we don't have the fallback of attachEvent and
  // other IE only stuff we won't try to run JS for IE.
  // It will run though when using Google Chrome Frame
  if (document.all) { return; }

  var currentSlideNo;
  var notesOn = false;
  var pageNumbersOn = true;
  var slides = document.getElementsByClassName('slide');
  var touchStartX = 0;

  // var slide_hash = window.location.hash.replace(/#/, '');
  // if (slide_hash) {
  //   for (var i = 0, len = slides.length; i < len; i++) {
  //     if (slides[i].id == slide_hash) {
  //       currentSlideNo = i;
  //       updateSlideClasses();
  //     }
  //   }
  // }

  var spaces = /\s+/, a1 = [""];

  var str2array = function(s) {
    if (typeof s == "string" || s instanceof String) {
      if (s.indexOf(" ") < 0) {
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
    var cls = " " + node.className + " ";
    for (var i = 0, len = classStr.length, c; i < len; ++i) {
      c = classStr[i];
      if (c && cls.indexOf(" " + c + " ") < 0) {
        cls += c + " ";
      }
    }
    node.className = trim(cls);
  };

  var removeClass = function(node, classStr) {
    var cls;
    if (classStr !== undefined) {
      classStr = str2array(classStr);
      cls = " " + node.className + " ";
      for (var i = 0, len = classStr.length; i < len; ++i) {
        cls = cls.replace(" " + classStr[i] + " ", " ");
      }
      cls = trim(cls);
    } else {
      cls = "";
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
      return el.getElementsByTagName('header')[0].innerHTML;
    } else {
      return null;
    }
  };

  var changeSlideElClass = function(slideNo, className) {
    var el = getSlideEl(slideNo);

    if (el) {
      removeClass(el, 'far-past past current future far-future');
      addClass(el, className);
    }
  };

  var updateSlideClasses = function() {
    window.location.hash = "slide" + currentSlideNo;
    changeSlideElClass(currentSlideNo - 2, 'far-past');
    changeSlideElClass(currentSlideNo - 1, 'past');
    changeSlideElClass(currentSlideNo, 'current');
    changeSlideElClass(currentSlideNo + 1, 'future');
    changeSlideElClass(currentSlideNo + 2, 'far-future');
  };

  var nextSlide = function() {
    if (currentSlideNo < slides.length) {
      currentSlideNo++;
    }

    updateSlideClasses();
  };

  var prevSlide = function() {
    if (currentSlideNo > 1) {
      currentSlideNo--;
    }
    updateSlideClasses();
  };

  var showNotes = function() {
    var notes = document.querySelectorAll('.notes');
    for (var i = 0, len = notes.length; i < len; i++) {
      notes[i].style.display = (notesOn) ? 'none':'block';
    }
    notesOn = (notesOn) ? false:true;
  };
  
  var showPageNumbers = function() {
    var pn = document.querySelectorAll('.page_number');
    for (var i = 0, len = pn.length; i < len; i++) {
      pn[i].style.display = (pageNumbersOn) ? 'none':'block';
    }
    pageNumbersOn = (pageNumbersOn) ? false:true;
  };
  
  var showToc = function() {
    var toc = document.getElementById('toc');
    var hidden = toc.style.display != 'block';
    toc.style.display = hidden ? 'block' : 'none';
    return false;
  };

  var switch3D = function() {
    if (document.body.className.indexOf('three-d') == -1) {
      document.getElementsByClassName('presentation')[0].style.webkitPerspective = '1000px';
      document.body.className += ' three-d';
    } else {
      window.setTimeout("document.getElementsByClassName('presentation')[0].style.webkitPerspective = '0';", 2000);
      document.body.className = document.body.className.replace(/three-d/, '');
    }
  };

  var handleBodyKeyDown = function(event) {
    switch (event.keyCode) {
      case 37: // left arrow
        prevSlide();
        break;
      case 39: // right arrow
      // case 32: // space
        nextSlide();
        break;
      case 50: // 2
        showNotes();
        break;
      case 51: // 3
        switch3D();
        break;
      case 78: // n
        showPageNumbers();
        break;
      case 84: // t
        showToc();
        break;
    }
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
    var tocLinks = document.getElementById('toc').getElementsByTagName('a');
    for (var i=0; i < tocLinks.length; i++) {
      tocLinks.item(i).addEventListener('click', function(e) {
        currentSlideNo = Number(this.attributes['href'].value.replace('#slide', ''));
        updateSlideClasses();
        return false;
      }, true);
    }
  };

  // initialize

  (function() {
    if (window.location.hash != "") {
      currentSlideNo = Number(window.location.hash.replace('#slide', ''));
    } else {
      currentSlideNo = 1;
    }

    document.addEventListener('keydown', handleBodyKeyDown, false);

    var els = slides;
    for (var i = 0, el; el = els[i]; i++) {
      addClass(el, 'slide far-future');
    }
    updateSlideClasses();

    // add support for finger events (filter it by property detection?)
    addTouchListeners();
    
    addTocLinksListeners();
  })();
};