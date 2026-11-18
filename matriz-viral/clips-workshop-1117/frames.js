const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/frame.html');await p.waitForTimeout(1500);
for(const c of JSON.parse(fs.readFileSync('clips.json'))){
 await p.evaluate(c=>{document.getElementById('h').innerHTML=c.hook1+'<em>'+c.hook2+'</em>';document.getElementById('s').textContent=c.sub},c);
 await p.screenshot({path:`marco-${c.id}.png`,omitBackground:true});}
await b.close();})();
