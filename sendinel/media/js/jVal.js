/*
 * jVal - dynamic jquery form field validation framework
 *	version 0.1.5
 * Author: Jim Palmer
 * Released under MIT license.
 */
(function($) {
	// core jVal function - returns TRUE if all jVal validation passes, false if not
	$.fn.jVal = function (options) {
		$.fn.jVal.clean(this);
		// clear jVal warnings
		if ((options || '').toString().toUpperCase() == 'CLEAN')
			return this; // chainable
		$.fn.jVal.defaults = $.extend($.fn.jVal.defaults, options);
		$(this).stop().find('.jfVal,.jValCover').stop().remove();
		var passVal = true, dm = $.fn.jVal.defaults.message, ds = $.fn.jVal.defaults.jvalstyle;
		$(this).find('.jVal,[jVal]:not(:disabled):visible').each(
			function () {
				var cmd = $(this).data('jVal');
				if ( typeof cmd !== 'object' ) eval( 'cmd = ' + ( $(this).data('jVal') || $(this).attr('jVal') ) + ';' );
				//$.fn.jVal.clean(this);
				if ( cmd instanceof Object && cmd.valid instanceof RegExp && !cmd.valid.test($(this).val()) ) {
					$.fn.jVal.showWarning(cmd.target || this, cmd.message || dm, cmd.autoHide || false, cmd.styleType || ds);
					passVal = false;
				} else if ( cmd instanceof Object && cmd.valid instanceof Function ) {
					var testFRet = cmd.valid( $(this).val(), this );
					if ( testFRet === false || testFRet.length > 0 ) {
						$.fn.jVal.showWarning(cmd.target || this, testFRet || cmd.message || dm, cmd.autoHide || false, cmd.styleType || ds);
						passVal = false;
					}
				} else if ( ( cmd instanceof RegExp && !cmd.test($(this).val()) ) || ( cmd instanceof Function && !cmd($(this).val()) ) ) {
					$.fn.jVal.showWarning(cmd.target || this, dm, cmd.autoHide || false, cmd.styleType || ds);
					passVal = false;
				}
			}
		);
		return passVal;
	};
	// showWarning utility function
	$.fn.jVal.showWarning = function (elements, message, autoHide, styleType) {
		var par = $(elements).eq(0).parent();
		clearTimeout( $(par).data('autoHide') ) && $(par).data('autoHide', null);
		$.fn.jVal.clean(par);
		$(elements).css({marginTop:'',position:'',borderColor:'red'});
		var dbw = $.fn.jVal.defaults.border,
			dp = $.fn.jVal.defaults.padding,
			fieldWidth = 0, fieldHeight = 0,
			absoluteLeft = $(elements).eq(0).position().left,
			absoluteTop = $(elements).eq(0).position().top;
		// normalize multi-element coordinates
		$(elements).each(function () {
			fieldWidth += $(this).outerWidth(true);
			fieldHeight = Math.max( $(elements).outerHeight(true), fieldHeight );
			absoluteLeft = Math.min( $(this).position().left, absoluteLeft );
			absoluteTop = Math.min( $(this).position().top, absoluteTop );
		});
		var fwidth = 0, tPos = absoluteTop - dp - dbw, lPos = absoluteLeft + dp, rPos = absoluteLeft + fieldWidth + dp,
			ph = (fieldHeight + (dp * 2)), fhp = fieldHeight + dp + dbw, fwp = fieldWidth + dp,
			clips = [ 
				'rect(0px, 5000px, ' + (dp + dbw) + 'px, 0px)', // top
				'rect(' + fhp + 'px, 5000px, 5000px, 0px)', // bottom
				'rect(' + dp + 'px, ' + dp + 'px, 5000px, 0px)', // left
				'rect(' + dp + 'px, 5000px, 5000px, ' + fwp + 'px)']; // right
		// fixed alerts, no wrapping
		if (!$.fn.jVal.defaults.wrap) {
			fieldWidth = ph = fph = 12;
			rPos = lPos;
		}
		$(elements).eq(0).before(
			'<div class="jValSpacer jValSpacer' + styleType + '" style="line-height:' + ph + 'px; height:' + ph + 'px; clip:' + clips[0] + '; ' +
				'left:' + (absoluteLeft - dp) + 'px; top:' + tPos + 'px; ' + 
				'width:' + (fieldWidth + (dp * 2)) + 'px;" />' +
			'<div class="jfVal' + ( styleType ? ' jfVal' + styleType : '' ) + '" style="left:' + lPos + 'px; ' +
				'top:' + tPos + 'px;">' +
				'<div class="icon' + ( styleType ? ' icon' + styleType : '' ) + '" style="height:' + ph + 'px;"><div class="iconbg" /></div>' +
				'<div class="content' + ( styleType ? ' content' + styleType : '' ) + '" style="height:' + ph + 'px; line-height:' + ph + 'px;">' +
					'<span class="message' + styleType + '">' + message + '</span>' +
				'</div>' +
			'</div>')
			.parent().find('.jfVal>*').each(function () { fwidth += $(this).outerWidth() }).end()
			.find('.jfVal').width(fwidth + 20);
		for (var si = 1; si < 4; si++) 
			$(par).find('.jValSpacer:first').before( 
				$(par).find('.jValSpacer:first').clone().css({clip:clips[si]}) );
		// autoHide = set spacer width + add autohide function to fx queue
		if ( autoHide )
			$(par).data( 'autoHide', setTimeout(function () { $(par).find('.jfVal').animate({left:lPos,opacity:0}, 200, function () { $.fn.jVal.clean(par); }); }, 10000) )
				.find('.jfVal').css({'left':rPos});
		else
			$(par).find('.jfVal').css({opacity:0}).animate({left:rPos,opacity:1}, 200);
	};
	// validate key stroke
	$.fn.jVal.valKey = function (keyRE, e, cF, cA) {
		var ek = (typeof(e.keyCode) != 'undefined'), ec = (typeof(e.charCode) != 'undefined'),
			k = e.keyCode, c = e.charCode, ks = k.toString();
		// return if invalid regex
		if ( !(keyRE instanceof RegExp) ) 
			return false;
		// test for ENTER key and cF being valid function otherwise return true
		if ( /^13$/.test(String(k || c)) ) {
			try { (this[cF]) ? this[cF](cA) : eval(cF); } catch(e) { return true; }
			return -1;
		}
		// otherwise test for valid keys supported by the regex allowing meta keys by default
		if	( e.ctrlKey || e.shiftKey || e.metaKey || (
				ek && k > 0 && keyRE.test(String.fromCharCode(k)) ) ||
				( ec && c > 0 && String.fromCharCode(c).search(keyRE) != (-1) ) ||
				( ec && c != k && ek && ks.search(/^(8|9|45|46|35|36|37|39)$/) != (-1) ) ||
				( ec && c == k && ek && ks.search(/^(8|9)$/) != (-1) ||
				( !ec && ek && ks.search(/^(8|9|45|46|35|36|37|39)$/) != (-1) ) ) 
			) {
			return 1;
		} else {
			return 0;
		}
	};
	// clear all displayed jVal warnings within scope
	$.fn.jVal.clean = function (target) {
		$(target)
			.find('.jfVal,.jValSpacer').stop().remove().end()
			.find('.jVal,[jVal]').css({position:'',borderColor:'',left:'0px',top:'0px'}).parent().find('.jValRelWrap').remove();
	};
	$.fn.jVal.init = function (options) {
		$.fn.jVal.defaults = $.extend($.fn.jVal.defaults, options);
		$('.jVal,[jVal]').filter(':not(:disabled)').unbind("blur").bind("blur", function (e) { 
			if ($.fn.jVal.defaults.blurCheck || $(this).hasClass('jValBlur'))
				$(this).parent().jVal();
		});
		var keyFunc = function (e) {
			eval( 'var cmd = ' + ( $(this).data('jValKey') || $(this).attr('jValKey') || $(this).data('jValKeyUp') || $(this).attr('jValKeyUp') ) + ';' );
			var keyTest, ds = $.fn.jVal.defaults.jvalstyle, dkm = $.fn.jVal.defaults.keyMessage,
				autoHide = typeof(cmd.autoHide) != 'undefined' ? cmd.autoHide : true;
			if ( cmd instanceof Object && cmd.valid instanceof Function ) {
				keyTest = cmd.valid( e, this );
				if ( keyTest === false || keyTest.length > 0 ) {
					$.fn.jVal.clean(cmd.target || this);
					// only show warning and allow keypress event to return true
					$.fn.jVal.showWarning(cmd.target || this, ( keyTest || (cmd.message || dkm).replace('%c', String.fromCharCode(e.keyCode || e.charCode))), autoHide, cmd.styleType || ds);
				} else 
					$.fn.jVal.clean($(cmd.target || this).parent());
			} else {
				keyTest = $.fn.jVal.valKey( ( (cmd instanceof Object) ? cmd.valid : cmd ), e, (cmd instanceof Object) ? cmd.cFunc : null, (cmd instanceof Object) ? cmd.cArgs : null );
				if ( keyTest == 0 ) {
					$.fn.jVal.clean(cmd.target || this);
					$.fn.jVal.showWarning(cmd.target || this, (( cmd instanceof Object && cmd.message) || dkm).replace('%c', String.fromCharCode(e.keyCode || e.charCode)), autoHide, cmd.styleType || ds);
					return false;
				} else if ( keyTest == -1 ) 
					return false;
				else 
					$.fn.jVal.clean($(cmd.target || this).parent());
			}
			return true;
		};
		$('.jValKey,[jValKey]').filter(':not(:disabled)').unbind("keypress").bind("keypress", keyFunc);
		$('.jValKeyUp,[jValKeyUp]').filter(':not(:disabled)').unbind("keyup").bind("keyup", keyFunc);
		return this; // chainable
	};
	// jVal defaults
	$.fn.jVal.defaults = {
		blurCheck: false,
		message: 'Invalid entry',
		jvalstyle: 'cover',
		keyMessage: '"%c" Invalid character',
		padding: 3,
		border: 1,
		wrap: true
	};
	// automatically init on dom load
	$($.fn.jVal.init);
})(jQuery);
