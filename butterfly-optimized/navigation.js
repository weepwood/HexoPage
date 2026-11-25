/* Keep Butterfly routes/search/sidebar; add accessible desktop dropdown and current route. */
;(()=>{'use strict';
function init(){
 const nav=document.getElementById('nav');if(!nav||nav.dataset.haloNav)return;nav.dataset.haloNav='1';nav.setAttribute('aria-label','主导航');
 const root=new URL(GLOBAL_CONFIG.root,location.origin).pathname,normalize=p=>p.replace(/index\.html$/,'').replace(/\/$/,'');
 for(const link of nav.querySelectorAll('.menus_items a[href]')){
   if(link.protocol!==location.protocol||link.origin!==location.origin)continue;
   const a=normalize(link.pathname),b=normalize(location.pathname);
   if(a===b||(a===normalize(root)&&b.startsWith(normalize(root)+'/page/')&&/\/page\/\d+$/.test(b)))link.setAttribute('aria-current','page');
 }
 for(const item of nav.querySelectorAll('.menus_items>.menus_item')){
   const list=item.querySelector('.menus_item_child'),trigger=item.querySelector(':scope>a.site-page');if(!list||!trigger)continue;
   let timer;const state=open=>{clearTimeout(timer);item.classList.toggle('halo-menu-open',open);trigger.setAttribute('aria-expanded',String(open));list.style.removeProperty('display')};
   trigger.setAttribute('role','button');trigger.setAttribute('aria-expanded','false');trigger.setAttribute('aria-controls','halo-nav-links');list.id='halo-nav-links';
   item.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse')state(true)});
   item.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse')timer=setTimeout(()=>{if(!item.contains(document.activeElement))state(false)},140)});
   trigger.addEventListener('click',e=>{e.preventDefault();state(!item.classList.contains('halo-menu-open'))});
   trigger.addEventListener('keydown',e=>{if(e.key===' '||e.key==='ArrowDown'){e.preventDefault();state(true);list.querySelector('a')?.focus()}});
   item.addEventListener('focusout',e=>{if(!item.contains(e.relatedTarget))state(false)});
   document.addEventListener('pointerdown',e=>{if(!item.contains(e.target))state(false)});
   item.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();state(false);trigger.focus()}});
 }
 for(const [selector,label] of [['#search-button a','搜索'],['#toggle-menu a','打开导航菜单']]){
   const el=nav.querySelector(selector);if(!el)continue;el.tabIndex=0;el.setAttribute('role','button');el.setAttribute('aria-label',label);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click()}});
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
