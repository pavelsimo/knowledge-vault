import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const htmlDir = path.join(root, "wiki_html");
const storageKey = "knowledge-vault-theme";

const initializer = `<script id="theme-init">(function(){var k='${storageKey}',s=null;try{s=localStorage.getItem(k)}catch(e){}var m=matchMedia('(prefers-color-scheme: dark)');document.documentElement.dataset.theme=s==='light'||s==='dark'?s:(m.matches?'dark':'light')})();</script>`;

const styles = `
/* Standard self-contained wiki theme control. */
html{color-scheme:light}html[data-theme="dark"]{color-scheme:dark}
:root[data-theme="dark"]{--ivory:#171714;--paper:#22221E;--slate:#F4F0E6;--clay:#E58A68;--clay-d:#F0A080;--oat:#5A463B;--olive:#9CAF7E;--g100:#292923;--g200:#36362F;--g300:#4A4940;--g500:#A5A198;--g700:#D2CEC4}
.theme-toggle{position:fixed;top:16px;right:16px;z-index:1000;width:42px;height:42px;display:grid;place-items:center;padding:0;border:1.5px solid var(--g300);border-radius:9999px;background:var(--paper);color:var(--g700);cursor:pointer;box-shadow:0 4px 16px rgba(20,20,19,.12);transition:color 120ms ease,border-color 120ms ease,background-color 120ms ease,transform 150ms ease}
.theme-toggle:hover{color:var(--clay);border-color:var(--clay);transform:translateY(-1px)}.theme-toggle:focus-visible{outline:3px solid var(--clay);outline-offset:3px}.theme-toggle svg{width:20px;height:20px;display:block}.theme-toggle .moon{display:none}:root[data-theme="dark"] .theme-toggle .sun{display:none}:root[data-theme="dark"] .theme-toggle .moon{display:block}
@media(max-width:640px){.theme-toggle{top:10px;right:10px;width:40px;height:40px}}
@media(prefers-reduced-motion:reduce){.theme-toggle{transition:none}.theme-toggle:hover{transform:none}}
`;

const button = `<button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false" title="Switch to dark mode"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><g class="sun"><circle cx="12" cy="12" r="3.5"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"/></g><path class="moon" d="M20.2 15.1A8.5 8.5 0 0 1 8.9 3.8 8.5 8.5 0 1 0 20.2 15.1Z"/></svg></button>`;

const controller = `<script id="theme-controller">(function(){var k='${storageKey}',r=document.documentElement,b=document.querySelector('.theme-toggle'),m=matchMedia('(prefers-color-scheme: dark)');if(!b)return;function stored(){try{var v=localStorage.getItem(k);return v==='light'||v==='dark'?v:null}catch(e){return null}}function apply(t){r.dataset.theme=t;var dark=t==='dark',label='Switch to '+(dark?'light':'dark')+' mode';b.setAttribute('aria-pressed',String(dark));b.setAttribute('aria-label',label);b.title=label}function system(){if(!stored())apply(m.matches?'dark':'light')}b.addEventListener('click',function(){var next=r.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem(k,next)}catch(e){}apply(next)});m.addEventListener?m.addEventListener('change',system):m.addListener(system);addEventListener('storage',function(e){if(e.key===k)apply(stored()||(m.matches?'dark':'light'))});apply(r.dataset.theme==='dark'?'dark':'light')})();</script>`;

const htmlFiles = fs.readdirSync(htmlDir).filter((name) => name.endsWith(".html")).sort();
let changed = 0;

for (const name of htmlFiles) {
  const file = path.join(htmlDir, name);
  const original = fs.readFileSync(file, "utf8");
  if (original.includes('id="theme-init"')) continue;

  let updated = original.replace(/<style>/i, `${initializer}<style>`);
  updated = updated.replace(/<\/style>/i, `${styles}</style>`);
  updated = updated.replace(/<body([^>]*)>/i, `<body$1>${button}`);
  updated = updated.replace(/<\/body>/i, `${controller}</body>`);

  if (updated === original || !updated.includes('id="theme-controller"')) {
    throw new Error(`Could not install theme control in ${name}`);
  }

  fs.writeFileSync(file, updated);
  changed += 1;
}

console.log(`Theme control synchronized: ${changed} changed, ${htmlFiles.length - changed} already current`);
