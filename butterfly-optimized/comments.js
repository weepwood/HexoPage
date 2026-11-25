/* Public read-only GitHub API; posting always takes place in GitHub's authenticated UI. */
;(()=>{'use strict';
const section=document.querySelector('#halo-comments');if(!section)return;
const status=section.querySelector('.halo-comment-status'),list=section.querySelector('.halo-comment-list'),primary=section.querySelector('.halo-comment-primary'),retry=section.querySelector('.halo-comment-retry'),create=section.querySelector('.halo-comment-new');
const repo='weepwood/HexoPage',key=section.dataset.key,original=primary.href;let busy=false;
function text(tag,cls,value){const el=document.createElement(tag);if(cls)el.className=cls;el.textContent=value;return el}
async function get(url){const c=new AbortController(),timer=setTimeout(()=>c.abort(),10000);try{const r=await fetch(url,{signal:c.signal,headers:{Accept:'application/vnd.github+json'}});if(!r.ok)throw Error(String(r.status));return await r.json()}finally{clearTimeout(timer)}}
function comment(c){const el=text('article','halo-comment-item','');const head=text('div','halo-comment-meta','');const name=text('strong','',c.user?.login||'GitHub 用户');head.append(name);if(c.created_at){const time=text('time','',new Date(c.created_at).toLocaleDateString('zh-CN'));time.dateTime=c.created_at;head.append(time)}const body=text('p','halo-comment-body',c.body||'');el.append(head,body);return el}
async function load(){if(busy)return;busy=true;retry.hidden=true;create.hidden=true;status.textContent='正在加载 GitHub 讨论…';list.replaceChildren();primary.href=original;primary.textContent='前往 GitHub 讨论';try{
const result=await get('https://api.github.com/search/issues?'+new URLSearchParams({q:section.dataset.query,per_page:'20'}));if(result.incomplete_results||!Array.isArray(result.items))throw Error('Incomplete search');
const threads=result.items.filter(x=>!x.pull_request&&x.title?.includes('['+key+']')&&Number.isInteger(x.number));if(!threads.length){status.textContent='暂无讨论，欢迎发表第一条评论。';create.hidden=false;primary.href=create.href;primary.textContent='发起讨论';return}
threads.sort((a,b)=>a.number-b.number);const issue=threads[0];primary.href='https://github.com/'+repo+'/issues/'+issue.number+'#new_comment_field';primary.textContent=issue.state==='closed'?'查看已关闭讨论':'登录 GitHub 发表评论';
const comments=issue.comments?await get('https://api.github.com/repos/'+repo+'/issues/'+issue.number+'/comments?per_page=30'):[];
if(!Array.isArray(comments))throw Error('Invalid comments');status.textContent='共 '+(1+issue.comments)+' 条讨论（含首条）'+(threads.length>1?'；发现多个讨论，请通过 GitHub 查看。':'');list.append(comment(issue));for(const c of comments)list.append(comment(c));if(issue.comments>comments.length)list.append(text('p','halo-comment-status','更多评论请在 GitHub 查看。'));
}catch(e){status.textContent='暂时无法加载讨论，可能是网络或 GitHub 请求限制。仍可通过 GitHub 查看或发表评论。';retry.hidden=false}finally{busy=false}}
retry.addEventListener('click',load);const details=section.querySelector('.halo-legacy-comments');if(details){details.addEventListener('toggle',()=>{if(details.open&&!list.children.length)load()});return}if('IntersectionObserver'in window){const io=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){io.disconnect();load()}},{rootMargin:'160px'});io.observe(section)}else load()
})();
