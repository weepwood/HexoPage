"""One-shot migration from rendered old pages, never used during normal site builds."""
import argparse, concurrent.futures, hashlib, html, io, json, re, subprocess, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit, quote, unquote
from html.parser import HTMLParser
from PIL import Image, ImageOps
from collections import Counter
class Scan(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.urls=set()
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        for k,v in attrs:
            if not v:continue
            if (tag in ('img','image') and k in ('src','data-src','data-lazy-src','data-original','href','xlink:href')) or k=='poster' or (tag=='meta' and k=='content' and d.get('property') in ('og:image','twitter:image')):
                if v.startswith(('http://','https://','//')):self.urls.add(v)
            if k=='style':self.urls.update(re.findall(r'url\([\x22\x27]?(https?://[^\s\x22\x27)]+)',v))
def main():
    a=argparse.ArgumentParser();a.add_argument('rendered',type=Path);a.add_argument('--workers',type=int,default=16);args=a.parse_args()
    repo=Path(__file__).resolve().parents[1];out=repo/'source/images/archive';out.mkdir(parents=True,exist_ok=True)
    manifest=repo/'butterfly-optimized/assets/images.json'; scan=Scan()
    for f in args.rendered.rglob('*.html'):
        try:scan.feed(f.read_text())
        except Exception: pass
    for i in list(range(1,16))+['flow1','flow2']:
        suffix=f'i{i}' if isinstance(i,int) else i
        scan.urls.add('https://cdn.jsdelivr.net/gh/halo-blog/cdn-blog-img-a@main/BilibiliBannerSpring/'+suffix+'.png')
    previous=json.loads(manifest.read_text()) if manifest.exists() else {}
    def fetch(url):
        if previous.get(url,{}).get('file') and (repo/'source'/previous[url]['file'].lstrip('/')).is_file():return url,previous[url]
        candidates=[('https:'+url if url.startswith('//') else url)]
        if url.startswith('http://'):candidates.insert(0,'https://'+url[7:])
        match=re.match(r'https?://cdn\.jsdelivr\.net/gh/([^/]+/[^@/]+)@([^/]+)/(.+)',url)
        if match:candidates.append('https://raw.githubusercontent.com/'+match[1]+'/'+match[2]+'/'+match[3])
        for candidate in candidates:
            # No URL credentials; only static public sources.
            if urlsplit(candidate).username:continue
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'download'
                try:
                    result=subprocess.run(['curl','-fsSL','--connect-timeout','4','--max-time','14','--max-filesize','20000000','-A','Mozilla/5.0','-o',str(p),quote(unquote(candidate),safe=":/?&=%#@!$+,;~()*[]")],capture_output=True,timeout=16)
                    if result.returncode or not p.exists():continue
                    data=p.read_bytes()
                    if urlsplit(url).path.lower().endswith('.svg'):
                        # SVG may contain active content; render in Chromium as an image, never inline.
                        if b'<svg' not in data or len(data)>10000000:continue
                        root=ET.fromstring(data)
                        if root.tag.rsplit('}',1)[-1]!='svg':continue
                        # Reject active scripting and external loads. Keep diagram labels and local fragment references.
                        if re.search(rb'<(?:[a-z]+:)?(?:script|iframe|object|embed)\b|\bon[a-z]+\s*=|javascript:|@import',data,re.I):continue
                        for el in root.iter():
                            for k,v in el.attrib.items():
                                if k.rsplit('}',1)[-1] in ('href','src') and not (v.startswith('#') or v.startswith('data:image/')):raise ValueError('external SVG reference')
                        if re.search(rb'url\(\s*[\"\x27]?(?:https?:)?//',data,re.I):continue
                        name=hashlib.sha256(data).hexdigest()[:24]+'.svg';(out/name).write_bytes(data)
                        return url,{'file':'/images/archive/'+name,'bytes':len(data),'original_bytes':len(data),'format':'svg'}
                    with Image.open(io.BytesIO(data)) as im:
                        fmt=im.format
                        if fmt not in ('PNG','JPEG','WEBP','GIF','BMP','AVIF','TIFF','ICO'):continue
                        if getattr(im,'is_animated',False):
                            if fmt not in ('GIF','WEBP'):continue
                            content=data; ext=fmt.lower(); width,height=im.size
                        else:
                            im=ImageOps.exif_transpose(im)
                            banner='BilibiliBannerSpring/' in url
                            if not banner:im.thumbnail((1800,1800),Image.Resampling.LANCZOS)
                            alpha='A' in im.getbands() or 'transparency' in im.info
                            im=im.convert('RGBA' if alpha else 'RGB');width,height=im.size
                            buf=io.BytesIO();im.save(buf,format='WEBP',quality=90 if banner else 85,method=4);content=buf.getvalue();ext='webp'
                            if not banner and fmt in ('PNG','JPEG','WEBP') and len(data)<len(content) and width==Image.open(io.BytesIO(data)).width and height==Image.open(io.BytesIO(data)).height:content=data;ext={'PNG':'png','JPEG':'jpg','WEBP':'webp'}[fmt]
                    name=hashlib.sha256(content).hexdigest()[:24]+'.'+ext;(out/name).write_bytes(content)
                    return url,{'file':'/images/archive/'+name,'bytes':len(content),'original_bytes':len(data),'width':width,'height':height}
                except Exception: continue
        return url,{'status':'unavailable'}
    result={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i,(url,row) in enumerate(pool.map(fetch,sorted(scan.urls)),1):
            result[url]=row
            if i%25==0:print('PROGRESS',i,'/',len(scan.urls),'ok',sum('file' in v for v in result.values()),flush=True)
            if i%50==0:manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('DONE',len(result),Counter('ok' if 'file'in v else 'unavailable' for v in result.values()),'unique files',len(list(out.iterdir())),flush=True)
if __name__=='__main__':main()
