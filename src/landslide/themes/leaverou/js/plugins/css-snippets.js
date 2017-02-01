/**
 * Script to add prefixes to standard CSS3 in textareas or style attributes
 * Requires css-edit.js
 * @author Lea Verou
 * MIT License
 */

(function(head) {

var self = window.CSSSnippet = function(element) {
	var me = this;
	
	// this holds the elements the CSS is gonna be applied to
	this.subjects = CSSEdit.getSubjects(element);
	
	CSSEdit.setupSubjects(this.subjects);

	// Test if its text field first
	if(/^(input|textarea)$/i.test(element.nodeName)) {
		this.textField = element;
		
		// Turn spellchecking off
		this.textField.spellcheck = false;
		
		CSSEdit.elastic(this.textField);
		
		var supportsInput = 'oninput' in this.textField;
		
		this.textField.addEventListener('input', function() {
			me.update();
		});
		
		this.textField.addEventListener('keydown', function(evt) {
			var code = evt.keyCode;

			if(
				(evt.metaKey || evt.ctrlKey) 
				&& !evt.altKey 
				&& [48, 61, 109, 187, 189].indexOf(code) > -1
			  ) { // 0, +, -
			  
				var fontSize;
	
				if(code === 48) {
					fontSize = 100;
				}
				else {
					fontSize = (code == 61 || code == 187? 10 : -10) + (+this.getAttribute('data-size') || 100);
				}
				
				evt.preventDefault();
				
				if(40 <= fontSize && fontSize <= 200) {
					this.setAttribute('data-size', fontSize);
				}
				
				return false;
			}
			
			me.update();
		});
	}
	
	this.raw = this.getCSS().indexOf('{') > -1;
	
	if (window.SlideShow) {
		this.slide = SlideShow.getSlide(element);
		
		// Remove it after we're done with it, to save on resources
		addEventListener('hashchange', function() {
			if(location.hash == '#' + me.slide.id) {
				me.update();
			}
			else if(me.raw) {
				head.removeChild(me.style);
			}
		}, false);
		
		if(location.hash == '#' + me.slide.id) {
			this.update();
		}
	}
	else {
		this.update();
	}
}

self.prototype = {
	update: function() {
		var code = this.getCSS(),
		    previousRaw = this.raw;
		
		this.raw = code.indexOf('{') > -1;
		
		var supportedStyle = StyleFix.fix(code, this.raw);
		
		if (previousRaw != this.raw) {
			if (previousRaw && !this.raw) {
				head.removeChild(this.style);
			}
			else {
				this.textField.classList.remove('error');
				CSSEdit.updateStyle(this.subjects, '', 'data-originalstyle');
			}
		}
		
		if (this.raw) {
			if (!this.style) {
				this.style = document.createElement('style');
			}
			
			if (!this.style.parentNode) {
				head.appendChild(this.style);
			}
			
			this.style.textContent = supportedStyle;
		}
		else {
			var valid = CSSEdit.updateStyle(this.subjects, code, 'data-originalstyle');
			
			if(this.textField && this.textField.classList) {
				this.textField.classList[valid? 'remove' : 'add']('error');
			}
		}
	},
	
	getCSS: function() {
		return this.textField ? this.textField.value : this.subjects[0].getAttribute('style');
	}
};

var sizeStyles = '';
for(var i=40; i<=200; i++) {
	sizeStyles += '\r\ntextarea[data-size="' + i + '"] { font-size: ' + i + '%; }';
}

var style = document.createElement('style');
style.textContent = sizeStyles;
document.head.appendChild(style);

})(document.head);