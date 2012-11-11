/**
 * CSSS javascript code
 * @author Lea Verou (http://leaverou.me)
 * @version 2.0
 */
 
/**
 * Make the environment a bit friendlier
 */
function $(expr, con) { return (con || document).querySelector(expr); }
function $$(expr, con) { return [].slice.call((con || document).querySelectorAll(expr)); }

(function(head, body, html){

// Check for classList support and include the polyfill if it's not supported
if(!('classList' in body)) {
	var thisScript = $('script[src$="slideshow.js"]'),
	    script = document.createElement('script');
	    script.src = thisScript.src.replace(/\bslideshow\.js/, 'classList.js');
	thisScript.parentNode.insertBefore(script, thisScript);
}

// Cache <title> element, we may need it for slides that don't have titles
var documentTitle = document.title + '';

var self = window.SlideShow = function(slide) {
	var me = this;
	
	// Set instance
	if(!window.slideshow) {
		window.slideshow = this;
	}
	
	// Current slide
	this.index = this.slide = slide || 0;
	
	// Current .delayed item in the slide
	this.item = 0;
	
	// Create timer, if needed
	this.duration = body.getAttribute('data-duration');
	
	if(this.duration > 0) {
		var timer = document.createElement('div');
		    
		timer.id = 'timer';
		timer.setAttribute('style', PrefixFree.prefixCSS('transition-duration: ' + this.duration * 60 + 's;'));
		body.appendChild(timer);
		
		addEventListener('load', function() {
			timer.className = 'end';

			setTimeout(function() {
				timer.classList.add('overtime');
			}, me.duration * 60000);
		});
	}
	
	// Create slide indicator
	this.indicator = document.createElement('div');
	
	this.indicator.id = 'indicator';
	body.appendChild(this.indicator);
	
	// Get the slide elements into an array
	this.slides = $$('.slide', body);

	// Get the overview
	this.overview = function(evt) {
        if(body.classList.contains('show-thumbnails')) {
            body.classList.remove('show-thumbnails');
            body.classList.remove('headers-only');
        }
        else {
            body.classList.add('show-thumbnails');
            
            if(evt && (!evt.shiftKey || !evt.ctrlKey)) {
                body.classList.add('headers-only');
            }

            body.addEventListener('click', function(evt) {
                var slide = evt.target;
                
                while(slide && !slide.classList.contains('slide')) {
                    slide = slide.parentNode;
                }
                
                if(slide) {
                    me.goto(slide.id);
                    setTimeout(function() { me.adjustFontSize(); }, 1000); // for Opera
                }
                
                body.classList.remove('show-thumbnails');
                body.classList.remove('headers-only');
                
                body.removeEventListener('click', arguments.callee);
            }, false);
        }
    }
	
	// Order of the slides
	this.order = [];
	
	for(var i=0; i<this.slides.length; i++) {
		var slide = this.slides[i]; // to speed up references
		
		// Asign ids to slides that don't have one
		if(!slide.id) {
			slide.id = 'slide' + (i+1);
		}
		
		// Set data-title attribute to the title of the slide
		if(!slide.title) {
			// no title attribute, fetch title from heading(s)
			var heading = $('hgroup', slide) || $('h1,h2,h3,h4,h5,h6', slide);
			
			if(heading && heading.textContent.trim()) {
				slide.setAttribute('data-title', heading.textContent);
			}
		}
		else {
			// The title attribute is set, use that
			slide.setAttribute('data-title', slide.title);
			slide.removeAttribute('title');
		}
		
		slide.setAttribute('data-index', i);
		
		var imp = slide.getAttribute('data-import'),
			imported = imp? this.getSlideById(imp) : null;
		
		this.order.push(imported? +imported.getAttribute('data-index') : i);
	}
	
	if(window.name === 'projector' && window.opener && opener.slideshow) {
		body.classList.add('projector');
		this.presenter = opener.slideshow;
		this.presenter.projector = this;
	}
	
	// Adjust the font-size when the window is resized
	addEventListener('resize', this, false);
	
	// In some browsers DOMContentLoaded is too early, so try again onload
	addEventListener('load', this, false);
	
	addEventListener('hashchange', this, false);
	
	// If there's already a hash, update current slide number...
	this.handleEvent({type: 'hashchange'});
	
	document.addEventListener('keyup', this, false);
	document.addEventListener('keydown', this, false);
	
	// Process iframe slides
	$$('.slide[data-src]:empty').forEach(function(slide) {
		var iframe = document.createElement('iframe');
		
		iframe.setAttribute('data-src', slide.getAttribute('data-src'));
		slide.removeAttribute('data-src');
		
		slide.appendChild(iframe);
	});
	
	$$('.slide > iframe:only-child').forEach(function(iframe) {
		var slide = iframe.parentNode,
			src = iframe.src || iframe.getAttribute('data-src');
		
		slide.classList.add('iframe');
		
		if(!slide.classList.contains('notitle')) {
			var h = document.createElement('h1'),
			    a = document.createElement('a'),
			    title = iframe.title || slide.title || slide.getAttribute('data-title') || src.replace(/\/#?$/, '')
							 .replace(/^\w+:\/\/w{0,3}\.?/, '');
			
			a.href = src;
			a.target = '_blank';
			a.textContent = title;
			h.appendChild(a);
			
			slide.appendChild(h);
		}
		else {
			var b = document.createElement('button');
			b.className = 'onscreen-nav next';
			b.textContent = 'Next ▶';
			b.type = 'button';
			b.onclick = function() { me.next(); }
			
			slide.appendChild(b);
		}
	});
};

self.prototype = {
	handleEvent: function(evt) {
		var me = this;
		
		switch(evt.type) {
			/**
				Keyboard navigation
				Ctrl+G : Go to slide...
				Ctrl+H : Show thumbnails and go to slide
				Ctrl+P : Presenter view
				(Shift instead of Ctrl works too)
			*/
			case 'keyup':
				if((evt.ctrlKey || evt.shiftKey) && !evt.altKey && !/^(?:input|textarea)$/i.test(document.activeElement.nodeName)) {
					switch(evt.keyCode) {
						case 71: // G
							var slide = prompt('Which slide?');
							me.goto(+slide? slide - 1 : slide);
							break;
						case 72: // H
						    me.overview(evt);
							break;
						case 74: // J
							if(body.classList.contains('hide-elements')) {
								body.classList.remove('hide-elements');
							}
							else {
								body.classList.add('hide-elements');
							}
							break;
						case 80: // P
							// Open new window for attendee view
							this.projector = open(location, 'projector');
		
							// Get the focus back
							window.focus();
							
							// Switch this one to presenter view
							body.classList.add('presenter');
					}
				}
				break;
			case 'keydown':
				/**
					Keyboard navigation
					Home : First slide
					End : Last slide
					Space/Up/Right arrow : Next item/slide
					Ctrl + Space/Up/Right arrow : Next slide
					Down/Left arrow : Previous item/slide
					Ctrl + Down/Left arrow : Previous slide 
					(Shift instead of Ctrl works too)
				*/
				if(evt.target === body || evt.target === body.parentNode || evt.metaKey && evt.altKey) {
					if(evt.keyCode >= 32 && evt.keyCode <= 40) {
						evt.preventDefault();
					}
		
					switch(evt.keyCode) {
						case 33: //page up
							this.previous();
							break;
						case 34: //page down
							this.next();
							break;
						case 35: // end
							this.end();
							break;
						case 36: // home
							this.start();
							break;
						case 37: // <-
						case 38: // up arrow
							this.previous(evt.ctrlKey || evt.shiftKey);
							break;
						case 32: // space
						case 39: // ->
						case 40: // down arrow
							this.next(evt.ctrlKey || evt.shiftKey);
							break;
					}
				}
				break;
			case 'load':
			case 'resize':
				this.adjustFontSize();
				break;
			case 'hashchange':
				this.goto(location.hash.substr(1) || 0);
		}
	},
	
	start: function() {
		this.goto(0);
	},
	
	end: function() {
		this.goto(this.slides.length - 1);
	},
	
	/**
		@param hard {Boolean} Whether to advance to the next slide (true) or 
			just the next step (which could very well be showing a list item)
	 */
	next: function(hard) {
		if(!hard && this.items.length) {
			this.nextItem();
		}
		else {	
			this.goto(this.index + 1);
			
			this.item = 0;
			
			// Mark all items as not displayed, if there are any
			if(this.items.length) {	
				for (var i=0; i<this.items.length; i++) {
					var classes = this.items[i].classList;
					if(classes) {
						classes.remove('displayed');
						classes.remove('current');
					}
				}
			}
		}
	},
	
	nextItem: function() {
		if(this.item < this.items.length) {
			this.gotoItem(++this.item);
		}
		else {
			this.item = 0;
			this.next(true);
		}
	},
	
	previous: function(hard) {
		if(!hard && this.item > 0) {
			this.previousItem();
		}
		else {	
			this.goto(this.index - 1);
			
			this.item = this.items.length;

			// Mark all items as displayed, if there are any
			if(this.items.length) {	
				for (var i=0; i<this.items.length; i++) {
					if(this.items[i].classList) {
						this.items[i].classList.add('displayed');
					}
				}
				
				// Mark the last one as current
				var lastItem = this.items[this.items.length - 1];
				
				lastItem.classList.remove('displayed');
				lastItem.classList.add('current');
			}
		}
	},
	
	previousItem: function() {
		this.gotoItem(--this.item);
	},
	
	getSlideById: function(id) {
		return $('.slide#' + id);
	},
	
	/**
		Go to an aribtary slide
		@param which {String|Integer} Which slide (identifier or slide number)
	*/
	goto: function(which) {
		var slide;
		
		// We have to remove it to prevent multiple calls to goto messing up
		// our current item (and there's no point either, so we save on performance)
		window.removeEventListener('hashchange', this, false);
		
		var id;
		
		if(which + 0 === which && which in this.slides) { 
			// Argument is a valid slide number
			this.index = which;
			this.slide = this.order[which]
			
			slide = this.slides[this.slide];
			
			location.hash = '#' + slide.id;
		}
		else if(which + '' === which) { // Argument is a slide id
			slide = this.getSlideById(which);
			
			if(slide) {
				this.slide = this.index = +slide.getAttribute('data-index');
				location.hash = '#' + which;	
			}
		}
		
		if(slide) { // Slide actually changed, perform any other tasks needed
			document.title = slide.getAttribute('data-title') || documentTitle;
			
			if(slide.classList.contains('iframe')) {
				var iframe = $('iframe', slide), src;
				
				if(!iframe.hasAttribute('src') && (src = iframe.getAttribute('data-src'))) {
					iframe.setAttribute('src', src);
				}
			}
			else {
				this.adjustFontSize();
			}
			
			this.indicator.textContent = this.index + 1;
			
			// Update items collection
			this.items = $$('.delayed, .delayed-children > *', this.slides[this.slide]);
			this.items.sort(function(a, b){
				return (a.getAttribute('data-index') || 0) - (b.getAttribute('data-index') || 0)
			});
			this.item = 0;
			
			this.projector && this.projector.goto(which);
			
			// Update next/previous
			for (var i=this.slides.length; i--;) {
				this.slides[i].classList.remove('previous');
				this.slides[i].classList.remove('next');
			}
			
			this.slides.previous = this.slides[this.order[this.index - 1]];
			this.slides.next = this.slides[this.order[this.index + 1]];
			
			this.slides.previous && this.slides.previous.classList.add('previous');
			this.slides.next && this.slides.next.classList.add('next');
		}
		
		// If you attach the listener immediately again then it will catch the event
		// We have to do it asynchronously
		var me = this;
		setTimeout(function() {
			addEventListener('hashchange', me, false);
		}, 1000);
	},
	
	gotoItem: function(which) {
		this.item = which;
		
		var items = this.items, classes;
		
		for(var i=items.length; i-- > 0;) {
			classes = this.items[i].classList;
			
			classes.remove('current');
			classes.remove('displayed');
		}
		
		for(var i=this.item - 1; i-- > 0;) {
			this.items[i].classList.add('displayed');
		}
		
		if(this.item > 0) {
			this.items[this.item - 1].classList.add('current');
		}
		
		this.projector && this.projector.gotoItem(which);
	},
	
	adjustFontSize: function() {
		// Cache long lookup chains, for performance
		var htmlStyle = html.style,
			scrollRoot = html.scrollHeight? html : body,
			innerHeight = window.innerHeight,
			innerWidth = window.innerWidth,
			slide = this.slides[this.slide];
			
		// Clear previous styles
		htmlStyle.fontSize = '';
		
		if(body.classList.contains('show-thumbnails') 
			|| slide.classList.contains('dont-resize')) {
			return;
		}

		for(
			var percent = 100;	
			(scrollRoot.scrollHeight > innerHeight || scrollRoot.scrollWidth > innerWidth) && percent >= 35;
			percent-=5
		) {
			htmlStyle.fontSize = percent + '%';
		}
		
		// Individual slide

		if(slide.clientHeight && slide.clientWidth) {
			// Strange FF bug: scrollHeight doesn't work properly with overflow:hidden
			var previousStyle = slide.getAttribute('style');
			slide.style.overflow = 'auto';
			
			for(
				;	
				(slide.scrollHeight > slide.clientHeight || slide.scrollWidth > slide.clientWidth) && percent >= 35;
				percent--
			) {
				htmlStyle.fontSize = percent + '%';
			}
			
			slide.setAttribute('style', previousStyle);
		}

		if(percent <= 35) {
			// Something probably went wrong, so just give up altogether
			htmlStyle.fontSize = '';
		}
	},
	
	// Is the element on the current slide?
	onCurrent: function(element) {
		var slide = self.getSlide(element);
		
		if(slide) {
			return '#' + slide.id === location.hash;
		}
		
		return false;
	}
};

/**********************************************
 * Static methods 
 **********************************************/
 
// Helper method for plugins
self.getSlide = function(element) {
	var slide = element;
	
	while (slide && slide.classList && !slide.classList.contains('slide')) {
		slide = slide.parentNode;
	}
	
	return slide;
}

})(document.head || document.getElementsByTagName('head')[0], document.body, document.documentElement);

// Rudimentary style[scoped] polyfill
addEventListener('load', function(){ // no idea why the timeout is needed
	$$('style[scoped]').forEach(function(style) {
		var rulez = style.sheet.cssRules,
			parentid = style.parentNode.id || self.getSlide(style).id || style.parentNode.parentNode.id;

		for(var j=rulez.length; j--;) {
			var selector = rulez[j].selectorText.replace(/^|,/g, function($0) {
				return '#' + parentid + ' ' + $0
			});
			
			var cssText = rulez[j].cssText.replace(/^.+?{/, selector + '{');
			
			style.sheet.deleteRule(j);
			style.sheet.insertRule(cssText, j);
		}
		
	});
});
