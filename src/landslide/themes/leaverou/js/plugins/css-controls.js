/**
 * Script to make form controls control CSS styles
 * Requires css-edit.js
 * @author Lea Verou
 * MIT License
 */

(function(){

var self = window.CSSControl = function(control) {
	var me = this;
	
	this.control = control;
	
	// this holds the elements the CSS is gonna be applied to
	this.subjects = CSSEdit.getSubjects(control);
	
	CSSEdit.setupSubjects(control);
	
	control.addEventListener('input', function() {
		me.update();
	}, false);
	
	control.addEventListener('change', function() {
		me.update();
	}, false);
	
	this.update();
};

self.prototype = {
	update: function() {
		// Get code
		var code = this.control.getAttribute('data-style').replace(/\{value\}/gi, this.control.value);
		
		CSSEdit.updateStyle(this.subjects, code, 'style');
	}
};

})();