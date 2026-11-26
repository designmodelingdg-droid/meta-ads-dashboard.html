const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{const dir=path.resolve(process.argv[2]);const b=await chromium.launch({args:['--allow-file-access-from-files']});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html')).sort()){const m=f.match(/-(1x1|3x4|9x16|16x9)\.html$/);const S={'1x1':[1080,1080],'3x4':[1080,1440],'9x16':[1080,1920],'16x9':[1920,1080]}[m[1]];
const p=await b.newPage({viewport:{width:S[0],height:S[1]}});await p.goto('file://'+path.join(dir,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(250);await p.screenshot({path:path.join(dir,f.replace('.html','.png'))});await p.close();}
await b.close();})();
