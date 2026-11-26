const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{const dir=path.resolve(process.argv[2]);const b=await chromium.launch({args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html')).sort()){await p.goto('file://'+path.join(dir,f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);await p.screenshot({path:path.join(dir,f.replace('.html','.jpg')),type:'jpeg',quality:90});}
await b.close();})();
