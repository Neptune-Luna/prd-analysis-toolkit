"""Render business release notes into one portable HTML file, with embedded images."""
import argparse
import base64
import datetime as dt
import html
import json
import re
from pathlib import Path


def render(data, source_dir):
    date=dt.date.fromisoformat(data['release_date'])
    if type(data.get('released')) is not bool:
        raise ValueError('released must be an explicit boolean')
    title=f'{date.year}年{date.month}月{date.day}日版本更新内容说明'
    modules=data.get('modules')
    if not modules:
        raise ValueError('At least one reviewed module is required')
    nav=[]; sections=[]; ids=set()
    for n, module in enumerate(modules,1):
        key=module['id']
        if not re.fullmatch(r'[a-z][a-z0-9-]*',key) or key in ids:
            raise ValueError(f'Invalid or duplicate module id: {key}')
        ids.add(key)
        label=html.escape(module['title'])
        nav.append(f'<a href="#{key}">{n:02d}　{label}</a>')
        blocks=[]
        if not module.get('blocks'):
            raise ValueError(f'Empty module: {key}')
        for block in module['blocks']:
            if ('html' in block)==('image' in block):
                raise ValueError('Each block must contain exactly one of html/image')
            if 'html' in block:
                blocks.append(block['html'])
                continue
            path=(source_dir/block['image']).resolve()
            raw=path.read_bytes()
            if raw.startswith(b'\x89PNG\r\n\x1a\n'): mime='image/png'
            elif raw.startswith(b'\xff\xd8\xff'): mime='image/jpeg'
            elif raw.startswith(b'RIFF') and raw[8:12]==b'WEBP': mime='image/webp'
            else: raise ValueError(f'Unsupported or invalid screenshot: {path}')
            image_title=html.escape(block['title'],quote=True)
            caption=html.escape(block['caption'])
            encoded=base64.b64encode(raw).decode('ascii')
            blocks.append(f'<figure class="shot desktop"><img src="data:{mime};base64,{encoded}" alt="{image_title}" tabindex="0" onclick="showShot(this)" onkeydown="if(event.key===\'Enter\')showShot(this)"><figcaption><strong>{image_title}</strong><br>{caption}<span class="shot-source">点击图片可放大。</span></figcaption></figure>')
        sections.append(f'<section id="{key}"><h2><b>{n:02d}</b>{label}</h2>{"".join(blocks)}</section>')
    template=(Path(__file__).resolve().parents[1]/'assets/release-template.html').read_text(encoding='utf-8')
    values={'TITLE':html.escape(title), 'INTRO':html.escape(data.get('intro','')),
        'STATUS':'已发布功能说明' if data['released'] else '待上线功能说明',
        'DATE_LABEL':'上线日期' if data['released'] else '计划上线日期',
        'DATE':f'{date.year}年{date.month}月{date.day}日',
        'TOC':''.join(nav),'CONTENT':''.join(sections)}
    # Single-pass replacement: supplied prose must not be interpreted as template syntax.
    result=re.sub(r'@@([A-Z_]+)@@',lambda m:values[m.group(1)],template)
    if not data.get('show_release_status', False):
        result=result.replace('<span>文档状态：'+values['STATUS']+'</span>', '')
        result=result.replace(values['DATE_LABEL']+'：', '上线日期：')
    return title,result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args()
    title,result=render(json.loads(args.input.read_text(encoding='utf-8')),args.input.resolve().parent)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    dest=args.output_dir/(title+'.html')
    dest.write_text(result,encoding='utf-8')
    print(str(dest))


if __name__=='__main__':
    main()
