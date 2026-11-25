'use strict';
hexo.extend.generator.register('compact-search',function(locals){const rows=locals.posts.sort('-date').map(p=>{const categories=p.categories.map(c=>c.name),tags=p.tags.map(t=>t.name);return {title:p.title,url:hexo.config.root+p.path,date:p.date.format('YYYY-MM-DD'),categories,search:[p.title,...categories,...tags,String(p.description||p.summary||'').slice(0,180)].join(' ').toLocaleLowerCase()}});return {path:'search-index.json',data:JSON.stringify(rows)}});
hexo.extend.generator.register('static-404',function(){return {path:'404.html',layout:'404',data:{title:'页面不存在'}}});
