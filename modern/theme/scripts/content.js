'use strict';
// Preserve source HTML while deferring heavy historical media on article pages.
hexo.extend.filter.register('after_post_render',function(data){
 if(typeof data.content!=='string')return data;
 data.content=data.content.replace(/<img\b(?![^>]*\bloading\s*=)([^>]*)>/gi,'<img loading="lazy" decoding="async"$1>').replace(/<iframe\b(?![^>]*\bloading\s*=)([^>]*)>/gi,'<iframe loading="lazy"$1>');
 return data;
});
