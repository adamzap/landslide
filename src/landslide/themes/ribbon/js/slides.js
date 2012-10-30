(function () {
	var url = window.location,
		body = document.body,
		slides = document.querySelectorAll('.slide'),
		progress = document.querySelector('div.progress div'),
        presenterWin = null,
		slideList = [],
		timer,
        spaces = /\s+/, a1 = [''],
		l = slides.length, i;

	for (i = 0; i < l; i++) {
		// Slide ID's are optional. In case of missing ID we set it to the
		// slide number
		if (!slides[i].id) {
			slides[i].id = i + 1;
		}

		slideList.push({
			id: slides[i].id,
			hasInnerNavigation: null !== slides[i].querySelector('.next'),
			hasTiming: null != slides[i].dataset.timing
		});
	}

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


    function fullUrl(baseUrl, queryStr, slideId) {
        var url = '';

        var presenter = getParamByName('presenter');
        if (presenter != '') {
            url += baseUrl + "?presenter=" + presenter + "&" + queryStr;
        } else {
            url += baseUrl + "?" + queryStr;
        }

        url += '#' + slideId;
        return url;
    }

    function getParamByName(name) {
        name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
        var regexS = "[\\?&]" + name + "=([^&#]*)";
        var regex = new RegExp(regexS);
        var results = regex.exec(window.location.search);

        if(results == null)
            return "";
        else
            return decodeURIComponent(results[1].replace(/\+/g, " "));
    }

	function getTransform() {
		var denominator = Math.max(
			body.clientWidth / window.innerWidth,
			body.clientHeight / window.innerHeight
		);

		return 'scale(' + (1 / denominator) + ')';
	}

	function applyTransform(transform) {
		body.style.WebkitTransform = transform;
		body.style.MozTransform = transform;
		body.style.msTransform = transform;
		body.style.OTransform = transform;
		body.style.transform = transform;
	}

	function enterSlideMode() {
		body.classList.remove('list');
		body.classList.add('full');
		applyTransform(getTransform());
	}

	function enterListMode() {
		body.classList.remove('full');
		body.classList.add('list');
		applyTransform('none');
	}

	function getCurrentSlideNumber() {
		var i, l = slideList.length,
			currentSlideId = url.hash.substr(1);

		for (i = 0; i < l; ++i) {
			if (currentSlideId === slideList[i].id) {
				return i;
			}
		}

		return -1;
	}

	function scrollToSlide(slideNumber) {
		if (-1 === slideNumber ) { return; }

		var currentSlide = document.getElementById(slideList[slideNumber].id);

		if (null != currentSlide) {
			window.scrollTo(0, currentSlide.offsetTop);
		}
	}

	function isListMode() {
		return url.search.indexOf('full') == -1;
	}

	function normalizeSlideNumber(slideNumber) {
		if (0 > slideNumber) {
			return 0;
		} else if (slideList.length <= slideNumber) {
			return slideList.length - 1;
		} else {
			return slideNumber;
		}
	}

	function updateProgress(slideNumber) {
		if (null === progress) { return; }
		progress.style.width = (100 / (slideList.length - 1) * normalizeSlideNumber(slideNumber)).toFixed(2) + '%';
	}

	function updateCurrentAndPassedSlides(slideNumber) {
		var i, l = slideList.length, slide;
		slideNumber = normalizeSlideNumber(slideNumber);

		for ( i = 0; i < l; ++i ) {
			slide = document.getElementById(slideList[i].id);

			if ( i < slideNumber ) {
				slide.classList.remove('current');
				slide.classList.add('passed');
			} else if ( i > slideNumber ) {
				slide.classList.remove('passed');
				slide.classList.remove('current');
			} else {
				slide.classList.remove('passed');
				slide.classList.add('current');
			}
		}
	}

	function getSlideHash(slideNumber) {
		return '#' + slideList[normalizeSlideNumber(slideNumber)].id;
	}

	function goToSlide(slideNumber) {
		url.hash = getSlideHash(slideNumber);

		if (!isListMode()) {
			updateProgress(slideNumber);
			updateCurrentAndPassedSlides(slideNumber);
            if (presenterWin != null) {
                presenterWin.postMessage('slide#' + slideNumber, '*');
            }
		}
	}

	function getContainingSlideId(el) {
		var node = el;
		while ('BODY' !== node.nodeName && 'HTML' !== node.nodeName) {
			if (node.classList.contains('slide')) {
				return node.id;
			} else {
				node = node.parentNode;
			}
		}

		return '';
	}

	// FIXME: Renaming needed? Or just some handlers rewriting?
	function dispatchSingleSlideMode(e) {
		// Process links
		// TODO: presentation links support
		if ('A' === e.target.nodeName) {
			e.preventDefault();

			window.open(e.target.getAttribute('href'));
			return;
		}

		var slideId = getContainingSlideId(e.target);

		if ('' !== slideId && isListMode()) {
			e.preventDefault();

			// NOTE: we should update hash to get things work properly
			url.hash = '#' + slideId;
			history.replaceState(null, null,
                                 fullUrl(url.pathname, 'full', slideId));
			enterSlideMode();

			updateProgress(getCurrentSlideNumber());
			updateCurrentAndPassedSlides(getCurrentSlideNumber());
			runSlideshowIfPresented(getCurrentSlideNumber());
		}
	}

	function runSlideshowIfPresented(slideNumber) {
		slideNumber = normalizeSlideNumber(slideNumber);

		clearTimeout(timer);

		if (slideList[slideNumber].hasTiming) {
			// Compute number of milliseconds from format "X:Y", where X is
			// number of minutes, and Y is number of seconds
			var timing = document.getElementById(slideList[slideNumber].id).dataset.timing.split(':');
			timing = parseInt(timing[0]) * 60 * 1000 + parseInt(timing[1]) * 1000;

			timer = setTimeout( function () {
				goToSlide(slideNumber + 1);
				runSlideshowIfPresented(slideNumber + 1);
			}, timing );
		}
	}

	// Increases inner navigation by adding 'active' class to next inactive inner navigation item
	function increaseInnerNavigation(slideNumber) {
		// Shortcut for slides without inner navigation
		if (true !== slideList[slideNumber].hasInnerNavigation) { return -1; }

		var nextNodes = document.getElementById(slideList[slideNumber].id).querySelectorAll('.next:not(.active)'),
			node;

		if (0 !== nextNodes.length) {
			node = nextNodes[0];
			node.classList.add('active');
			return nextNodes.length - 1;
		} else {
			return -1;
		}
	}

	// Event handlers

	window.addEventListener('DOMContentLoaded', function () {
		if (!isListMode()) {
            // "?full" is present without slide hash, so we should display
            // first slide
			if (-1 === getCurrentSlideNumber()) {
				history.replaceState(null, null,
                                     fullUrl(url.pathname, 'full',
                                             getSlideHash(0)));
			}

			enterSlideMode();
			updateProgress(getCurrentSlideNumber());
			updateCurrentAndPassedSlides(getCurrentSlideNumber());
			runSlideshowIfPresented(getCurrentSlideNumber())
		}
	}, false);

	window.addEventListener('popstate', function (e) {
		if (isListMode()) {
			enterListMode();
			scrollToSlide(getCurrentSlideNumber());
		} else {
			enterSlideMode();
		}
	}, false);

	window.addEventListener('resize', function (e) {
		if (!isListMode()) {
			applyTransform(getTransform());
		}
	}, false);

    window.addEventListener("message", function(e) {
        if (e.data.indexOf("slide#") != -1) {
                currentSlideNo = Number(e.data.replace('slide#', ''));
                goToSlide(currentSlideNo);
        }
    }, false);

	document.addEventListener('keydown', function (e) {
		// Shortcut for alt, shift and meta keys
		if (e.altKey || e.ctrlKey || e.metaKey) { return; }

		var currentSlideNumber = getCurrentSlideNumber(),
			innerNavigationCompleted = true;

		switch (e.which) {
			case 116: // F5
			case 13: // Enter
				if (isListMode() && -1 !== currentSlideNumber) {
					e.preventDefault();

					history.pushState(null, null,
                                      fullUrl(url.pathname, 'full',
                                            getSlideHash(currentSlideNumber)));
					enterSlideMode();

					updateProgress(currentSlideNumber);
					updateCurrentAndPassedSlides(currentSlideNumber);
					runSlideshowIfPresented(currentSlideNumber);
				}
			break;

			case 27: // Esc
				if (!isListMode()) {
					e.preventDefault();

					history.pushState(null, null,
                                      url.pathname
                                      + getSlideHash(currentSlideNumber));
					enterListMode();
					scrollToSlide(currentSlideNumber);
				}
			break;

			case 33: // PgUp
			case 38: // Up
			case 37: // Left
			case 72: // h
			case 75: // k
				e.preventDefault();

				currentSlideNumber--;
				goToSlide(currentSlideNumber);
			break;

			case 34: // PgDown
			case 40: // Down
			case 39: // Right
			case 76: // l
			case 74: // j
				e.preventDefault();

				if (!isListMode() ) {
					// Inner navigation is "completed" if current slide have
					// no inner navigation or inner navigation is fully shown
					innerNavigationCompleted = !slideList[currentSlideNumber].hasInnerNavigation ||
						-1 === increaseInnerNavigation(currentSlideNumber);
				} else {
					// Also inner navigation is always "completed" if we are in
					// list mode
					innerNavigationCompleted = true;
				}
				// NOTE: First of all check if there is no current slide
				if (
					-1 === currentSlideNumber || innerNavigationCompleted
				) {
					currentSlideNumber++;
					goToSlide(currentSlideNumber);
					// We must run slideshow only in full mode
					if (!isListMode()) {
						runSlideshowIfPresented(currentSlideNumber);
					}
				}
			break;

			case 36: // Home
				e.preventDefault();

				currentSlideNumber = 0;
				goToSlide(currentSlideNumber);
			break;

			case 35: // End
				e.preventDefault();

				currentSlideNumber = slideList.length - 1;
				goToSlide(currentSlideNumber);
			break;

			case 9: // Tab = +1; Shift + Tab = -1
			case 32: // Space = +1; Shift + Space = -1
				e.preventDefault();

				currentSlideNumber += e.shiftKey ? -1 : 1;
				goToSlide(currentSlideNumber);
			break;
            case 80: // p for presenter
                presenterWin = open(window.location.pathname + '?presenter=1'
                                    + "&full"
                                    + getSlideHash(currentSlideNumber));
            break;

			default:
				// Behave as usual
		}
	}, false);

	document.addEventListener('click', dispatchSingleSlideMode, false);
	document.addEventListener('touchend', dispatchSingleSlideMode, false);

	document.addEventListener('touchstart', function (e) {
		if (!isListMode()) {
			var currentSlideNumber = getCurrentSlideNumber(),
				x = e.touches[0].pageX;
			if (x > window.innerWidth / 2) {
				currentSlideNumber++;
			} else {
				currentSlideNumber--;
			}

			goToSlide(currentSlideNumber);
		}
	}, false);

	document.addEventListener('touchmove', function (e) {
		if (!isListMode()) {
			e.preventDefault();
		}
	}, false);


    if (getParamByName('presenter') != "") {
        addClass(document.body, 'presenter_view');
    }
}());
