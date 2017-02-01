/**
 * Script for making multiple numbers in a textfield incrementable/decrementable (like Firebug's CSS values)
 * @author Lea Verou
 * @version 1.1
 */
 
(function(){

/**
 * Constructor
 * @param textField {HTMLElement} An input or textarea element
 * @param multiplier {Function} A function that accepts the event object and returns the multiplier or 0 for nothing to happen.
 */
var _ = window.Incrementable = function(textField, multiplier, units) {
	var me = this;

	this.textField = textField;
	
	this.step = +textField.getAttribute('step') || 
				+textField.getAttribute('data-step') || 1;

	this.multiplier = multiplier || function(evt) {
		if(evt.shiftKey) { return 10; }
		
		if(evt.ctrlKey) { return .1; }
		
		return 1;
	}

	if(units) {
		this.units = units;
	}
	
	this.changed = false;

	this.textField.addEventListener('keydown', function(evt) {
		var multiplier = me.multiplier(evt);
		
		if(multiplier && (evt.keyCode == 38 || evt.keyCode == 40)) {
			me.changed = false;
			
			// Up or down arrow pressed, check if there's something
			// increment/decrement-able where the caret is
			var caret = this.selectionStart, text = this.value,
				regex = new RegExp('^([\\s\\S]{0,' + caret + '}[^-0-9\\.])(-?[0-9]*(?:\\.?[0-9]+)(?:' + me.units + '))\\b', 'i'),
				property = 'value' in this? 'value' : 'textContent';
			
			this[property] = this[property].replace(regex, function($0, $1, $2) {
				if($1.length <= caret && $1.length + $2.length >= caret) {
					me.changed = true;
					var stepValue = me.stepValue($2, evt.keyCode == 40, multiplier);
					caret = caret + (stepValue.length - $2.length);
					return $1 + stepValue;
				}
				else {
					return $1 + $2;
				}
			});

			if(me.changed) {
				this.setSelectionRange(caret, caret);
				
				evt.preventDefault();
				evt.stopPropagation();
			}
		}
	}, false);

	this.textField.addEventListener('keypress', function(evt) {
		if(me.changed && (evt.keyCode == 38 || evt.keyCode == 40))
			evt.preventDefault();
			evt.stopPropagation();
			me.changed = false;
	}, false);
}

_.prototype = {
	/**
	 * Gets a <length> and increments or decrements it
	 */
	stepValue: function(length, decrement, multiplier) {
		var val = parseFloat(length),
			offset = (decrement? -1 : 1) * (multiplier || 1) * this.step,
			valPrecision = precision(val),
			offsetPrecision = precision(offset);
		
		// Prevent rounding errors
		var newVal = (parseFloat((val + offset).toPrecision(
			Math.max(valPrecision.integer, offsetPrecision.integer) +
			Math.max(valPrecision.decimals, offsetPrecision.decimals)
		)));
		
		return newVal + length.replace(/^-|[0-9]+|\./g, '');
	},

	units: '|%|deg|px|r?em|ex|ch|in|cm|mm|pt|pc|vmin|vw|vh|gd|m?s'
};

function precision(number) {
	number = (number + '').replace(/^0+/, '');
	
	var dot = number.indexOf('.');
	
	if (dot === -1) {
		return {
			integer: number.length,
			decimals: 0
		};
	}
	
	return {
		integer: dot,
		decimals: number.length - 1 - dot
	};
}

})();
