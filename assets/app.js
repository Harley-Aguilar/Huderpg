document.querySelectorAll('[data-demo]').forEach(demo=>{const pt=document.documentElement.lang==='pt-BR';demo.querySelectorAll('[data-resource]').forEach(input=>{input.addEventListener('input',()=>{const row=input.closest('.resource');row.querySelector('output').textContent=`${input.value} / ${input.max}`;});});const tabs=[...demo.querySelectorAll('[role=tab]')];function activate(tab){tabs.forEach(t=>{const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;document.getElementById(t.getAttribute('aria-controls')).hidden=!active;});}tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>activate(tab));tab.addEventListener('keydown',event=>{let target;if(event.key==='ArrowRight')target=tabs[(i+1)%tabs.length];if(event.key==='ArrowLeft')target=tabs[(i-1+tabs.length)%tabs.length];if(event.key==='Home')target=tabs[0];if(event.key==='End')target=tabs.at(-1);if(target){event.preventDefault();activate(target);target.focus();}});});demo.querySelector('[data-roll]').addEventListener('click',()=>{const sides=Number(demo.querySelector('[data-die]').value);const random=new Uint32Array(1);crypto.getRandomValues(random);const limit=Math.floor(4294967296/sides)*sides;while(random[0]>=limit)crypto.getRandomValues(random);const result=random[0]%sides+1;const out=demo.querySelector('[data-result]');out.textContent=`d${sides} → ${result} · ${pt?'Sem modificadores':'No modifiers'}`;});});

const privacyNotice=document.getElementById('privacy-notice');
if(privacyNotice){
 const closePrivacy=privacyNotice.querySelector('[data-close-privacy]');
 const privacyKey='huderpg-privacy-notice-v1';
 closePrivacy.hidden=false;
 try{privacyNotice.hidden=sessionStorage.getItem(privacyKey)==='dismissed';}catch{}
 document.querySelectorAll('[data-open-privacy]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();privacyNotice.hidden=false;document.getElementById('privacy-title').focus({preventScroll:true});}));
 closePrivacy.addEventListener('click',()=>{privacyNotice.hidden=true;try{sessionStorage.setItem(privacyKey,'dismissed');}catch{}const link=document.querySelector('[data-open-privacy]');if(link)link.focus({preventScroll:true});});
}
