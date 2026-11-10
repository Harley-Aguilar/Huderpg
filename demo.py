from html import escape

def sheet(d,full=False,demo=False):
    attrs=''.join(f'<label class="attribute"><span class="mono">{a}</span><input type="number" min="0" max="99" value="2" aria-label="{a}"></label>' if demo else f'<div class="attribute"><span class="mono">{a}</span><strong>02</strong></div>' for a in d['attrs'])
    bars=''.join(f'<div class="resource"><div class="resource-title mono"><span>{l}</span><span><output>{v} / {m}</output></span></div>'+ (f'<input data-resource type="range" min="0" max="{m}" value="{v}" aria-label="{l}">' if demo else '<div class="meter"><span></span></div>')+'</div>' for l,v,m in zip(d['resources'],[18,12,8],[24,16,12]))
    blocks=''.join('<div class="sheet-block"><span class="mono">'+d[k]+'</span><ul>'+''.join('<li>'+escape(v)+'</li>' for v in d[l])+'</ul></div>' for k,l in [('skills','skillList'),('equipment','equipmentList')])
    identity=f'<label><span class="mono">{d["char"]}</span><input class="demo-name" aria-label="{d["name"]}" value="{d["identity"]}" maxlength="60"></label>' if demo else f'<div class="sheet-identity"><span class="mono">{d["char"]}</span><h3>{d["identity"]}</h3></div>'
    if demo:
        tabs='<div class="sheet-tabs" role="tablist" aria-label="UTOPIA">'+''.join(f'<button type="button" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{t}</button>' for i,t in enumerate(d['tabs']))+'</div>'
        contents=f'<div class="sheet-grid" id="panel-0" role="tabpanel" aria-labelledby="tab-0">{blocks}</div>'
        contents+='<div class="sheet-grid" id="panel-1" role="tabpanel" aria-labelledby="tab-1" hidden><div class="sheet-block"><span class="mono">'+d['equipment']+'</span>'+''.join(f'<input aria-label="{x}" value="{x}" maxlength="80">' for x in d['equipmentList'])+'</div></div>'
        contents+='<div class="sheet-grid" id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden><div class="sheet-block"><span class="mono">'+d['implantLabel']+'</span>'+''.join(f'<input aria-label="{x}" value="{x}" maxlength="80">' for x in d['implants'])+'</div><p class="mono">'+d['implantNote']+'</p></div>'
        contents+=f'<div class="demo-controls"><label class="mono">{d["die"]} <select data-die>'+''.join(f'<option value="{n}"'+(' selected' if n==20 else '')+f'>d{n}</option>' for n in [4,6,8,10,12,20])+f'</select></label><button type="button" data-roll>{d["roll"]}</button><output class="dice-result" data-result aria-live="polite">{d["ready"]}</output></div><p class="demo-notice">{d["demoNotice"]}</p>'
    else:
        tabs='<div class="sheet-tabs">'+''.join(f'<span>{t}</span>' for t in d['tabs'])+'</div>'
        contents=f'<div class="sheet-grid">{blocks}</div>' if full else ''
    return f'<div class="sheet{" sheet-full" if full else ""}"><div class="sheet-top"><span class="sheet-logo">UTOPIA</span><span class="mono">{d["hub"]}</span></div>{identity}<div class="attributes">{attrs}</div>{bars}{tabs}{contents}<p class="mono sheet-note">{d["excerpt"]}</p></div>'
