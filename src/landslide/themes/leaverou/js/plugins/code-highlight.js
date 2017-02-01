/**
 * Super simple syntax highlighting plugin for CSSS code snippets
 * Usage: <code lang="javascript">
 * @author Lea Verou
 */

(function(){ 

var _ = window.Highlight = {
	languages: {
		javascript: {
			'comment': /(\/\*.*?\*\/)|\/\/.*?(\r?\n|$)/g,
			'regex': /\/(\\?.)+?\/[gim]{0,3}/g,
			'string': /(('|").*?(\2))/g, // used to be: /'.*?'|".*?"/g,
			'keyword': /\b(var|let|if|else|while|do|for|return|in|instanceof|function|new|with|typeof|try|catch|finally|null)\b/g,
			'boolean': /\b(true|false)\b/g,
			'number': /\b-?(0x)?\d*\.?\d+\b/g,
			'operator': /([-+!=<>]|&lt;){1,3}/g,
			'ignore': /&(lt|gt|amp);/gi,
			'punctuation': /[{}[\];(),.]/g
		},
		css: {
			'comment': /\/\*[\w\W]*?\*\//g,
			'url': /url\((?:'|")?(.+?)(?:'|")?\)/gi,
			'atrule': /@[\w-]+?(\s+[^{]+)?(?=\s*{)/gi,
			'selector': /[^\{\}\s][^\{\}]+(?=\s*\{)/g,
			'property': /(\b|\B)[a-z-]+(?=\s*:)/ig,
			'important': /\B!important\b/gi,
			'ignore': /&(lt|gt|amp);/gi,
			'punctuation': /[\{\};:]/g
		},
		html: {
			'comment': /&lt;!--[\w\W]*?--(>|&gt;)/g,
			'tag': {
				'pattern': /(&lt;|<)\/?[\w\W]+?(>|&gt;)/gi,
				'inside': {
					'attr-value': {
						'pattern': /[\w:-]+=(('|").*?(\2)|[^\s>]+(?=>|&|\s))/gi,
						'inside': {
							'attr-name': /^[\w:-]+(?==)/gi,
							'punctuation': /=/g
						}
					},
					'attr-name': /\s[\w:-]+(?=\s)/gi,
					'punctuation': /&lt;\/?|\/?&gt;/g
				}
			},
			'entity': /&amp;#?[\da-z]{1,8};/gi
		}
	},
	
	isInited: function(code) {
		return code.hasAttribute('data-highlighted');
	},
	
	init: function(code) {
		if(!code || _.isInited(code)) {
			return; // or should I rehighlight?
		}
		
		var lang = _.languages[code.getAttribute('lang')];
		
		if(!lang) {
			return;
		}
		
		code.normalize();
		
		var text = code.textContent
					.replace(/&/g, '&amp;')
					.replace(/</g, '&lt;')
					.replace(/>/g, '&gt;')
					.replace(/\u00a0/g, ' ');
		
		code.innerHTML = _.do(text, lang);
		
		code.setAttribute('data-highlighted', 'true');
	},
	
	do: function(text, tokens) {
		var strarr = [text];
								
		for(var token in tokens) {
			var pattern = tokens[token], 
				inside = pattern.inside;
			pattern = pattern.pattern || pattern;
			
			for(var i=0; i<strarr.length; i++) {
				
				var str = strarr[i];
				
				if(str.token) {
					continue;
				}
				
				pattern.lastIndex = 0;
				var match = pattern.exec(str);
				
				if(match) {
					var to = pattern.lastIndex,
						match = match[0],
						len = match.length,
						from = to - len,
						before = str.slice(0, from),
						after = str.slice(to); 
					
					
					strarr.splice(i, 1);
					
					if(before) {
						strarr.splice(i++, 0, before);
					}
					
					var wrapped = 
						new String(
							_.wrap(
								token,
								inside && (before || after)? _.do(match, inside) : match
							)
						);
					
					wrapped.token = true;
					strarr.splice(i, 0, wrapped);
					
					if(after) {
						
						strarr.splice(i+1, 0, after);
					}
				}
			}
		}

		return strarr.join('');
	},
	
	wrap: function(token, content) {
		return '<span class="token ' + token + (token === 'comment'? '" spellcheck="true' : '') + '">' + content + '</span>' 
	},
	
	container: function(container) {
		if(!container) {
			return;
		}
		
		var codes = container.querySelectorAll('code[lang]');
	
		for(var i=0; i<codes.length; i++) {
			Highlight.init(codes[i]);
		}
	}
}

// Highlight current slide
function highlightSlide() {
	_.container(document.getElementById(location.hash.slice(1)));
}

addEventListener('hashchange', highlightSlide, false);
addEventListener('DOMContentLoaded', highlightSlide, false);

})();