(function($){$.extend($.easing,{spincrementEasing:function(x,t,b,c,d){return(t===d)?b+c:c*(-Math.pow(2,-10*t/d)+1)+b}})
$.fn.spincrement=function(opts){var defaults={from:0,to:null,decimalPlaces:null,decimalPoint:'.',thousandSeparator:',',duration:1000,leeway:50,easing:'spincrementEasing',fade:true,complete:null}
var options=$.extend(defaults,opts)
var re_thouSep=new RegExp(/^(-?[0-9]+)([0-9]{3})/)
function format(num,dp){num=num.toFixed(dp)
if((dp>0)&&(options.decimalPoint!=='.')){num=num.replace('.',options.decimalPoint)}if(options.thousandSeparator){while(re_thouSep.test(num)){num=num.replace(re_thouSep,'$1'+options.thousandSeparator+'$2')}}return num}return this.each(function(){var obj=$(this)
var from=options.from
if(obj.attr('data-from')){from=parseFloat(obj.attr('data-from'))}var to
if(obj.attr('data-to')){to=parseFloat(obj.attr('data-to'))}else if(options.to!==null){to=options.to}else{var ts=$.inArray(options.thousandSeparator,['\\','^','$','*','+','?','.'])>-1?'\\'+options.thousandSeparator:options.thousandSeparator
var re=new RegExp(ts,'g')
to=parseFloat(obj.text().replace(re,''))}var duration=options.duration
if(options.leeway){duration+=Math.round(options.duration*((Math.random()*2)-1)*options.leeway/100)}var dp
if(obj.attr('data-dp')){dp=parseInt(obj.attr('data-dp'),10)}else if(options.decimalPlaces!==null){dp=options.decimalPlaces}else{var ix=obj.text().indexOf(options.decimalPoint)
dp=(ix>-1)?obj.text().length-(ix+1):0}obj.css('counter',from)
if(options.fade)obj.css('opacity',0)
obj.animate({counter:to,opacity:1},{easing:options.easing,duration:duration,step:function(progress){obj.html(format(progress*to,dp))},complete:function(){obj.css('counter',null)
obj.html(format(to,dp))
if(options.complete){options.complete(obj)}}})})}})(jQuery)