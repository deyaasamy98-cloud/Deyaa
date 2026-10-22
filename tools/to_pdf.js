// usage: node to_pdf.js <fontdir> <in.html> <out.pdf> [<in.html> <out.pdf> ...]
const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const [fontDir,...pairs]=process.argv.slice(2);
let fontCss=fs.readFileSync(path.join(fontDir,'cairo.css'),'utf8')
  .replace(/url\(https:\/\/fonts\.gstatic\.com\/[^)]*\/([^/)]+\.woff2)\)/g,(m,f)=>
    `url(data:font/woff2;base64,${fs.readFileSync(path.join(fontDir,f)).toString('base64')})`);
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const page=await b.newPage();
  for(let i=0;i<pairs.length;i+=2){
    let body=fs.readFileSync(pairs[i],'utf8')
      .replace(/<link rel="(preconnect|stylesheet)"[^>]*>\n?/g,'')
      .replace(/<details>/g,'<details open>');
    const html=`<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${fontCss}</style></head><body>${body}</body></html>`;
    await page.emulateMedia({media:'print',colorScheme:'light'});
    await page.setContent(html,{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    const fam=await page.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family).join(','));
    await page.pdf({path:pairs[i+1],format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,
      headerTemplate:'<div></div>',
      footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#888"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'});
    console.log(path.basename(pairs[i+1]),'fonts loaded:',fam);
  }
  await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
