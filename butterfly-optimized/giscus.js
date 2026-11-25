/* Giscus official widget, lazy mount, strict article mapping and origin-checked messages. */
;(()=>{
  'use strict'
  const section=document.getElementById('halo-comments')
  if(!section)return
  const mount=section.querySelector('.giscus'), status=section.querySelector('.halo-giscus-status')
  const retry=section.querySelector('.halo-giscus-retry'), fallback=section.querySelector('.halo-legacy-comments')
  const origin='https://giscus.app'
  let timer,script,loading=false,ready=false,fatal=false
  const theme=()=>document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light'
  function sync(){
    const iframe=mount.querySelector('iframe.giscus-frame')
    iframe?.contentWindow?.postMessage({giscus:{setConfig:{theme:theme()}}},origin)
  }
  function failure(message){
    clearTimeout(timer);loading=false;ready=false;fatal=true
    status.textContent=message;status.hidden=false;retry.hidden=false;fallback.hidden=false
  }
  function loaded(){
    clearTimeout(timer);loading=false;ready=true;status.hidden=true;retry.hidden=true;sync()
  }
  function load(){
    if(loading||ready)return
    // A mounted official client has its own window listener; retry by reloading the page,
    // not injecting multiple clients and duplicating OAuth handling.
    if(script){location.reload();return}
    loading=true;retry.hidden=true;status.hidden=false;status.textContent='正在加载站内评论…'
    let cfg
    try{cfg=JSON.parse(section.dataset.giscus)}catch{failure('评论配置无法读取。');return}
    script=document.createElement('script');script.src=origin+'/client.js';script.async=true;script.crossOrigin='anonymous'
    for(const [key,value] of Object.entries({...cfg,term:section.dataset.key,theme:theme()}))script.dataset[key]=value
    script.addEventListener('error',()=>failure('评论服务暂时无法连接，可重试或使用 GitHub 备用入口。'),{once:true})
    timer=setTimeout(()=>failure('评论加载超时，可重试或使用 GitHub 备用入口。'),15000)
    section.appendChild(script)
  }
  window.addEventListener('message',event=>{
    const frame=mount.querySelector('iframe.giscus-frame')
    if(event.origin!==origin||!frame||event.source!==frame.contentWindow||!event.data?.giscus)return
    const data=event.data.giscus
    if(typeof data.error==='string'){
      if(data.error.includes('Discussion not found')){fatal=false;loaded();return}
      if(/Bad credentials|Invalid state value|State has expired/i.test(data.error)){return}
      if(/not installed/i.test(data.error)){failure('站内评论尚待仓库管理员完成 Giscus 授权，暂可使用 GitHub 备用入口。');return}
      failure('评论服务暂时不可用，请重试或使用备用入口。');return
    }
    if(!fatal&&((typeof data.resizeHeight==='number'&&data.resizeHeight>0)||data.discussion)){loaded()}
  })
  new MutationObserver(sync).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']})
  retry.addEventListener('click',load)
  // OAuth return must initialize even when the comment section is not visible.
  if(new URL(location.href).searchParams.has('giscus'))load()
  else if('IntersectionObserver' in window){const io=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){io.disconnect();load()}},{rootMargin:'240px'});io.observe(section)}
  else load()
})();
