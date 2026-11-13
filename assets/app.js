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


const contactDialog=document.getElementById('contact-dialog');
if(contactDialog&&typeof contactDialog.showModal==='function'){
 const mode=contactDialog.querySelector('[data-toggle-contact-focus]');
 let lastContactTrigger;
 function setMode(focused){contactDialog.classList.toggle('is-focused',focused);mode.setAttribute('aria-pressed',String(focused));mode.textContent=focused?mode.dataset.dockLabel:mode.dataset.focusLabel;}
 function closeContact(){contactDialog.close();if(lastContactTrigger)lastContactTrigger.focus({preventScroll:true});}
 document.querySelectorAll('[data-open-contact]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();lastContactTrigger=link;if(!contactDialog.open){setMode(false);contactDialog.show();}contactDialog.querySelector('[data-close-contact]').focus({preventScroll:true});}));
 contactDialog.querySelector('[data-close-contact]').addEventListener('click',closeContact);
 mode.addEventListener('click',()=>{const focused=!contactDialog.classList.contains('is-focused');contactDialog.close();setMode(focused);if(focused)contactDialog.showModal();else contactDialog.show();mode.focus({preventScroll:true});});
 contactDialog.addEventListener('cancel',event=>{event.preventDefault();closeContact();});
 contactDialog.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();closeContact();}});
 contactDialog.addEventListener('click',event=>{if(event.target===contactDialog&&contactDialog.classList.contains('is-focused')){const box=contactDialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)closeContact();}});
}


// Local image galleries: keyboard navigation and native modal focus management.
const imageDialog=document.getElementById('image-dialog');
if(imageDialog&&typeof imageDialog.showModal==='function'){
 const full=imageDialog.querySelector('#image-full');
 const caption=imageDialog.querySelector('#image-caption');
 const count=imageDialog.querySelector('#image-count');
 let gallery=[],current=0,trigger;
 function renderImage(){imageDialog.classList.remove('is-zoomed');imageDialog.querySelector('[data-image-zoom]').setAttribute('aria-pressed','false');const item=gallery[current];full.src=item.href;full.alt=item.dataset.caption;caption.textContent=item.dataset.caption;count.textContent=`${current+1} / ${gallery.length}`;imageDialog.querySelector('.image-canvas').scrollTop=0;}
 function moveImage(step){current=(current+step+gallery.length)%gallery.length;renderImage();}
 document.querySelectorAll('[data-gallery]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();trigger=link;gallery=[...document.querySelectorAll('[data-gallery]')].filter(item=>item.dataset.gallery===link.dataset.gallery);current=gallery.indexOf(link);renderImage();imageDialog.showModal();}));
 imageDialog.querySelector('[data-image-zoom]').addEventListener('click',event=>{const zoomed=imageDialog.classList.toggle('is-zoomed');event.currentTarget.setAttribute('aria-pressed',String(zoomed));});
 imageDialog.querySelector('[data-close-image]').addEventListener('click',()=>imageDialog.close());
 imageDialog.querySelector('[data-image-prev]').addEventListener('click',()=>moveImage(-1));
 imageDialog.querySelector('[data-image-next]').addEventListener('click',()=>moveImage(1));
 imageDialog.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();moveImage(event.key==='ArrowLeft'?-1:1);}});
 imageDialog.addEventListener('close',()=>{full.removeAttribute('src');if(trigger)trigger.focus({preventScroll:true});});
}

// Fit the official local module to its contents as tabs and records change.
document.querySelectorAll('.official-implants').forEach(frame=>{
 frame.addEventListener('load',()=>{
  const content=frame.contentDocument?.querySelector('.content');
  if(!content)return;
  const fit=()=>{if(content.getBoundingClientRect().width)frame.style.height=Math.ceil(content.getBoundingClientRect().height+24)+'px';};
  new ResizeObserver(fit).observe(content);fit();
 });
});

const characterVideo=document.querySelector('[data-character-video]');
if(characterVideo){
 const toggle=document.querySelector('[data-character-toggle]');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 toggle.hidden=false;
 function syncCharacter(){const paused=characterVideo.paused;toggle.setAttribute('aria-label',paused?toggle.dataset.playLabel:toggle.dataset.pauseLabel);toggle.querySelector('path').setAttribute('d',paused?'M8 5l11 7-11 7Z':'M9 6v12m6-12v12');}
 characterVideo.addEventListener('play',syncCharacter);
 characterVideo.addEventListener('pause',syncCharacter);
 toggle.addEventListener('click',()=>{if(characterVideo.paused)characterVideo.play().catch(syncCharacter);else characterVideo.pause();});
 reduced.addEventListener('change',()=>{if(reduced.matches)characterVideo.pause();});
 if(!reduced.matches)characterVideo.play().catch(syncCharacter);
 syncCharacter();
}
