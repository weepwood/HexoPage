'use strict';
if (typeof renderMathInElement === 'function') renderMathInElement(document.querySelector('.prose') || document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}],throwOnError:false});
