
// ══ SUPABASE + GOOGLE DRIVE (سحابي حقيقي) ══════════════════
// ─── الإعدادات (علنية - آمنة) ───
const SUPABASE_URL='https://mkdsnnfkkdwdkywnwnjh.supabase.co';
const SUPABASE_ANON_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1rZHNubmZra2R3ZGt5d253bmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwMDk0MDgsImV4cCI6MjA5NDU4NTQwOH0.girscgcDBxUi2O1kWjD5Q_Uc-6bJZEtuAa_tpZlazQo';
const GOOGLE_DRIVE_FOLDER_NAME='خطتي الفصلية';
const WHATSAPP='+96876990975';
const sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_ANON_KEY,{
  auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}
});
let currentUser=null,displayName='';
let googleAccessToken=null;   // توكن Google لرفع الملفات على Drive
let driveFolderId=null;       // مجلد التطبيق داخل درايف المستخدم
const MAX_FILE_SIZE=500*1024*1024; // 500MB حد رفع

// ─── تسجيل الدخول بحساب Google ───
async function signInWithGoogle(){
  const btn=document.getElementById('google-signin-btn');
  if(btn){btn.disabled=true;document.getElementById('google-btn-text').textContent='جارٍ التحويل...';}
  const {error}=await sb.auth.signInWithOAuth({
    provider:'google',
    options:{
      redirectTo:window.location.href.split('#')[0],
      scopes:'https://www.googleapis.com/auth/drive.file',
      queryParams:{access_type:'offline',prompt:'consent'}
    }
  });
  if(error){
    if(btn){btn.disabled=false;document.getElementById('google-btn-text').textContent='تسجيل الدخول بحساب Google';}
    toast('❌ تعذّر تسجيل الدخول: '+error.message,true);
  }
}
async function signOut(){
  if(!confirm('تسجيل الخروج؟ بياناتك محفوظة في حسابك السحابي.'))return;
  await sb.auth.signOut();
  location.reload();
}

// ─── قاعدة البيانات (جدول profiles في Supabase) ───
async function dbLoad(){
  if(!currentUser)return null;
  try{
    const {data,error}=await sb.from('profiles').select('data').eq('id',currentUser.id).maybeSingle();
    if(error){console.error('dbLoad error:',error);return null;}
    return data?data.data:null;
  }catch(e){console.error('dbLoad exception:',e);return null;}
}
async function dbInit(){
  if(!currentUser)return false;
  try{
    const {data}=await sb.from('profiles').select('id').eq('id',currentUser.id).maybeSingle();
    if(!data){
      await sb.from('profiles').insert({
        id:currentUser.id,
        email:currentUser.email||'',
        data:{display_name:displayName||'',email:currentUser.email||'',avatar_url:currentUser.user_metadata?.avatar_url||'',created_at:new Date().toISOString()}
      });
    }
    return true;
  }catch(e){console.error('dbInit exception:',e);return false;}
}
async function dbSave(payload){
  if(!currentUser)return false;
  showSyncing();
  let ok=false;
  try{
    const current=await dbLoad()||{};
    const gMeta=currentUser.user_metadata||{};
    const merged={
      ...current,...payload,
      email:currentUser.email||'',
      avatar_url:gMeta.avatar_url||gMeta.picture||current.avatar_url||'',
      full_name:gMeta.full_name||gMeta.name||current.full_name||'',
      updated_at:new Date().toISOString()
    };
    const {error}=await sb.from('profiles').upsert({id:currentUser.id,email:currentUser.email||'',data:merged,updated_at:new Date().toISOString()});
    ok=!error;
    if(error)console.error('dbSave error:',error);
  }catch(e){
    if(!navigator.onLine){
      toast('📵 لا يوجد اتصال بالإنترنت — سيتم الحفظ عند الاتصال',true);
    }else{
      toast('⚠️ تعذّر الحفظ — تحقق من الاتصال',true);
    }
    ok=false;
  }
  hideSyncing(ok);
  return ok;
}
let syncTimer2;
function showSyncing(){const el=document.getElementById('sync-status');const fill=document.getElementById('sync-bar-fill');document.getElementById('sync-text').textContent='جاري الحفظ...';el.classList.add('show');fill.style.width='70%';}
function hideSyncing(ok){const el=document.getElementById('sync-status');const fill=document.getElementById('sync-bar-fill');document.getElementById('sync-text').textContent=ok?'تم الحفظ ✅':'تعذّر الحفظ ⚠️';fill.style.width=ok?'100%':'30%';clearTimeout(syncTimer2);syncTimer2=setTimeout(()=>{el.classList.remove('show');fill.style.width='0%';},2000);}
function fmtSize(b){if(!b)return'';if(b<1024)return b+'B';if(b<1048576)return(b/1024).toFixed(1)+'KB';return(b/1048576).toFixed(2)+'MB';}

// ══ GOOGLE DRIVE (تخزين الملفات الحقيقي) ══════════════════
// إنشاء/إيجاد مجلد التطبيق داخل درايف المستخدم (مرة واحدة)
async function ensureDriveFolder(){
  if(driveFolderId)return driveFolderId;
  if(!googleAccessToken)throw new Error('no-google-token');
  // ابحث عن المجلد
  const q=encodeURIComponent(`name='${GOOGLE_DRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false`);
  const res=await fetch(`https://www.googleapis.com/drive/v3/files?q=${q}&fields=files(id,name)`,{
    headers:{Authorization:'Bearer '+googleAccessToken}
  });
  const j=await res.json();
  if(j.files&&j.files.length){driveFolderId=j.files[0].id;return driveFolderId;}
  // أنشئ المجلد
  const cr=await fetch('https://www.googleapis.com/drive/v3/files',{
    method:'POST',
    headers:{Authorization:'Bearer '+googleAccessToken,'Content-Type':'application/json'},
    body:JSON.stringify({name:GOOGLE_DRIVE_FOLDER_NAME,mimeType:'application/vnd.google-apps.folder'})
  });
  const cj=await cr.json();
  driveFolderId=cj.id;
  return driveFolderId;
}
// يرفع الملف على Drive ويرجّع كائن متوافق مع باقي الكود
async function driveUpload(file,fileName){
  if(!googleAccessToken){toast('❌ صلاحية Google منتهية. سجّل الدخول من جديد',true);return null;}
  if(file.size>MAX_FILE_SIZE){toast('❌ الملف أكبر من 500MB',true);return null;}
  try{
    const folderId=await ensureDriveFolder();
    const metadata={name:fileName,parents:[folderId]};
    const form=new FormData();
    form.append('metadata',new Blob([JSON.stringify(metadata)],{type:'application/json'}));
    form.append('file',file);
    const res=await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,size,webViewLink,webContentLink',{
      method:'POST',
      headers:{Authorization:'Bearer '+googleAccessToken},
      body:form
    });
    if(!res.ok){
      if(res.status===401){toast('❌ صلاحية Google منتهية. سجّل الدخول من جديد',true);}
      else{toast('❌ فشل رفع الملف على Drive',true);}
      console.error('drive upload failed:',res.status,await res.text());
      return null;
    }
    const j=await res.json();
    const view='https://drive.google.com/file/d/'+j.id+'/view';
    return{
      id:j.id,name:j.name||fileName,size:file.size,
      viewLink:view,previewLink:view,
      downloadLink:'https://drive.google.com/uc?export=download&id='+j.id
    };
  }catch(e){console.error('drive upload error:',e);toast('❌ تعذّر رفع الملف',true);return null;}
}
async function driveDelete(fileId){
  if(!fileId||!googleAccessToken)return false;
  try{
    const res=await fetch('https://www.googleapis.com/drive/v3/files/'+fileId,{
      method:'DELETE',headers:{Authorization:'Bearer '+googleAccessToken}
    });
    return res.ok||res.status===404;
  }catch(e){console.error('drive delete error:',e);return false;}
}
async function driveGetStorageInfo(){
  // صلاحية drive.file لا تسمح بقراءة إجمالي مساحة Drive (يرجّع 403)
  // نرجّع null بهدوء — شريط المساحة يُخفى تلقائياً، والرفع/الحذف يعمل عادي
  return null;
}
function isDriveFile(fileObj){return fileObj&&fileObj.driveId;}
async function getFileUrl(fileObj){
  if(isDriveFile(fileObj))return'https://drive.google.com/file/d/'+fileObj.driveId+'/view';
  return'';
}
async function getDownloadUrl(fileObj){
  if(isDriveFile(fileObj))return'https://drive.google.com/uc?export=download&id='+fileObj.driveId;
  return'';
}

// ══ حذف كل البيانات ══════════════════════════════════
async function resetAllData(){
  if(!confirm('⚠️ سيتم حذف جميع بياناتك نهائياً من حسابك السحابي. هل أنت متأكد؟'))return;
  if(!confirm('تأكيد أخير: لا يمكن التراجع. متابعة الحذف؟'))return;
  try{
    await sb.from('profiles').update({data:{}}).eq('id',currentUser.id);
  }catch(e){}
  location.reload();
}

// ══ بدء التشغيل ════════════════════════════════════════
function showAuthState(state){
  ['auth-login','auth-denied','auth-onboard','auth-loading'].forEach(id=>{
    const el=document.getElementById(id);if(!el)return;
    if(id===state){el.style.display='block';el.classList.add('show');el.classList.remove('hide');}
    else{el.style.display='none';el.classList.remove('show');el.classList.add('hide');}
  });
}
async function completeOnboard(){
  const name=document.getElementById('onboard-name').value.trim();
  if(!name){document.getElementById('onboard-name').focus();return;}
  displayName=name;
  await dbSave({display_name:name});
  document.getElementById('auth-screen').classList.add('hidden');
  showSetupScreen();
}
function showUserBadge(){
  const badge=document.getElementById('user-badge');if(badge)badge.style.display='flex';
  const imgEl=document.getElementById('ub-img');
  if(imgEl)imgEl.src=`data:image/svg+xml;base64,${btoa('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><circle cx="20" cy="20" r="20" fill="%23c0392b"/><text x="20" y="27" font-size="18" text-anchor="middle" fill="white">D</text></svg>')}`;
  const ubn=document.getElementById('ub-name');
  if(ubn){
    const adminTag=isAdmin()?'<span class="admin-badge">👑 مشرف</span>':'';
    ubn.innerHTML=adminTag+(displayName||'حسابي');
  }
  const umn=document.getElementById('um-name');if(umn)umn.textContent=displayName||'حسابي';
  const ume=document.getElementById('um-email');if(ume)ume.textContent='محفوظ سحابياً ☁️';
  const tb=document.getElementById('teacher-name-banner');if(tb)tb.textContent=displayName||'الأستاذ';
}
function toggleUserMenu(e){e.stopPropagation();document.getElementById('user-menu').classList.toggle('show');}
document.addEventListener('click',e=>{const m=document.getElementById('user-menu');if(m&&!m.contains(e.target)&&!e.target.closest('#user-badge'))m.classList.remove('show');});
async function renameTeacher(){const newName=prompt('الاسم الجديد:',displayName||'');if(!newName||!newName.trim())return;displayName=newName.trim();await dbSave({display_name:displayName});showUserBadge();document.getElementById('user-menu').classList.remove('show');toast('✅ تم التحديث','ok');}
function reopenSetup(){document.getElementById('user-menu').classList.remove('show');showSetupScreen();}

// نقطة الدخول: تنتظر تسجيل دخول Google عبر Supabase
async function bootApp(session){
  currentUser=session.user;
  // ─── فحص قائمة الإيميلات المسموحة ───
  const userEmail=(currentUser.email||'').toLowerCase().trim();
  try{
    const {data:allowed,error}=await sb.from('allowed_emails').select('email').eq('email',userEmail).maybeSingle();
    if(error){
      console.error('allowed_emails check error:',error);
      await sb.auth.signOut();
      document.getElementById('auth-screen').classList.remove('hidden');
      showAuthState('auth-login');
      toast('⚠️ تعذّر التحقق من الصلاحية. حاول لاحقاً',true);
      return;
    }
    if(!allowed){
      // تحقق من وجود كود دعوة في الرابط قبل الرفض
      const inviteCode=new URLSearchParams(location.search).get('invite');
      if(inviteCode){
        // فحص الدعوة وإضافة البريد
        const handled=await handleInviteOnBoot(inviteCode,userEmail);
        if(handled){
          // أعد تشغيل bootApp بعد الإضافة
          bootApp(session);
          return;
        }
      }
      await sb.auth.signOut();
      currentUser=null;googleAccessToken=null;
      document.getElementById('auth-screen').classList.remove('hidden');
      showAuthState('auth-login');
      const sub=document.querySelector('#auth-login .auth-sub');
      if(sub)sub.innerHTML='⛔ هذا البريد ('+userEmail+') غير مصرّح له بالدخول.<br/>تواصل مع المشرف لإضافة بريدك.';
      const btn=document.getElementById('google-signin-btn');
      if(btn){btn.disabled=false;document.getElementById('google-btn-text').textContent='تسجيل الدخول بحساب آخر';}
      return;
    }
  }catch(e){
    console.error('allowed_emails exception:',e);
    await sb.auth.signOut();
    document.getElementById('auth-screen').classList.remove('hidden');
    showAuthState('auth-login');
    toast('⚠️ تعذّر التحقق من الصلاحية',true);
    return;
  }
  // التقط توكن Google لرفع الملفات على Drive
  if(session.provider_token)googleAccessToken=session.provider_token;

  // فحص إذا كان الحساب محظوراً
  try{
    const{data:banned}=await sb.from('banned_users').select('user_id').eq('user_id',currentUser.id).maybeSingle();
    if(banned){
      await sb.auth.signOut();
      currentUser=null;
      document.getElementById('auth-screen').classList.remove('hidden');
      showAuthState('auth-login');
      const sub=document.querySelector('#auth-login .auth-sub');
      if(sub)sub.innerHTML='⛔ تم تعليق حسابك. تواصل مع المشرف.';
      return;
    }
  }catch(e){}

  await dbInit();
  const data=await dbLoad();
  document.getElementById('auth-screen').classList.add('hidden');
  if(!data||!data.display_name){
    // أول دخول: استخدم اسم Google كاقتراح ثم اطلب التأكيد
    const gName=(currentUser.user_metadata&&(currentUser.user_metadata.full_name||currentUser.user_metadata.name))||'';
    document.getElementById('auth-screen').classList.remove('hidden');
    showAuthState('auth-onboard');
    const inp=document.getElementById('onboard-name');
    if(inp){inp.value=gName;setTimeout(()=>inp.focus(),200);}
    return;
  }
  displayName=data.display_name;
  // ─── المشرف يدخل مباشرة بدون إعداد ───
  const isAdminUser=(currentUser?.email||'').toLowerCase().trim()===ADMIN_EMAIL.toLowerCase();
  if(isAdminUser){
    // ضع إعداداً افتراضياً مبسطاً للمشرف (لتجنب أخطاء الدوال التي تتوقع وجوده)
    if(!data.teacher_config||!data.teacher_config.grades||!data.teacher_config.grades.length){
      data.teacher_config={
        grades:[],subjects:['الرياضيات'],subject:'الرياضيات',
        semester:'الفصل الأول',setupDone:true,isAdminMode:true
      };
    }else{
      data.teacher_config.isAdminMode=true;
    }
    showApp(data);
    startBellPolling();
    return;
  }
  if(!data.teacher_config||!data.teacher_config.grades||!data.teacher_config.grades.length){
    showSetupScreen();
    return;
  }
  showApp(data);
  // بدء polling للجرس
  startBellPolling();
}

(async()=>{
  // أظهر شاشة الدخول مبدئياً
  document.getElementById('auth-screen').classList.remove('hidden');
  showAuthState('auth-loading');

  const {data:{session}}=await sb.auth.getSession();
  if(session){
    await bootApp(session);
  }else{
    showAuthState('auth-login');
  }

  // راقب تغيّر حالة الدخول (بعد رجوع المستخدم من Google)
  sb.auth.onAuthStateChange(async(event,session)=>{
    if(event==='SIGNED_IN'&&session){
      if(!currentUser)await bootApp(session);
      else if(session.provider_token)googleAccessToken=session.provider_token;
    }
    if(event==='SIGNED_OUT'){currentUser=null;googleAccessToken=null;stopBellPolling();}
  });
})();

// ══ SETUP SCREEN ══════════════════════════════════════
const GRADE_COLORS=['#e74c3c','#e8b86d','#f0c060','#27ae60','#3498db','#9b59b6','#e67e22','#1abc9c','#e91e63','#00bcd4','#8bc34a','#ff5722'];

function showSetupScreen(){
  document.getElementById('setup-screen').classList.remove('hidden');
  document.getElementById('main-nav').style.display='none';
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  // إعادة ضبط حالة الإعداد والبدء من الخطوة الأولى (الفصل)
  setupSemester='';setupGrades=[];setupData={};curriculumBySubject={};gradeSubjectsMap={};setupActiveGrade=null;
  document.getElementById('setup-step-1').style.display='block';
  document.getElementById('setup-step-2').style.display='none';
  document.getElementById('step-1').classList.add('active');document.getElementById('step-1').classList.remove('done');
  document.getElementById('step-2').classList.remove('active');
  document.getElementById('grade-card').style.display='none';
  document.getElementById('lessons-preview-card').style.display='none';
  document.querySelectorAll('#semester-grid .class-chip-btn').forEach(b=>b.classList.remove('sel'));
}
// ── حالة الإعداد ──
let setupSemester='';
let gradeSubjectsMap={};       // {grade: [subjects]} مواد كل صف من جدول subjects
let curriculumBySubject={};    // {"subject|grade": [rows]} المحتوى الفعلي
// لكل صف: مواده وشعبه → setupData[gradeNum] = {subjects:[], classes:[]}
let setupData={};
let setupGrades=[];            // الصفوف المختارة
let setupActiveGrade=null;     // تبويب الصف النشط

function selectSemester(sem,btn){
  setupSemester=sem;
  document.querySelectorAll('#semester-grid .class-chip-btn').forEach(b=>b.classList.remove('sel'));
  btn.classList.add('sel');
  setupGrades=[];setupData={};curriculumBySubject={};
  loadGradesForSemester();
}
async function loadGradesForSemester(){
  const card=document.getElementById('grade-card');
  const grid=document.getElementById('grade-grid');
  card.style.display='block';
  grid.innerHTML='<p style="color:var(--muted)">جارٍ التحميل...</p>';
  try{
    // اقرأ من الجدولين ودمجهما
    let rows=[];
    const r1=await sb.from('subjects').select('subject,grade,sort').eq('semester',setupSemester);
    if(!r1.error&&r1.data&&r1.data.length){
      rows=r1.data;
    }
    
    // اقرأ أيضاً من curriculum للتأكد من ظهور جميع المواد المتوفرة
    const r2=await sb.from('curriculum').select('subject,grade').eq('semester',setupSemester);
    if(!r2.error&&r2.data&&r2.data.length){
      // دمج البيانات بدون تكرار
      const existing=new Set(rows.map(r=>`${r.subject}|${r.grade}`));
      r2.data.forEach(r=>{
        const key=`${r.subject}|${r.grade}`;
        if(!existing.has(key)){
          rows.push({subject:r.subject,grade:r.grade,sort:99});
          existing.add(key);
        }
      });
    }
    
    if(!rows.length){
      grid.innerHTML='<p style="color:var(--muted)">لا توجد مواد مُجهّزة لهذا الفصل بعد. تواصل مع المشرف.</p>';
      return;
    }
    
    // خريطة: لكل صف → مواده (مرتبة حسب sort)
    gradeSubjectsMap={};
    rows.slice().sort((a,b)=>(a.sort||0)-(b.sort||0)).forEach(r=>{
      if(!gradeSubjectsMap[r.grade])gradeSubjectsMap[r.grade]=[];
      if(!gradeSubjectsMap[r.grade].includes(r.subject))gradeSubjectsMap[r.grade].push(r.subject);
    });
    const grades=Object.keys(gradeSubjectsMap).map(Number).sort((a,b)=>a-b);
    const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
    grid.innerHTML=grades.map(g=>`<button class="class-chip-btn ${setupGrades.includes(g)?'sel':''}" onclick="toggleSetupGrade(${g},this)">الصف ${arabicNums[g-1]}</button>`).join('');
  }catch(e){grid.innerHTML='<p style="color:var(--muted)">تعذّر التحميل</p>';}
}
function toggleSetupGrade(g,btn){
  const i=setupGrades.indexOf(g);
  if(i>=0){setupGrades.splice(i,1);btn.classList.remove('sel');delete setupData[g];}
  else{setupGrades.push(g);btn.classList.add('sel');setupData[g]={subjects:[],classes:{}};}
  setupGrades.sort((a,b)=>a-b);
}
async function goToStep2(){
  if(!setupSemester){toast('❌ اختر الفصل الدراسي',true);return;}
  if(!setupGrades.length){toast('❌ اختر صفاً واحداً على الأقل',true);return;}
  document.getElementById('setup-step-1').style.display='none';
  document.getElementById('setup-step-2').style.display='block';
  document.getElementById('step-1').classList.remove('active');document.getElementById('step-1').classList.add('done');
  document.getElementById('step-2').classList.add('active');
  setupActiveGrade=setupGrades[0];
  buildGradeTabs();
  buildGradeSetupBody();
}
function buildGradeTabs(){
  const tabs=document.getElementById('grade-tabs');
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  tabs.innerHTML=setupGrades.map(g=>{
    const d=setupData[g];
    const done=(d&&d.subjects.length)?' ✓':'';
    return `<button class="grade-tab-btn ${g===setupActiveGrade?'active':''}" onclick="switchGradeTab(${g})">الصف ${arabicNums[g-1]}${done}</button>`;
  }).join('');
}
function switchGradeTab(g){
  setupActiveGrade=g;
  buildGradeTabs();
  buildGradeSetupBody();
}
// حمّل محتوى مادة+صف عند الحاجة (للمعاينة)
async function ensureContent(subject,grade){
  const key=subject+'|'+grade;
  if(curriculumBySubject[key])return curriculumBySubject[key];
  // محاولة قراءة من localStorage cache (صالح لمدة 24 ساعة)
  const cacheKey='curr:'+setupSemester+':'+subject+':'+grade;
  try{
    const cached=localStorage.getItem(cacheKey);
    if(cached){
      const obj=JSON.parse(cached);
      if(obj&&obj.t&&(Date.now()-obj.t)<86400000){
        curriculumBySubject[key]=obj.d||[];
        return curriculumBySubject[key];
      }
    }
  }catch(e){}
  try{
    const {data}=await sb.from('curriculum').select('*')
      .eq('semester',setupSemester).eq('subject',subject).eq('grade',grade).order('sort');
    curriculumBySubject[key]=data||[];
    // حفظ في cache
    try{localStorage.setItem(cacheKey,JSON.stringify({t:Date.now(),d:data||[]}));}catch(e){}
  }catch(e){curriculumBySubject[key]=[];}
  return curriculumBySubject[key];
}
// مسح cache المناهج (يستخدم عند تحديث الدروس من زر "🔄 تحديث الدروس")
function clearCurriculumCache(){
  try{
    const keys=[];
    for(let i=0;i<localStorage.length;i++){
      const k=localStorage.key(i);
      if(k&&k.startsWith('curr:'))keys.push(k);
    }
    keys.forEach(k=>localStorage.removeItem(k));
  }catch(e){}
  curriculumBySubject={};
}
function buildGradeSetupBody(){
  const g=setupActiveGrade;
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  const subjects=gradeSubjectsMap[g]||[];
  const sel=setupData[g]||{subjects:[],classes:{}};
  let html=`<div style="margin:10px 0 6px;font-weight:700;font-size:13px;color:var(--gold)">📖 الصف ${arabicNums[g-1]} — اختر المواد التي تدرّسها:</div>`;
  html+=`<div class="grades-grid">`+subjects.map(s=>
    `<button class="class-chip-btn ${sel.subjects.includes(s)?'sel':''}" onclick="toggleGradeSubject('${s.replace(/'/g,"\\'")}',this)">${s}</button>`
  ).join('')+`</div>`;
  // شعب الصف (مشتركة لكل مواد هذا الصف)
  if(sel.subjects.length){
    const presets=Array.from({length:12},(_,i)=>`${g}/${i+1}`);
    const chosen=sel.classes[g]||[];
    html+=`<div style="margin:14px 0 6px;font-weight:700;font-size:13px;color:var(--gold)">👥 حدّد شعب الصف ${arabicNums[g-1]} (12 شعبة جاهزة):</div>`;
    html+=`<div class="grades-grid">`+
      presets.map(p=>`<button class="class-chip-btn ${chosen.includes(p)?'sel':''}" onclick="toggleGradeClass('${p}',this)">${p}</button>`).join('')+
      `</div>`;
  }
  document.getElementById('grade-setup-body').innerHTML=html;
  updateLessonsPreview();
}
function toggleGradeSubject(subj,btn){
  const d=setupData[setupActiveGrade];
  const i=d.subjects.indexOf(subj);
  if(i>=0){d.subjects.splice(i,1);btn.classList.remove('sel');}
  else{d.subjects.push(subj);btn.classList.add('sel');}
  buildGradeTabs();
  buildGradeSetupBody();
}
function toggleGradeClass(cls,btn){
  const g=setupActiveGrade;
  const d=setupData[g];
  d.classes[g]=d.classes[g]||[];
  const i=d.classes[g].indexOf(cls);
  if(i>=0){d.classes[g].splice(i,1);btn.classList.remove('sel');}
  else{d.classes[g].push(cls);btn.classList.add('sel');}
  updateLessonsPreview();
}
function goToStep1(){
  document.getElementById('setup-step-2').style.display='none';
  document.getElementById('setup-step-1').style.display='block';
  document.getElementById('step-2').classList.remove('active');
  document.getElementById('step-1').classList.remove('done');document.getElementById('step-1').classList.add('active');
}
async function updateLessonsPreview(){
  const card=document.getElementById('lessons-preview-card');
  const box=document.getElementById('lessons-preview');
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  let lines=[];
  for(const g of setupGrades){
    const d=setupData[g];if(!d||!d.subjects.length)continue;
    for(const s of d.subjects){
      const rows=await ensureContent(s,g);
      if(rows.length){
        const units=[...new Set(rows.map(r=>r.unit))].length;
        lines.push(`✅ الصف ${arabicNums[g-1]} — ${s}: ${rows.length} درس / ${units} وحدة`);
      }else{
        lines.push(`🕓 الصف ${arabicNums[g-1]} — ${s}: المحتوى قيد الإعداد`);
      }
    }
  }
  if(!lines.length){card.style.display='none';return;}
  card.style.display='block';
  box.innerHTML=lines.join('<br/>');
}
// id ثابت لكل درس: مبني على (الفصل|المادة|الصف|الوحدة|الدرس)
// نفس الدرس يأخذ نفس الـ id دائماً → المرفقات تبقى مرتبطة به حتى بعد سنوات
function stableLessonId(semester,subject,grade,unit,lesson){
  const raw=`${semester}|${subject}|${grade}|${unit}|${lesson}`;
  let h=5381;
  for(let i=0;i<raw.length;i++){h=((h<<5)+h+raw.charCodeAt(i))>>>0;}
  return 'L'+h.toString(36);
}
function buildUnitsFromRows(rows,semester,subject){
  const sorted=rows.slice().sort((a,b)=>(a.sort||0)-(b.sort||0));
  const unitsMap={};const order=[];
  sorted.forEach(r=>{
    if(!unitsMap[r.unit]){unitsMap[r.unit]=[];order.push(r.unit);}
    unitsMap[r.unit].push({id:stableLessonId(semester,subject,r.grade,r.unit,r.lesson),name:r.lesson});
  });
  return order.map(u=>({name:u,lessons:unitsMap[u]}));
}
// ─── Step 3: رفع طلاب الشعب ───
let _setupStudents={}; // {classId: [{name,phone}]}

function goToStep3(){
  // تحقق من إتمام Step 2
  const chosenGrades=setupGrades.filter(g=>setupData[g]&&setupData[g].subjects.length);
  if(!chosenGrades.length){toast('❌ اختر مادة واحدة على الأقل',true);return;}
  for(const g of chosenGrades){
    const d=setupData[g];
    if(!(d.classes[g]||[]).length){toast(`❌ اختر شعبة للصف ${g}`,true);return;}
  }
  
  // الانتقال
  document.getElementById('setup-step-2').style.display='none';
  document.getElementById('setup-step-3').style.display='block';
  document.getElementById('step-2').classList.remove('active');
  document.getElementById('step-3').classList.add('active');
  
  renderSetupClassesList();
}

function renderSetupClassesList(){
  const wrap=document.getElementById('setup-classes-list');
  if(!wrap)return;
  
  // بناء قائمة الشعب
  const chosenGrades=setupGrades.filter(g=>setupData[g]&&setupData[g].subjects.length);
  const classes=[];
  for(const g of chosenGrades){
    const d=setupData[g];
    for(const s of d.subjects){
      (d.classes[g]||[]).forEach((cls,k)=>{
        const classId=`cls_${s}_${g}_${k}`.replace(/\s/g,'_');
        classes.push({id:classId, name:cls, grade:g, subject:s});
      });
    }
  }
  
  if(!classes.length){
    wrap.innerHTML='<div style="color:var(--muted);text-align:center;padding:20px;">لا توجد شعب</div>';
    return;
  }
  
  wrap.innerHTML=classes.map(c=>{
    const hasData=_setupStudents[c.id]&&_setupStudents[c.id].length;
    return `<div class="setup-class-row ${hasData?'has-students':''}">
      <div class="scr-name">📚 ${escHtml(c.subject)} — ${escHtml(c.name)} <span style="font-size:11px;color:var(--muted);font-weight:400">(الصف ${c.grade})</span></div>
      ${hasData?`<span class="scr-status filled">✓ ${_setupStudents[c.id].length} طالب</span>`:'<span class="scr-status empty">⚠️ لم تُرفع بعد</span>'}
      <div class="scr-actions">
        <label class="scr-upload">
          📂 ${hasData?'تغيير':'رفع Excel'}
          <input type="file" accept=".xlsx,.xls,.csv" style="display:none" onchange="uploadSetupClassExcel(event,'${c.id}')"/>
        </label>
        ${hasData?`<button class="scr-skip" onclick="clearSetupClass('${c.id}')">🗑️ مسح</button>`:''}
      </div>
    </div>`;
  }).join('');
  
  // ملخص
  const filled=classes.filter(c=>_setupStudents[c.id]&&_setupStudents[c.id].length).length;
  const total=classes.length;
  if(filled<total){
    wrap.innerHTML+=`<div style="margin-top:8px;padding:10px 14px;background:rgba(240,192,96,.08);border:1px solid rgba(240,192,96,.25);border-radius:10px;font-size:12px;color:var(--gold);line-height:1.6;">
      💡 رفعت <strong>${filled}</strong> من <strong>${total}</strong> شعبة. يمكنك تخطّي الباقي وإكمالها لاحقاً من قائمة حسابك.
    </div>`;
  }else{
    wrap.innerHTML+=`<div style="margin-top:8px;padding:10px 14px;background:rgba(0,166,81,.08);border:1px solid rgba(0,212,106,.25);border-radius:10px;font-size:12px;color:var(--green2);text-align:center;font-weight:700;">
      ✅ رفعت جميع الشعب! جاهز للبدء
    </div>`;
  }
}

async function uploadSetupClassExcel(event, classId){
  const file=event.target.files[0];
  if(!file)return;
  event.target.value='';
  toast('⏳ جاري قراءة الملف...');
  
  if(!window.XLSX){
    const s=document.createElement('script');
    s.src='https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
    document.head.appendChild(s);
    await new Promise(r=>s.onload=r);
  }
  
  const reader=new FileReader();
  reader.onload=e=>{
    try{
      const wb=XLSX.read(e.target.result,{type:'binary'});
      const ws=wb.Sheets[wb.SheetNames[0]];
      const rows=XLSX.utils.sheet_to_json(ws,{header:1});
      if(!rows.length){toast('❌ الملف فارغ',true);return;}
      
      // البحث عن عمود الاسم والهاتف
      const nameKW=['اسم الطالب','الاسم','اسم','student','name','طالب','أسماء'];
      const phoneKW=['الهاتف النقال','هاتف ولي','ولي الأمر','هاتف','جوال','رقم','phone','mobile'];
      let nameCol=-1, phoneCol=-1, headerRow=0;

      // المرور الأول: نبحث عن صف يحتوي على الاسم والهاتف معاً (الأولوية)
      for(let ri=0;ri<Math.min(50,rows.length);ri++){
        const row=rows[ri]||[];
        let fn=-1,fp=-1;
        row.forEach((cell,ci)=>{
          const v=String(cell||'').trim().replace(/\u0640/g,'').toLowerCase();
          if(fn<0&&nameKW.some(kw=>v.includes(kw))){fn=ci;}
          if(fp<0&&phoneKW.some(kw=>v.includes(kw))){fp=ci;}
        });
        if(fn>=0&&fp>=0){nameCol=fn;phoneCol=fp;headerRow=ri;break;}
      }

      // المرور الثاني: إذا لم نجد الاثنين معاً، نقبل الاسم فقط
      if(nameCol<0){
        for(let ri=0;ri<Math.min(50,rows.length);ri++){
          const row=rows[ri]||[];
          row.forEach((cell,ci)=>{
            const v=String(cell||'').trim().replace(/\u0640/g,'').toLowerCase();
            if(nameCol<0&&nameKW.some(kw=>v.includes(kw))){nameCol=ci;headerRow=ri;}
            if(phoneCol<0&&phoneKW.some(kw=>v.includes(kw))){phoneCol=ci;}
          });
          if(nameCol>=0)break;
        }
      }
      
      if(nameCol<0){toast('❌ لم يتم التعرف على عمود الاسم',true);return;}
      
      const studentsList=[];
      rows.slice(headerRow+1).forEach(r=>{
        if(!r)return;
        const name=String(r[nameCol]||'').trim();
        const phone=phoneCol>=0?String(r[phoneCol]||'').trim():'';
        if(name&&name.length>1&&!/^\d+$/.test(name)&&!nameKW.some(kw=>name.toLowerCase().replace(/\u0640/g,'').includes(kw))){
          studentsList.push({name, phone});
        }
      });
      
      if(!studentsList.length){toast('❌ لم يتم العثور على طلاب',true);return;}
      
      // ترتيب أبجدي
      studentsList.sort((a,b)=>a.name.localeCompare(b.name,'ar'));
      _setupStudents[classId]=studentsList;
      
      renderSetupClassesList();
      toast(`✅ تم تحميل ${studentsList.length} طالب`,'ok');
    }catch(err){
      toast('❌ خطأ في قراءة الملف: '+err.message,true);
    }
  };
  reader.readAsBinaryString(file);
}

function clearSetupClass(classId){
  if(!confirm('هل تريد مسح قائمة هذه الشعبة؟'))return;
  delete _setupStudents[classId];
  renderSetupClassesList();
}

async function finishSetup(){
  // تحقق: كل صف له مادة واحدة على الأقل وشعبة واحدة
  const chosenGrades=setupGrades.filter(g=>setupData[g]&&setupData[g].subjects.length);
  if(!chosenGrades.length){toast('❌ اختر مادة واحدة على الأقل لصف واحد',true);return;}
  for(const g of chosenGrades){
    const d=setupData[g];
    if(!(d.classes[g]||[]).length){toast(`❌ اختر شعبة للصف ${g}`,true);return;}
  }
  // ابنِ grades: كل (صف+مادة) عنصر مستقل
  const grades=[];let ci=0;
  for(const g of chosenGrades){
    const d=setupData[g];
    for(const s of d.subjects){
      const rows=await ensureContent(s,g);
      grades.push({
        num:g,
        subject:s,
        classes:(d.classes[g]||[]).map((cls,k)=>({id:`cls_${s}_${g}_${k}`.replace(/\s/g,'_'),name:cls,color:GRADE_COLORS[(ci++)%GRADE_COLORS.length]})),
        units:buildUnitsFromRows(rows,setupSemester,s),
      });
    }
  }
  const allSubjects=[...new Set(grades.map(x=>x.subject))];
  const config={grades,subjects:allSubjects,subject:allSubjects[0],semester:setupSemester,setupDone:true};
  
  // تطبيق طلاب الشعب من Step 3 على students وbehaviorStudents
  Object.keys(_setupStudents).forEach(classId=>{
    const list=_setupStudents[classId]||[];
    const formattedList=list.map(s=>({
      id:'s_'+Date.now()+'_'+Math.random().toString(36).slice(2,7),
      name:s.name,
      phone:s.phone||''
    }));
    students[classId]=formattedList;
    behaviorStudents[classId]=formattedList.map(s=>({...s}));
  });
  // حافظ على البيانات القديمة: المرفقات لا تُمسح (الـ id ثابت فترجع تلقائياً)
  // وأرشِف الإعداد السابق احتياطياً
  const prev=await dbLoad().catch(()=>null);
  const archive=(prev&&prev.config_archive)?prev.config_archive:[];
  if(prev&&prev.teacher_config&&prev.teacher_config.setupDone){
    archive.push({archivedAt:new Date().toISOString(),teacher_config:prev.teacher_config});
    if(archive.length>20)archive.shift(); // احتفظ بآخر 20 إعداد
  }
  await dbSave({
    teacher_config:config,
    config_archive:archive,
    students:students,
    behavior_students:behaviorStudents,
    // نُبقي المرفقات والحالة كما هي (لا نصفّرها) — الـ id الثابت يعيد ربطها
    lesson_files:(prev&&prev.lesson_files)||{},
    plan_state:(prev&&prev.plan_state)||{},
    arc_meta:(prev&&prev.arc_meta)||{},
    cv_items:(prev&&prev.cv_items)||[],
    cv_profile:(prev&&prev.cv_profile)||{},
    arc_categories:(prev&&prev.arc_categories)||DEFAULT_CATS,
    timetable_config:(prev&&prev.timetable_config)||{},
    class_config:(prev&&prev.class_config)||{},
    grades:(prev&&prev.grades)||{},
    grade_types:(prev&&prev.grade_types)||[],
    reminders_config:(prev&&prev.reminders_config)||{enabled:false,minutes:10}
  });
  document.getElementById('setup-screen').classList.add('hidden');
  const data=await dbLoad();
  showApp(data);
  toast('🎉 تم الإعداد بنجاح!','ok');
}

// ══ APP INIT ══════════════════════════════════════════
const DEFAULT_CATS=[
  {id:'homework',title:'الواجبات',icon:'📝'},{id:'quiz1',title:'الاختبارات القصيرة الأولى',icon:'📋'},
  {id:'quiz2',title:'الاختبارات القصيرة الثانية',icon:'📋'},{id:'short1',title:'السؤال القصير الأول',icon:'❓'},
  {id:'short2',title:'السؤال القصير الثاني',icon:'❓'},{id:'project',title:'المشروع',icon:'🎯'},
  {id:'finals',title:'تجميع اختبارات نهائية',icon:'📚'},
];


let state={};let arcMeta={};let arcCategories=[];let cvItems=[];let cvProfile={};
let lessonFiles={};let timetableConfig=null;let classConfig=null;let ttEditing=false;let ttBackup=null;
let students={};let grades={};let gradeTypes=[];let remindersConfig={enabled:false,minutes:10};
let activeGradesClass=null;let reminderState={};let teacherConfig=null;
let currentTrackerIdx=0;

const DEFAULT_PERIODS=[
  {num:1,start:'7:25 AM',end:'8:05 AM'},{num:2,start:'8:10 AM',end:'8:50 AM'},
  {num:3,start:'8:55 AM',end:'9:35 AM'},{num:4,start:'9:35 AM',end:'10:15 AM'},
  {num:5,start:'10:40 AM',end:'11:20 AM'},{num:6,start:'11:20 AM',end:'12:00 PM'},
  {num:7,start:'12:00 PM',end:'12:40 PM'},{num:8,start:'1:00 PM',end:'1:40 PM'},
];
const DEFAULT_DAYS=[{id:'sun',name:'أحد'},{id:'mon',name:'أثنين'},{id:'tue',name:'ثلاثاء'},{id:'wed',name:'أربعاء'},{id:'thu',name:'خميس'}];

// ══ ثيمات المواد ══════════════════════════════════════
// كل مادة فرعية → مادتها الأساسية
const SUBJECT_BASE={
  'رياضيات':'الرياضيات','الرياضيات الأساسية':'الرياضيات','الرياضيات المتقدمة':'الرياضيات',
  'العلوم':'العلوم','أحياء':'العلوم','كيمياء':'العلوم','فيزياء':'العلوم','العلوم البيئية':'العلوم',
  'ديني قيمي':'التربية الإسلامية','التربية الإسلامية':'التربية الإسلامية',
  'الدراسات الاجتماعية':'الاجتماعيات','الجغرافيا الاقتصادية':'الاجتماعيات','الجغرافيا والتقنيات الحديثة':'الاجتماعيات','هذا وطني':'الاجتماعيات','العالم من حولي':'الاجتماعيات',
  'لغتي الجميلة':'اللغة العربية',
  'لغة إنجليزية':'اللغة الإنجليزية',
  'تقنية المعلومات':'تقنية المعلومات',
};
// لكل مادة أساسية: شخصية بصرية كاملة (ألوان + نمط خلفية + رموز + خط)
const SUBJECT_THEMES={
  'الرياضيات':{
    accent:'#f0c060',accent2:'#d4a030',red:'#c0392b',red2:'#e74c3c',
    dark:{bg:'#0d0a07',surface:'#1a1410',card:'#211a12',border:'#3d3020'},
    light:{accent:'#8a6000',accent2:'#6e4c00',red:'#c0392b',red2:'#e74c3c'}
  },
  'العلوم':{
    accent:'#2ee59d',accent2:'#1fae77',red:'#16a085',red2:'#1abc9c',
    dark:{bg:'#07120e',surface:'#0d1f19',card:'#112821',border:'#1d4438'},
    light:{accent:'#0a7a5a',accent2:'#086248',red:'#0e8a6a',red2:'#16a085'}
  },
  'التربية الإسلامية':{
    accent:'#1fc9a6',accent2:'#159e82',red:'#27ae60',red2:'#2ecc71',
    dark:{bg:'#06120f',surface:'#0c1f1a',card:'#102823',border:'#1b443a'},
    light:{accent:'#0e6e3a',accent2:'#0a5830',red:'#1a7a44',red2:'#229954'}
  },
  'الاجتماعيات':{
    accent:'#f0a050',accent2:'#d97e2a',red:'#cd6133',red2:'#e58e26',
    dark:{bg:'#120d06',surface:'#1f170d',card:'#281e11',border:'#40321c'},
    light:{accent:'#8a4010',accent2:'#6e3208',red:'#8a3a18',red2:'#a04e20'}
  },
  'اللغة العربية':{
    accent:'#e8554a',accent2:'#c0392b',red:'#a93226',red2:'#e74c3c',
    dark:{bg:'#120807',surface:'#1f0f0e',card:'#281312',border:'#421f1d'},
    light:{accent:'#8a1a14',accent2:'#700e0a',red:'#8a1a14',red2:'#c0392b'}
  },
  'اللغة الإنجليزية':{
    accent:'#b06fd0',accent2:'#8e44ad',red:'#7d3c98',red2:'#a569bd',
    dark:{bg:'#0e0812',surface:'#180f20',card:'#1f1429',border:'#341f42'},
    light:{accent:'#6020a0',accent2:'#4e1888',red:'#5a1a90',red2:'#7d3c98'}
  },
  'تقنية المعلومات':{
    accent:'#4aa8e8',accent2:'#2980b9',red:'#2471a3',red2:'#5dade2',
    dark:{bg:'#060d12',surface:'#0c161f',card:'#101d28',border:'#1a3242'},
    light:{accent:'#1058a0',accent2:'#0c4688',red:'#0e5090',red2:'#1a6ab8'}
  }
};
function detectBaseSubject(cfg){
  if(!cfg||!cfg.grades||!cfg.grades.length)return null;
  const count={};
  cfg.grades.forEach(g=>{
    const base=SUBJECT_BASE[g.subject]||g.subject;
    count[base]=(count[base]||0)+1;
  });
  let best=null,max=0;
  Object.keys(count).forEach(b=>{if(count[b]>max){max=count[b];best=b;}});
  return best;
}
function applySubjectTheme(cfg){
  const base=detectBaseSubject(cfg);
  const t=SUBJECT_THEMES[base];
  const root=document.documentElement;
  const clear=()=>['--bg','--surface','--card','--border','--gold','--gold2','--red','--red2'].forEach(v=>root.style.removeProperty(v));
  clear();
  if(!t)return; // افتراضي = ثيم الرياضيات الأصلي عبر :root
  const isLight=document.body.classList.contains('light-mode');
  const pal=t.dark;
  root.style.setProperty('--bg',pal.bg);
  root.style.setProperty('--surface',pal.surface);
  root.style.setProperty('--card',pal.card);
  root.style.setProperty('--border',pal.border);
  // في النهاري: استخدم الألوان الأغمق للقراءة الجيدة
  const colors=isLight&&t.light?t.light:t;
  root.style.setProperty('--gold',colors.accent);
  root.style.setProperty('--gold2',colors.accent2);
  root.style.setProperty('--red',colors.red);
  root.style.setProperty('--red2',colors.red2);
}

function showApp(data){
  document.getElementById('main-nav').style.display='flex';
  document.querySelectorAll('.page')[0].classList.add('active');
  showUserBadge();

  if(data){
    state=data.plan_state||{};
    arcMeta=data.arc_meta||{};
    cvItems=data.cv_items||[];
    cvProfile=data.cv_profile||{};
    lessonFiles=data.lesson_files||{};
    arcCategories=data.arc_categories||DEFAULT_CATS;
    teacherConfig=data.teacher_config||null;
    remindersConfig=data.reminders_config||{enabled:false,minutes:10};
    students=data.students||{};
    grades=data.grades||{};
    gradeTypes=data.grade_types||[];
    cvProfile=data.cv_profile||{};
    // تحميل بيانات السلوك من Supabase
    behaviorStudents=data.behavior_students||{};
    behaviorViolations=data.behavior_violations||{};
    if(data.behavior_teacher_phone){
      localStorage.setItem('behaviorTeacherPhone',data.behavior_teacher_phone);
    }

    // Build classConfig from teacherConfig
    classConfig={};
    if(teacherConfig&&teacherConfig.grades){
      teacherConfig.grades.forEach(g=>{
        g.classes.forEach(cls=>{classConfig[cls.id]={name:cls.name,color:cls.color};});
      });
    }
    // Build timetableConfig
    if(data.timetable_config&&data.timetable_config.days){
      timetableConfig=data.timetable_config;
    } else {
      timetableConfig={days:DEFAULT_DAYS,periods:DEFAULT_PERIODS,schedule:{}};
    }
  } else {
    arcCategories=DEFAULT_CATS;
    timetableConfig={days:DEFAULT_DAYS,periods:DEFAULT_PERIODS,schedule:{}};
    classConfig={};
  }

  updateTeacherBanner();
  applySubjectTheme(teacherConfig);
  renderTimetable();
  renderLegend();
  buildTracker();
  applyFilter();
  update();
  loadCvProfile();
  loadRemindersUI();
  startClassWatcher();
  // تشغيل نظام الإشعارات
  initPushNotifications();
  
  // تهيئة التقويم والمهام
  renderCalendar();
  renderTasks();
  
  // تحميل المكتبة العامة
  loadLibrary();
  
  // تحديث أزرار المشرف
  if(typeof updateAdminButtons==='function')updateAdminButtons();
  // تحديث نص زر الإشعارات
  updateNotifMenuBtn();
}

function updateTeacherBanner(){
  const tb=document.getElementById('teacher-name-banner');
  if(tb)tb.textContent=displayName||'الأستاذ';
  const sub=document.getElementById('teacher-sub-banner');
  if(sub&&teacherConfig){
    const subject=teacherConfig.subject||'';
    const grades=teacherConfig.grades?.map(g=>`الصف ${g.num}`).join(' · ')||'';
    sub.textContent=`${subject} — ${grades}`;
  }
}

// ══ THEME ═════════════════════════════════════════════
let isDark=true;
function toggleTheme(){
  isDark=!isDark;
  document.body.classList.toggle('light-mode',!isDark);
  document.getElementById('theme-btn').textContent=isDark?'🌙':'☀️';
  localStorage.setItem('theme',isDark?'dark':'light');
  if(typeof teacherConfig!=='undefined'&&teacherConfig)applySubjectTheme(teacherConfig);
}
(function(){
  const t=localStorage.getItem('theme');
  if(t==='light'){
    isDark=false;
    document.body.classList.add('light-mode');
    document.getElementById('theme-btn').textContent='☀️';
  }
})();

// ══ NAV ════════════════════════════════════════════════
function showPage(id,btn){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active','ripple'));
  document.getElementById('page-'+id).classList.add('active');
  btn.classList.add('active','ripple');
  setTimeout(()=>btn.classList.remove('ripple'),600);
  if(id==='archive')loadArchive();
  if(id==='cv'){renderCv();loadCvProfile();}
  if(id==='grades'){setTimeout(()=>{renderGrades();if(isAdmin())loadAdminTemplates();},150);}

  if(id==='stats')renderStats();
  if(id==='library')loadLibrary();
  if(id==='behavior')initBehaviorPage();
  if(id==='surveys'){loadSurveyResults();renderSurveyBuilder();}
  if(id==='analytics')loadAnalytics();
  if(id==='users'){loadAdminUsers();loadInvites();}
  if(id==='announcements')loadAnnouncements();
  if(id==='users')loadAdminUsers();
  if(id==='timetable')loadAnnouncementBanner();
  if(id==='tracker'){
    setTimeout(()=>{
    if(isAdmin()){
      const semEl=document.getElementById('acs-semester');
      const gradeEl=document.getElementById('acs-grade');
      if(semEl&&teacherConfig&&teacherConfig.semester)semEl.value=teacherConfig.semester;
      if(gradeEl&&teacherConfig&&teacherConfig.grades&&teacherConfig.grades.length)gradeEl.value=teacherConfig.grades[0];
      loadAdminCurriculumSummary();
    }
    },50);
  }
}
const dayMap2={0:'sun',1:'mon',2:'tue',3:'wed',4:'thu'};
function currentDayKey(){const d=new Date().getDay();return({0:'sun',1:'mon',2:'tue',3:'wed',4:'thu',5:'fri',6:'sat'})[d];}

// ══ TIMETABLE ══════════════════════════════════════════
function getClassColor(key){return classConfig[key]?classConfig[key].color:'var(--text)';}
function hexToRgba(hex,alpha){if(!hex||!hex.startsWith('#'))return`rgba(192,57,43,${alpha})`;const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return`rgba(${r},${g},${b},${alpha})`;}
function renderLegend(){
  const el=document.getElementById('legend');
  if(!el)return; // العنصر غير موجود (مثلاً وضع المشرف)
  if(!classConfig)return;
  el.innerHTML=Object.keys(classConfig).map(k=>{const c=classConfig[k];return`<div class="leg-item"><div class="leg-dot" style="background:${c.color}"></div>${c.name}</div>`;}).join('');
}
function renderTimetable(){
  const head=document.getElementById('tt-head');const body=document.getElementById('tt-body');
  if(!head||!body)return; // عناصر غير موجودة
  const cfg=timetableConfig;
  if(!cfg||!cfg.periods)return;
  const todayKey=currentDayKey();
  let headHtml='<tr><th><div class="th-inner">اليوم</div></th>';
  cfg.periods.forEach((p,idx)=>{
    if(ttEditing){
      headHtml+=`<th><div class="th-inner"><button class="col-del" onclick="delPeriod(${idx})">✕</button><div class="th-num">${p.num}</div><div class="th-time-edit"><input type="text" value="${p.start}" onchange="updPeriod(${idx},'start',this.value)" placeholder="7:25 AM"/><input type="text" value="${p.end}" onchange="updPeriod(${idx},'end',this.value)" placeholder="8:05 AM"/></div></div></th>`;
    } else {
      headHtml+=`<th><div class="th-inner"><div class="th-num">${p.num}</div><div class="th-time"><span>${p.start.split(' ')[0]}</span> ${p.start.split(' ')[1]||''}<br/>${p.end}</div></div></th>`;
    }
  });
  if(ttEditing)headHtml+='<th><div class="th-inner"><button class="col-add-btn" onclick="addPeriod()">➕</button></div></th>';
  headHtml+='</tr>';head.innerHTML=headHtml;
  let bodyHtml='';
  cfg.days.forEach(day=>{
    const isToday=day.id===todayKey;
    bodyHtml+=`<tr${isToday?' class="today"':''} id="row-${day.id}"><td>${day.name}</td>`;
    cfg.periods.forEach((p,idx)=>{
      const classKey=(cfg.schedule[day.id]||{})[idx];
      if(classKey&&classConfig[classKey]){
        const col=classConfig[classKey].color;const bg=hexToRgba(col,.18);const br=hexToRgba(col,.35);
        bodyHtml+=`<td><div class="cell" style="background:${bg};color:${col};border:1px solid ${br};" onclick="${ttEditing?`cycleCell('${day.id}',${idx})`:''}">${ttEditing?`<button class="cell-del" onclick="event.stopPropagation();clearCell('${day.id}',${idx})">✕</button>`:''}<span class="cls">${classConfig[classKey].name}</span><span class="sub">${teacherConfig?.subject||'المادة'}</span></div></td>`;
      } else {
        bodyHtml+=`<td class="cell-empty" ${ttEditing?`onclick="cycleCell('${day.id}',${idx})"`:''}></td>`;
      }
    });
    if(ttEditing)bodyHtml+='<td class="cell-empty"></td>';
    bodyHtml+='</tr>';
  });
  body.innerHTML=bodyHtml;
  const ttw=document.getElementById('tt-wrap');
  if(ttw)ttw.classList.toggle('editing',ttEditing);
}
function toggleEditMode(){
  ttEditing=true;ttBackup=JSON.parse(JSON.stringify({timetableConfig,classConfig}));
  document.getElementById('tt-edit').style.display='none';
  document.getElementById('tt-save').style.display='inline-flex';
  document.getElementById('tt-cancel').style.display='inline-flex';
  document.getElementById('class-config').classList.add('active');
  renderClassConfig();renderTimetable();
}
function cancelEdit(){if(!confirm('إلغاء التعديلات؟'))return;timetableConfig=ttBackup.timetableConfig;classConfig=ttBackup.classConfig;exitEditMode();}
function saveTimetable(){exitEditMode();buildTracker();applyFilter();update();toast('✅ تم حفظ الجدول','ok');scheduleSave();}
function exitEditMode(){
  ttEditing=false;ttBackup=null;
  document.getElementById('tt-edit').style.display='inline-flex';
  document.getElementById('tt-save').style.display='none';
  document.getElementById('tt-cancel').style.display='none';
  document.getElementById('class-config').classList.remove('active');
  renderTimetable();renderLegend();
}
function renderClassConfig(){
  const list=document.getElementById('ccfg-list');const keys=Object.keys(classConfig);
  list.innerHTML=keys.map((k,i)=>{const c=classConfig[k];return`<div class="ccfg-row"><input type="text" value="${c.name}" onchange="updClassName('${k}',this.value)" placeholder="اسم الشعبة"/><input type="color" value="${c.color}" onchange="updClassColor('${k}',this.value)"/>${keys.length>1?`<button class="del-class" onclick="delClass('${k}')">حذف</button>`:''}</div>`;}).join('');
}
function updClassName(key,name){classConfig[key].name=name.trim()||key;}
function updClassColor(key,color){classConfig[key].color=color;renderTimetable();}
function addClassColor(){const newKey='cls_'+Date.now();classConfig[newKey]={name:'شعبة جديدة',color:'#'+Math.floor(Math.random()*16777215).toString(16).padStart(6,'0')};renderClassConfig();}
function delClass(key){if(Object.keys(classConfig).length<=1){toast('❌ لا يمكن حذف آخر شعبة',true);return;}if(!confirm('حذف هذه الشعبة؟'))return;delete classConfig[key];Object.keys(timetableConfig.schedule).forEach(dayId=>{Object.keys(timetableConfig.schedule[dayId]).forEach(pIdx=>{if(timetableConfig.schedule[dayId][pIdx]===key)delete timetableConfig.schedule[dayId][pIdx];});});renderClassConfig();renderTimetable();}
function addPeriod(){const last=timetableConfig.periods[timetableConfig.periods.length-1];timetableConfig.periods.push({num:last?last.num+1:1,start:'',end:''});renderTimetable();}
function delPeriod(idx){if(timetableConfig.periods.length<=1){toast('❌ لا يمكن حذف آخر حصة',true);return;}if(!confirm('حذف هذه الحصة؟'))return;timetableConfig.periods.splice(idx,1);Object.keys(timetableConfig.schedule).forEach(dayId=>{const newDay={};Object.keys(timetableConfig.schedule[dayId]).forEach(pIdx=>{const i=parseInt(pIdx);if(i<idx)newDay[i]=timetableConfig.schedule[dayId][pIdx];else if(i>idx)newDay[i-1]=timetableConfig.schedule[dayId][pIdx];});timetableConfig.schedule[dayId]=newDay;});renderTimetable();}
function updPeriod(idx,field,val){timetableConfig.periods[idx][field]=val.trim();}
function cycleCell(dayId,pIdx){if(!timetableConfig.schedule[dayId])timetableConfig.schedule[dayId]={};const keys=Object.keys(classConfig);const current=timetableConfig.schedule[dayId][pIdx];let nextIdx;if(!current)nextIdx=0;else{const ci=keys.indexOf(current);nextIdx=ci+1;}if(nextIdx>=keys.length){delete timetableConfig.schedule[dayId][pIdx];}else{timetableConfig.schedule[dayId][pIdx]=keys[nextIdx];}renderTimetable();}
function clearCell(dayId,pIdx){if(timetableConfig.schedule[dayId])delete timetableConfig.schedule[dayId][pIdx];renderTimetable();}

// ══ TRACKER ════════════════════════════════════════════
const get=id=>state[id]||{done:false,date:'',sessions:'',notes:'',classes:{}};

function allLessons(){
  if(!teacherConfig||!teacherConfig.grades)return[];
  const grade=teacherConfig.grades[currentTrackerIdx]||teacherConfig.grades[0];
  if(!grade)return[];
  return grade.units.flatMap(u=>u.lessons);
}

function buildGradeFilterBar(){
  if(!teacherConfig||!teacherConfig.grades)return;
  const bar=document.getElementById('grade-filter-bar');
  // إظهار الشريط دائماً ليرى المعلم كل الصفوف التي اختارها
  if(!teacherConfig.grades.length){bar.style.display='none';return;}
  bar.style.display='flex';
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  if(currentTrackerIdx==null||currentTrackerIdx>=teacherConfig.grades.length)currentTrackerIdx=0;
  // أظهر اسم المادة مع الصف دائماً لوضوح أكبر
  bar.innerHTML=teacherConfig.grades.map((g,idx)=>{
    const lessonsCount=(g.units||[]).reduce((sum,u)=>sum+(u.lessons||[]).length,0);
    const label=`${g.subject||''} — الصف ${arabicNums[(g.num||1)-1]}`;
    const badge=lessonsCount?` <span style="opacity:.7;font-size:10px">(${lessonsCount})</span>`:' <span style="color:var(--red);font-size:10px">⚠</span>';
    return `<button class="grade-filter-btn ${idx===currentTrackerIdx?'active':''}" onclick="switchTrackerGrade(${idx},this)">${label}${badge}</button>`;
  }).join('');
}

function switchTrackerGrade(idx,btn){
  currentTrackerIdx=idx;
  document.querySelectorAll('.grade-filter-btn').forEach(b=>b.classList.remove('active'));
  if(btn)btn.classList.add('active');
  buildTracker();applyFilter();update();
}

// ════════════════════════════════════════════════════════════════
// 📥 رفع محتوى المنهج من داخل الموقع (للمشرف فقط)
// ════════════════════════════════════════════════════════════════
let _parsedContent=null;

function openContentUploader(){
  if(!isAdmin()){toast('❌ هذه الميزة للمشرف فقط',true);return;}
  document.getElementById('content-uploader-modal').style.display='flex';
  // ضبط الفصل من الإعداد الحالي
  if(teacherConfig&&teacherConfig.semester){
    document.getElementById('up-semester').value=teacherConfig.semester;
  }
  // ضبط الصف من الإعداد الحالي
  const info=getCurrentClassInfo();
  if(info&&info.grade){
    document.getElementById('up-grade').value=info.grade;
  }
  // تحميل قائمة المواد بناءً على الصف المختار
  updateUploaderSubjects();
  document.getElementById('up-content').value='';
  document.getElementById('up-preview').style.display='none';
  document.getElementById('up-save-btn').disabled=true;
  _parsedContent=null;
}
function closeContentUploader(){
  document.getElementById('content-uploader-modal').style.display='none';
}

// تحديث قائمة المواد من Supabase مباشرة عند تغيير الصف أو الفصل
async function updateUploaderSubjects(){
  const grade=parseInt(document.getElementById('up-grade').value);
  const semester=document.getElementById('up-semester').value;
  const sel=document.getElementById('up-subject');
  const prevVal=sel.value;
  sel.innerHTML='<option value="">⏳ جاري التحميل...</option>';
  sel.disabled=true;
  try{
    const{data,error}=await sb.from('subjects')
      .select('subject').eq('grade',grade).eq('semester',semester).order('sort');
    if(error)throw error;
    const subjects=[...new Set((data||[]).map(r=>r.subject))];
    if(!subjects.length){
      sel.innerHTML='<option value="">— لا توجد مواد لهذا الصف —</option>';
    }else{
      sel.innerHTML='<option value="">— اختر المادة —</option>'+
        subjects.map(s=>`<option value="${s}">${s}</option>`).join('');
      if(prevVal&&subjects.includes(prevVal))sel.value=prevVal;
    }
  }catch(e){
    sel.innerHTML='<option value="">— خطأ في التحميل —</option>';
    toast('❌ خطأ في تحميل المواد',true);
  }finally{
    sel.disabled=false;
  }
}

// تحليل النص المُدخل إلى وحدات ودروس
function parseUploadedContent(text){
  // تقسيم المحتوى بناءً على سطرين فارغين متتاليين (فواصل الوحدات)
  const unitBlocks=text.split(/\n\s*\n\s*\n+/).map(b=>b.trim()).filter(b=>b.length>0);
  const units=[];
  
  for(const block of unitBlocks){
    const lines=block.split('\n').map(l=>l.trim()).filter(l=>l.length>0);
    if(lines.length===0)continue;
    
    // أول سطر = عنوان الوحدة
    const unitName=lines[0];
    const lessons=[];
    
    // باقي السطور = دروس
    for(let i=1;i<lines.length;i++){
      let lesson=lines[i];
      // إزالة جميع الرموز والأرقام من البداية:
      // - الأرقام العربية والإنجليزية (0-9, ٠-٩)
      // - رموز النقاط والرقام (-, •, *, ●, ○, ◦, ▪, ▫, ①-⑨, إلخ)
      // - يتبعها نقطة أو شرطة أو قوس أو نقطتين
      lesson=lesson.replace(/^[\d٠-٩①-⑨①②③④⑤⑥⑦⑧⑨⑩⑪⑫\-•*●○◦▪▫\[\(\.:\)\-]+\s*/,'').trim();
      if(lesson)lessons.push(lesson);
    }
    
    // إضافة الوحدة فقط إذا كان لديها درس واحد على الأقل
    if(lessons.length>0){
      units.push({name:unitName,lessons:lessons});
    }
  }
  
  return units;
}

function previewContent(){
  const text=document.getElementById('up-content').value.trim();
  if(!text){toast('❌ ألصق المحتوى أولاً',true);return;}
  const units=parseUploadedContent(text);
  if(!units.length){toast('❌ لم يتم العثور على أي وحدات',true);return;}
  const totalLessons=units.reduce((s,u)=>s+u.lessons.length,0);
  if(!totalLessons){toast('❌ لم يتم العثور على أي دروس',true);return;}
  
  let html=`<h4>📋 معاينة: ${units.length} وحدة، ${totalLessons} درس</h4>`;
  units.forEach(u=>{
    html+=`<div class="pv-unit">📂 ${u.name} (${u.lessons.length} درس)</div>`;
    u.lessons.forEach(l=>{html+=`<div class="pv-lesson">└─ ${l}</div>`;});
  });
  
  const pv=document.getElementById('up-preview');
  pv.innerHTML=html;
  pv.style.display='block';
  document.getElementById('up-save-btn').disabled=false;
  _parsedContent=units;
}

async function saveContent(){
  if(!_parsedContent){toast('❌ اضغط معاينة أولاً',true);return;}
  if(!isAdmin()){toast('❌ غير مصرح',true);return;}
  
  const semester=document.getElementById('up-semester').value;
  const subject=document.getElementById('up-subject').value.trim();
  const grade=parseInt(document.getElementById('up-grade').value);
  
  if(!subject){toast('❌ أدخل اسم المادة',true);return;}
  
  const confirmMsg=`سيتم حذف الدروس القديمة (إن وجدت) لـ:\n📘 ${subject} - الصف ${grade} - ${semester}\nواستبدالها بـ ${_parsedContent.reduce((s,u)=>s+u.lessons.length,0)} درس جديد.\n\nهل تريد المتابعة؟`;
  if(!confirm(confirmMsg))return;
  
  const saveBtn=document.getElementById('up-save-btn');
  saveBtn.disabled=true;
  saveBtn.textContent='⏳ جاري الحفظ...';
  
  try{
    // 1. حذف الدروس القديمة
    await sb.from('curriculum').delete()
      .eq('semester',semester).eq('subject',subject).eq('grade',grade);
    
    // 2. تسجيل المادة في جدول subjects (إن لم تكن مسجلة)
    const existing=await sb.from('subjects').select('*')
      .eq('semester',semester).eq('subject',subject).eq('grade',grade);
    if(!existing.data||!existing.data.length){
      await sb.from('subjects').insert([{semester,subject,grade,sort:99}]);
    }
    
    // 3. إنشاء صفوف الدروس
    const rows=[];let sort=1;
    _parsedContent.forEach(u=>{
      u.lessons.forEach(l=>{
        rows.push({semester,subject,grade,unit:u.name,lesson:l,sort:sort++});
      });
    });
    
    // 4. إدراج دفعة واحدة
    const{error}=await sb.from('curriculum').insert(rows);
    if(error)throw error;
    
    // 5. مسح cache
    clearCurriculumCache();
    
    toast(`✅ تم حفظ ${rows.length} درس بنجاح`);
    closeContentUploader();
  }catch(e){
    const msg=e.message||e.details||e.hint||JSON.stringify(e)||'غير معروف';
    console.error('saveContent error:',e);
    toast('❌ خطأ في الحفظ: '+msg,true);
    saveBtn.disabled=false;
    saveBtn.textContent='💾 حفظ';
  }
}

// ════════════════════════════════════════════════════════════════
// ⚙️ إدارة الدروس (تعديل/حذف) للمشرف
// ════════════════════════════════════════════════════════════════
function openLessonsManager(){
  if(!isAdmin()){toast('❌ هذه الميزة للمشرف فقط',true);return;}
  document.getElementById('lessons-manager-modal').style.display='flex';
  const info=getCurrentClassInfo();
  if(info){
    if(teacherConfig&&teacherConfig.semester)
      document.getElementById('mg-semester').value=teacherConfig.semester;
    if(info.grade)document.getElementById('mg-grade').value=info.grade;
  }
  // تحميل المواد أولاً ثم تحديد المادة
  updateManagerSubjects().then(()=>{
    const subjectVal=info?.subject||'';
    if(subjectVal){
      const sel=document.getElementById('mg-subject');
      // انتظر حتى تُحمَّل الخيارات
      setTimeout(()=>{
        if([...sel.options].some(o=>o.value===subjectVal)){
          sel.value=subjectVal;
          loadLessonsForManagement();
        }
      },600);
    }
  });
}
function closeLessonsManager(){
  document.getElementById('lessons-manager-modal').style.display='none';
}

async function updateManagerSubjects(){
  const grade=parseInt(document.getElementById('mg-grade').value);
  const semester=document.getElementById('mg-semester').value;
  const sel=document.getElementById('mg-subject');
  sel.innerHTML='<option value="">⏳ جاري التحميل...</option>';
  sel.disabled=true;
  try{
    const{data,error}=await sb.from('subjects')
      .select('subject').eq('grade',grade).eq('semester',semester).order('sort');
    if(error)throw error;
    const subjects=[...new Set((data||[]).map(r=>r.subject))];
    if(!subjects.length){
      sel.innerHTML='<option value="">— لا توجد مواد لهذا الصف —</option>';
    }else{
      sel.innerHTML='<option value="">— اختر المادة —</option>'+
        subjects.map(s=>`<option value="${s}">${s}</option>`).join('');
    }
  }catch(e){
    sel.innerHTML='<option value="">— خطأ في التحميل —</option>';
  }finally{
    sel.disabled=false;
    document.getElementById('mg-lessons-list').innerHTML='';
  }
}

async function loadLessonsForManagement(){
  const semester=document.getElementById('mg-semester').value;
  const subject=document.getElementById('mg-subject').value;
  const grade=parseInt(document.getElementById('mg-grade').value);
  const listEl=document.getElementById('mg-lessons-list');
  
  if(!subject){listEl.innerHTML='<div class="mg-empty">📝 اختر المادة أولاً</div>';return;}
  
  listEl.innerHTML='<div class="mg-empty">⏳ جاري التحميل...</div>';
  
  try{
    const{data}=await sb.from('curriculum').select('*')
      .eq('semester',semester).eq('subject',subject).eq('grade',grade).order('sort');
    
    if(!data||!data.length){
      listEl.innerHTML=`<div class="mg-empty">📭 لا توجد دروس لـ ${subject} - الصف ${grade}</div>`;
      return;
    }
    
    // تجميع حسب الوحدة
    const byUnit={};
    data.forEach(r=>{
      if(!byUnit[r.unit])byUnit[r.unit]=[];
      byUnit[r.unit].push(r);
    });
    
    let html=`<div style="font-size:11.5px;color:var(--muted);margin-bottom:8px;padding:6px 10px;background:rgba(240,192,96,.05);border-radius:6px;">📊 ${data.length} درس في ${Object.keys(byUnit).length} وحدة</div>`;
    Object.keys(byUnit).forEach(unit=>{
      html+=`<div class="mg-unit-block">`;
      html+=`<div class="mg-unit-title">📂 ${escHtml(unit)}</div>`;
      byUnit[unit].forEach(r=>{
        html+=`<div class="mg-lesson-row">
          <div class="mg-lesson-text">${escHtml(r.lesson)}</div>
          <button class="mg-edit-btn" onclick="editLesson(${r.id})" title="تعديل">✏️</button>
          <button class="mg-del-btn" onclick="deleteLesson(${r.id},'${escAttr(r.lesson)}')" title="حذف">🗑️</button>
        </div>`;
      });
      html+=`</div>`;
    });
    listEl.innerHTML=html;
  }catch(e){
    listEl.innerHTML=`<div class="mg-empty">❌ خطأ: ${e.message||'غير معروف'}</div>`;
  }
}

function escHtml(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function escAttr(s){return String(s||'').replace(/'/g,"\\'").replace(/"/g,'&quot;');}

async function editLesson(id){
  if(!isAdmin())return;
  try{
    const{data}=await sb.from('curriculum').select('*').eq('id',id).single();
    if(!data){toast('❌ الدرس غير موجود',true);return;}
    const newLesson=prompt('تعديل اسم الدرس:',data.lesson);
    if(newLesson===null||newLesson.trim()===data.lesson)return;
    if(!newLesson.trim()){toast('❌ الاسم فارغ',true);return;}
    const{error}=await sb.from('curriculum').update({lesson:newLesson.trim()}).eq('id',id);
    if(error)throw error;
    clearCurriculumCache();
    toast('✅ تم التعديل');
    loadLessonsForManagement();
  }catch(e){toast('❌ خطأ: '+(e.message||''),true);}
}

async function deleteLesson(id,name){
  if(!isAdmin())return;
  if(!confirm(`⚠️ هل تريد حذف الدرس:\n"${name}"؟\n\nلا يمكن التراجع عن هذا الإجراء.`))return;
  try{
    const{error}=await sb.from('curriculum').delete().eq('id',id);
    if(error)throw error;
    clearCurriculumCache();
    toast('✅ تم الحذف');
    loadLessonsForManagement();
  }catch(e){toast('❌ خطأ: '+(e.message||''),true);}
}

// إظهار/إخفاء أزرار المشرف عند تغير الحالة
function updateAdminButtons(){
  const show=isAdmin();
  console.log('[updateAdminButtons] isAdmin=',show,'email=',currentUser?.email);
  
  // إظهار/إخفاء عناصر admin-only
  const adminEls=document.querySelectorAll('.admin-only');
  adminEls.forEach(el=>{
    if(show){el.style.removeProperty('display');}
    else{el.style.display='none';}
  });
  console.log('[updateAdminButtons] admin-only count=',adminEls.length);
  
  // إظهار/إخفاء عناصر teacher-only
  const teacherEls=document.querySelectorAll('.teacher-only');
  teacherEls.forEach(el=>{
    if(show){el.style.display='none';}
    else{el.style.removeProperty('display');}
  });
  console.log('[updateAdminButtons] teacher-only count=',teacherEls.length);
  
  if(show){
    // عرض شارة المشرف الكبيرة في رأس الصفحة
    showAdminBanner();
    // إن كان المشرف على صفحة مخفية، انقله للخطة
    setTimeout(()=>{
      const currentActive=document.querySelector('.nav-btn.active:not([style*="display: none"])');
      if(!currentActive||currentActive.classList.contains('teacher-only')){
        const trackerBtn=document.querySelector('.nav-btn[data-page="tracker"]');
        if(trackerBtn){
          document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
          document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
          document.getElementById('page-tracker').classList.add('active');
          trackerBtn.classList.add('active');
        }
      }
    },50);
    // إخفاء بانر المعلم
    document.querySelectorAll('.teacher-banner').forEach(el=>el.style.display='none');
    // إظهار لوحة المناهج
    const adminContentPanel=document.getElementById('admin-content-panel');
    if(adminContentPanel)adminContentPanel.style.removeProperty('display');
    // تغيير عنوان صفحة الخطة
    const trackerTitle=document.getElementById('tracker-title');
    if(trackerTitle)trackerTitle.textContent='🛠️ لوحة المشرف';
    const trackerPara=document.querySelector('#page-tracker .page-header p');
    if(trackerPara)trackerPara.textContent='إدارة محتوى المناهج وقوالب الدرجات لكل المعلمين';
    // تحميل البيانات
    loadAdminCurriculumSummary();
    loadAdminTemplates();
  }
}

// شارة مرئية تؤكد للمشرف أنه في وضع المشرف
function showAdminBanner(){
  if(document.getElementById('admin-mode-banner'))return;
  const banner=document.createElement('div');
  banner.id='admin-mode-banner';
  banner.style.cssText='position:fixed;top:0;left:0;right:0;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#000;text-align:center;padding:6px 10px;font-size:11.5px;font-weight:800;z-index:200;font-family:Cairo,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.3)';
  banner.innerHTML='👑 وضع المشرف — لديك صلاحيات إدارية كاملة';
  document.body.appendChild(banner);
  document.body.style.paddingTop='28px';
}

// ملخص محتوى المناهج المرفوع (للمشرف)
async function loadAdminCurriculumSummary(){
  const el=document.getElementById('admin-curriculum-summary');
  if(!el)return;

  const semEl=document.getElementById('acs-semester');
  const gradeEl=document.getElementById('acs-grade');
  const semester=semEl?semEl.value:'الفصل الأول';
  const grade=gradeEl?parseInt(gradeEl.value):5;
  const gradeNames={5:'الخامس',6:'السادس',7:'السابع',8:'الثامن',9:'التاسع',10:'العاشر',11:'الحادي عشر',12:'الثاني عشر'};

  el.innerHTML='<div style="text-align:center;padding:14px;color:var(--muted);font-size:12px">⏳ جاري التحميل...</div>';

  try{
    // 1. جلب المواد المسجلة لهذا الصف والفصل
    const{data:subData,error:subErr}=await sb.from('subjects')
      .select('subject,sort').eq('grade',grade).eq('semester',semester).order('sort');
    if(subErr)throw subErr;

    // 2. جلب الدروس لهذا الصف والفصل
    const{data:curData,error:curErr}=await sb.from('curriculum')
      .select('subject,unit').eq('grade',grade).eq('semester',semester);
    if(curErr)throw curErr;

    // تجميع بيانات الدروس حسب المادة
    const lessonMap={};
    (curData||[]).forEach(r=>{
      if(!lessonMap[r.subject])lessonMap[r.subject]={lessons:0,units:new Set()};
      lessonMap[r.subject].lessons++;
      if(r.unit)lessonMap[r.subject].units.add(r.unit);
    });

    if(!subData||!subData.length){
      el.innerHTML=`<div style="text-align:center;padding:14px;color:var(--muted);font-size:12px">📭 لا توجد مواد مسجلة للصف ${gradeNames[grade]} - ${semester}</div>`;
      return;
    }

    let html=`<div style="font-size:12px;color:var(--muted);margin-bottom:10px">الصف ${gradeNames[grade]} · ${semester} · ${subData.length} مادة</div>`;
    html+='<div style="display:flex;flex-direction:column;gap:8px">';

    subData.forEach(s=>{
      const info=lessonMap[s.subject];
      if(info){
        const units=info.units.size;
        const lessons=info.lessons;
        html+=`<div style="background:var(--card);border:1px solid var(--border);border-right:3px solid var(--green);border-radius:10px;padding:10px 13px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px">
          <div style="display:flex;align-items:center;gap:7px">
            <span style="font-size:15px">✅</span>
            <span style="font-size:13px;font-weight:700;color:var(--white)">${escHtml(s.subject)}</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="font-size:11px;color:var(--muted);background:var(--surface);border:1px solid var(--border);border-radius:99px;padding:3px 10px">${units} وحدة · ${lessons} درس</span>
            <button onclick="previewSubjectContent('${s.subject.replace(/'/g,"\'")}',${grade},'${semester}')"
              style="background:linear-gradient(135deg,var(--red),var(--red2));color:#fff;border:none;border-radius:99px;padding:4px 12px;font-size:11px;font-family:'Cairo',sans-serif;font-weight:700;cursor:pointer">
              👁️ معاينة
            </button>
          </div>
        </div>`;
      }else{
        html+=`<div style="background:var(--card);border:1px solid var(--border);border-right:3px solid var(--border);border-radius:10px;padding:10px 13px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;opacity:.7">
          <div style="display:flex;align-items:center;gap:7px">
            <span style="font-size:15px">⏳</span>
            <span style="font-size:13px;font-weight:700;color:var(--muted)">${escHtml(s.subject)}</span>
          </div>
          <span style="font-size:11px;color:var(--muted)">لم ترفع الدروس بعد</span>
        </div>`;
      }
    });

    html+='</div>';
    el.innerHTML=html;
  }catch(e){
    el.innerHTML=`<div style="color:var(--red2);font-size:12px">❌ خطأ: ${e.message||''}</div>`;
  }
}

async function previewSubjectContent(subject,grade,semester){
  try{
    const{data,error}=await sb.from('curriculum')
      .select('unit,lesson,sort').eq('subject',subject).eq('grade',grade).eq('semester',semester).order('sort');
    if(error)throw error;
    if(!data||!data.length){toast('لا توجد دروس',true);return;}

    // تجميع حسب الوحدة
    const units={};
    data.forEach(r=>{
      const u=r.unit||'بدون وحدة';
      if(!units[u])units[u]=[];
      units[u].push(r.lesson);
    });

    let msg=`📚 ${subject} - الصف ${grade} - ${semester}
`;
    msg+=`${'─'.repeat(30)}
`;
    Object.entries(units).forEach(([u,lessons])=>{
      msg+=`
📂 ${u} (${lessons.length} درس)
`;
      lessons.forEach((l,i)=>{msg+=`  ${i+1}. ${l}
`;});
    });
    alert(msg);
  }catch(e){
    toast('❌ خطأ في المعاينة',true);
  }
}

// ════════════════════════════════════════════════════════════════
// 📢 الإعلانات
// ════════════════════════════════════════════════════════════════
function toggleNewAnnForm(){
  const f=document.getElementById('new-ann-form');
  const isHidden=f.style.display==='none';
  f.style.display=isHidden?'block':'none';
  if(isHidden){
    document.getElementById('ann-title-inp').focus();
    document.getElementById('ann-title-inp').value='';
    document.getElementById('ann-body-inp').value='';
  }
}

async function saveAnnouncement(){
  const title=document.getElementById('ann-title-inp').value.trim();
  const body=document.getElementById('ann-body-inp').value.trim();
  if(!title){toast('❌ أدخل عنوان الإعلان',true);return;}
  if(!body){toast('❌ أدخل نص الإعلان',true);return;}
  try{
    const{error}=await sb.from('announcements').insert({
      title,body,
      created_by:currentUser.email,
      created_at:new Date().toISOString()
    });
    if(error)throw error;
    toast('✅ تم نشر الإعلان بنجاح');
    toggleNewAnnForm();
    loadAnnouncements();
    // إرسال Push لجميع المعلمين
    sendPushToAll(title, body);
  }catch(e){
    toast('❌ خطأ في النشر: '+(e.message||''),true);
  }
}

async function deleteAnnouncement(id){
  if(!confirm('هل تريد حذف هذا الإعلان؟'))return;
  try{
    const{error}=await sb.from('announcements').delete().eq('id',id);
    if(error)throw error;
    toast('✅ تم حذف الإعلان');
    loadAnnouncements();
    loadAnnouncementBanner();
  }catch(e){
    toast('❌ خطأ في الحذف',true);
  }
}

async function loadAnnouncements(){
  const list=document.getElementById('announcements-list');
  if(!list)return;
  list.innerHTML='<div style="text-align:center;padding:14px;color:var(--muted);font-size:12px">⏳ جاري التحميل...</div>';
  try{
    const{data,error}=await sb.from('announcements').select('*').order('created_at',{ascending:false});
    if(error)throw error;
    if(!data||!data.length){
      list.innerHTML='<div style="text-align:center;padding:14px;color:var(--muted);font-size:12px">📭 لا توجد إعلانات بعد</div>';
      return;
    }
    list.innerHTML=data.map(a=>{
      const d=new Date(a.created_at);
      const dateStr=d.toLocaleDateString('ar-OM',{year:'numeric',month:'short',day:'numeric'});
      return `<div class="ann-item">
        <div class="ann-item-header">
          <span class="ann-item-title">📢 ${escHtml(a.title)}</span>
          <span class="ann-item-date">${dateStr}</span>
        </div>
        <div class="ann-item-body">${escHtml(a.body)}</div>
        <div class="ann-item-actions">
          <button class="ann-del-btn" onclick="deleteAnnouncement(${a.id})">🗑️ حذف</button>
        </div>
      </div>`;
    }).join('');
  }catch(e){
    list.innerHTML=`<div style="color:var(--red2);font-size:12px">❌ خطأ: ${e.message||''}</div>`;
  }
}

// بانر الإعلانات للمعلمين
// ════════════════════════════════════════════════════════════════
// 🔔 نظام الجرس والإشعارات
// ════════════════════════════════════════════════════════════════
let _bellAnnouncements=[];

function getBellReadIds(){
  try{return JSON.parse(localStorage.getItem('bell_read_ids')||'[]');}
  catch{return[];}
}
function saveBellReadIds(ids){
  localStorage.setItem('bell_read_ids',JSON.stringify(ids));
}

async function loadAnnouncementBanner(){
  try{
    // جلب الإعلانات العامة
    const{data:annData,error:annErr}=await sb.from('announcements')
      .select('*').order('created_at',{ascending:false});
    if(annErr)return;

    // جلب الرسائل الخاصة لهذا المعلم فقط
    let msgData=[];
    if(currentUser){
      const{data:msgs}=await sb.from('private_messages')
        .select('*').eq('to_user_id',currentUser.id).order('created_at',{ascending:false});
      msgData=msgs||[];
    }

    // دمج المصدرين مع تمييز النوع
    const announcements=(annData||[]).map(a=>({...a,_type:'ann'}));
    const messages=msgData.map(m=>({...m,_type:'msg'}));

    // ترتيب حسب التاريخ
    _bellAnnouncements=[...announcements,...messages]
      .sort((a,b)=>new Date(b.created_at)-new Date(a.created_at));

    renderBell();
  }catch(e){}
}

function renderBell(){
  const badge=document.getElementById('bell-badge');
  const list=document.getElementById('bell-drop-list');
  const countEl=document.getElementById('bell-unread-count');
  if(!badge||!list)return;

  const readIds=getBellReadIds();
  // مفتاح القراءة: نوع + id
  const getKey=(a)=>`${a._type}_${a.id}`;
  const unread=_bellAnnouncements.filter(a=>!readIds.includes(getKey(a)));

  // تحديث الشارة
  if(unread.length>0){
    badge.textContent=unread.length>9?'9+':unread.length;
    badge.classList.add('show');
  }else{
    badge.classList.remove('show');
  }

  if(countEl)countEl.textContent=unread.length>0?`${unread.length} غير مقروء`:'كل شيء مقروء';
  // فحص إشعارات جديدة
  checkNewAnnouncements();
  // تحديث عنوان الصفحة
  document.title=unread.length>0?`(${unread.length}) خطتي الفصلية`:'خطتي الفصلية';

  if(!_bellAnnouncements.length){
    list.innerHTML='<div class="bell-drop-empty">📭 لا توجد إشعارات</div>';
    return;
  }

  list.innerHTML=_bellAnnouncements.map(a=>{
    const key=getKey(a);
    const isUnread=!readIds.includes(key);
    const d=new Date(a.created_at);
    const dateStr=d.toLocaleDateString('ar-OM',{month:'short',day:'numeric'});
    const isMsg=a._type==='msg';
    const icon=isMsg?'✉️':'📢';
    const label=isMsg?`<span style="font-size:10px;background:rgba(41,128,185,.2);color:#3498db;border-radius:4px;padding:1px 6px;margin-right:4px">رسالة خاصة</span>`:'';
    return `<div class="bell-drop-item${isUnread?' unread':''}" onclick="markOneReadByKey('${key}')">
      <div class="bell-drop-title">${isUnread?'🔵 ':''}${icon} ${escHtml(a.title)}${label}</div>
      <div class="bell-drop-body">${escHtml(a.body)}</div>
      <div class="bell-drop-date">${dateStr}</div>
    </div>`;
  }).join('');
}

function toggleBellDropdown(e){
  e.stopPropagation();
  const dd=document.getElementById('bell-dropdown');
  if(!dd)return;
  dd.classList.toggle('show');
}

// إغلاق عند الضغط خارج القائمة
document.addEventListener('click',function(e){
  const wrap=document.getElementById('bell-wrap');
  if(wrap&&!wrap.contains(e.target)){
    const dd=document.getElementById('bell-dropdown');
    if(dd)dd.classList.remove('show');
  }
});

function markOneRead(id){
  // للتوافق مع الكود القديم
  markOneReadByKey(String(id));
}

function markOneReadByKey(key){
  const readIds=getBellReadIds();
  if(!readIds.includes(key)){
    readIds.push(key);
    saveBellReadIds(readIds);
    renderBell();
  }
}

function markAllRead(e){
  e.stopPropagation();
  const keys=_bellAnnouncements.map(a=>`${a._type}_${a.id}`);
  saveBellReadIds(keys);
  renderBell();
  const dd=document.getElementById('bell-dropdown');
  if(dd)dd.classList.remove('show');
}

// ════════════════════════════════════════════════════════════════
// 🔔 تحديث الجرس تلقائياً كل دقيقة
// ════════════════════════════════════════════════════════════════
let _bellPollInterval=null;

function startBellPolling(){
  // إظهار زر المساعدة عند أي تسجيل دخول
  const helpBtn=document.getElementById('help-btn');
  if(helpBtn)helpBtn.style.display='block';
  // تحميل فوري
  loadAnnouncementBanner();
  // ثم كل 15 ثانية
  if(_bellPollInterval)clearInterval(_bellPollInterval);
  _bellPollInterval=setInterval(()=>{
    loadAnnouncementBanner();
  },15000);
}

function stopBellPolling(){
  if(_bellPollInterval){clearInterval(_bellPollInterval);_bellPollInterval=null;}
}

// ════════════════════════════════════════════════════════════════
// 👥 إدارة المستخدمين
// ════════════════════════════════════════════════════════════════
let _allUsers=[];

async function loadAdminUsers(){
  const list=document.getElementById('users-list');
  const countEl=document.getElementById('users-count');
  if(!list)return;
  list.innerHTML='<div style="text-align:center;padding:14px;color:var(--muted);font-size:12px">⏳ جاري التحميل...</div>';
  try{
    // جلب جميع الملفات الشخصية مع البريد
    // جلب البيانات من profiles
    const queryResult=await sb.from('profiles').select('id,data,updated_at').order('updated_at',{ascending:false});
    if(queryResult.error)throw queryResult.error;

    // جلب قائمة المحظورين بالـ id
    const{data:bannedData}=await sb.from('banned_users').select('user_id');
    const bannedSet=new Set((bannedData||[]).map(r=>r.user_id));

    _allUsers=queryResult.data||[];
    _allUsers=_allUsers.map(u=>{
      const d=u.data||{};
      return{
        ...u,
        _email: d.email||'',
        _name: d.display_name||d.teacher_name||d.full_name||(d.email?d.email.split('@')[0]:'—'),
        _avatar: d.avatar_url||d.photo||'',
        _config: typeof d.teacher_config==='object'&&d.teacher_config!==null?d.teacher_config:{},
        _enabled: !bannedSet.has(u.id)
      };
    });
    console.log('[loadAdminUsers] عدد المستخدمين:', _allUsers.length, _allUsers);
    if(countEl)countEl.textContent=`${_allUsers.length} معلم مسجل`;
    renderUsersList(_allUsers);
  }catch(e){
    console.error('[loadAdminUsers] خطأ:', e);
    list.innerHTML=`<div style="color:var(--red2);font-size:12px">❌ خطأ: ${e.message||''}</div>`;
  }
}

function getLastSeenText(updated_at){
  if(!updated_at)return{text:'غير معروف',recent:false};
  const now=new Date();
  const last=new Date(updated_at);
  const diffMs=now-last;
  const diffMins=Math.floor(diffMs/60000);
  const diffHours=Math.floor(diffMins/60);
  const diffDays=Math.floor(diffHours/24);
  if(diffMins<60)return{text:`منذ ${diffMins} دقيقة`,recent:true};
  if(diffHours<24)return{text:`منذ ${diffHours} ساعة`,recent:true};
  if(diffDays===1)return{text:'أمس',recent:false};
  if(diffDays<7)return{text:`منذ ${diffDays} أيام`,recent:false};
  return{text:last.toLocaleDateString('ar-OM',{month:'short',day:'numeric'}),recent:false};
}

function renderUsersList(users){
  const list=document.getElementById('users-list');
  if(!list)return;
  if(!users.length){
    list.innerHTML='<div style="text-align:center;padding:14px;color:var(--muted);font-size:12px">لا توجد نتائج</div>';
    return;
  }
  list.innerHTML=users.map((u,idx)=>{
    const name=u._name||'—';
    const email=u._email||'';
    const config=u._config||{};
    const gradesRaw=config.grades;
    const grades=Array.isArray(gradesRaw)?gradesRaw.join('، '):(gradesRaw?String(gradesRaw):'—');
    const subject=typeof config.subject==='string'?config.subject:'—';
    const lastSeen=getLastSeenText(typeof u.updated_at==='string'?u.updated_at:null);
    const avatar=u._avatar||'';
    const avatarEl=avatar
      ?`<img class="user-avatar" src="${escHtml(avatar)}" onerror="this.parentElement.innerHTML='<div class=\"user-avatar-placeholder\">👤</div>'">`
      :`<div class="user-avatar-placeholder">👤</div>`;
    const isAdminUser=email===ADMIN_EMAIL;
    const enabled=u._enabled!==false;
    const disabledBadge=!enabled&&!isAdminUser?'<span class="user-disabled-badge">⛔ موقوف</span>':'';
    return `<div class="user-item" style="${!enabled&&!isAdminUser?'opacity:.7':''}">
      ${avatarEl}
      <div class="user-info" style="flex:1;min-width:0">
        <div class="user-name">${idx+1}. ${escHtml(name)}${isAdminUser?' 👑':''}${disabledBadge}</div>
        ${email?`<div class="user-email">${escHtml(email)}</div>`:'<div class="user-email" style="color:var(--muted);font-style:italic">بريد غير متاح</div>'}
        <div class="user-meta">📚 ${escHtml(subject)} · صف ${escHtml(grades)}</div>
        <div class="user-last-seen${lastSeen.recent?' recent':''}">🕐 آخر نشاط: ${lastSeen.text}</div>
      </div>
      ${!isAdminUser?`
        <div style="display:flex;flex-direction:column;gap:5px;flex-shrink:0">
          <button class="user-msg-btn" onclick="openMsgModal('${escHtml(u.id)}','${escHtml(name)}','${escHtml(email)}')">✉️ رسالة</button>
          ${enabled
            ?`<button class="user-disable-btn" onclick="toggleUserAccess('${escHtml(u.id)}','${escHtml(name)}',false)">⛔ تعطيل</button>`
            :`<button class="user-enable-btn" onclick="toggleUserAccess('${escHtml(u.id)}','${escHtml(name)}',true)">✅ تفعيل</button>`
          }
        </div>
      `:''}
    </div>`;
  }).join('');
}

// ════════════════════════════════════════
// 🔐 تفعيل / تعطيل الحساب
// ════════════════════════════════════════
async function toggleUserAccess(userId, name, enable){
  const action = enable ? 'تفعيل' : 'تعطيل';
  if(!confirm(`هل تريد ${action} حساب "${name}"؟`)) return;
  try{
    if(enable){
      // رفع الحظر - حذف من banned_users
      const{error}=await sb.from('banned_users').delete().eq('user_id',userId);
      if(error)throw error;
      toast(`✅ تم تفعيل حساب ${name}`);
    }else{
      // الحظر - إضافة لـ banned_users
      const{error}=await sb.from('banned_users').insert({user_id:userId,name:name,banned_at:new Date().toISOString()});
      if(error&&error.code!=='23505')throw error;
      toast(`⛔ تم تعطيل حساب ${name}`);
    }
    await loadAdminUsers();
  }catch(e){
    toast('❌ خطأ: '+(e.message||''),true);
  }
}

// ════════════════════════════════════════
// ✉️ الرسائل الخاصة
// ════════════════════════════════════════
let _msgTarget={id:'',name:'',email:''};

function openMsgModal(id,name,email){
  _msgTarget={id,name,email};
  document.getElementById('msg-modal-to').textContent=`إلى: ${name}${email?' ('+email+')':''}`;
  document.getElementById('msg-modal-title-inp').value='';
  document.getElementById('msg-modal-body-inp').value='';
  document.getElementById('msg-modal').style.display='flex';
  setTimeout(()=>document.getElementById('msg-modal-title-inp').focus(),150);
}

function closeMsgModal(e){
  if(e&&e.target!==document.getElementById('msg-modal'))return;
  document.getElementById('msg-modal').style.display='none';
}

async function sendPrivateMsg(){
  const title=document.getElementById('msg-modal-title-inp').value.trim();
  const body=document.getElementById('msg-modal-body-inp').value.trim();
  if(!title){toast('❌ أدخل عنوان الرسالة',true);return;}
  if(!body){toast('❌ أدخل نص الرسالة',true);return;}
  const btn=document.querySelector('.msg-modal-send');
  btn.disabled=true;btn.textContent='⏳ جاري الإرسال...';
  try{
    const{error}=await sb.from('private_messages').insert({
      to_user_id:_msgTarget.id,
      to_name:_msgTarget.name,
      to_email:_msgTarget.email,
      from_email:currentUser.email,
      title,body,
      created_at:new Date().toISOString(),
      is_read:false
    });
    if(error)throw error;
    toast(`✅ تم إرسال الرسالة إلى ${_msgTarget.name}`);
    document.getElementById('msg-modal').style.display='none';
    // إرسال Push للمعلم المحدد
    sendPushToUser(_msgTarget.id, title, body);
  }catch(e){
    toast('❌ خطأ في الإرسال: '+(e.message||''),true);
  }finally{
    btn.disabled=false;btn.textContent='📨 إرسال';
  }
}

function filterUsers(){
  const q=(document.getElementById('users-search').value||'').toLowerCase();
  if(!q){renderUsersList(_allUsers);return;}
  const filtered=_allUsers.filter(u=>{
    const name=(u._name||'').toLowerCase();
    const email=(u._email||'').toLowerCase();
    const subject=((u._config||{}).subject||'').toLowerCase();
    return name.includes(q)||email.includes(q)||subject.includes(q);
  });
  renderUsersList(filtered);
}

// ════════════════════════════════════════════════════════════════
// 🎯 إدارة قوالب الدرجات (للمشرف)
// ════════════════════════════════════════════════════════════════
let _editingTemplateId=null;

async function loadAdminTemplates(){
  const panel=document.getElementById('admin-templates-panel');
  const list=document.getElementById('admin-templates-list');
  if(!panel||!list)return;
  panel.style.display='block';
  list.innerHTML='<div class="template-empty-state">⏳ جاري التحميل...</div>';
  try{
    const{data,error}=await sb.from('grade_templates').select('*').order('subject').order('grade');
    if(error)throw error;
    if(!data||!data.length){
      list.innerHTML='<div class="template-empty-state">📭 لا توجد قوالب بعد. اضغط "إنشاء قالب جديد" للبدء.</div>';
      return;
    }
    let html='';
    data.forEach(t=>{
      const cols=Array.isArray(t.grade_types)?t.grade_types:[];
      const colsHtml=cols.length
        ? cols.map(c=>`<div>• ${escHtml(c.name||'بدون اسم')} (${c.max||0} درجة)</div>`).join('')
        : '<div style="color:var(--muted)">لا توجد أعمدة</div>';
      html+=`<div class="template-card">
        <div class="template-card-header">
          <div class="template-card-title">📘 ${escHtml(t.subject)}</div>
          <div class="template-card-grade">الصف ${t.grade}</div>
        </div>
        <div class="template-card-body">${colsHtml}</div>
        <div class="template-card-actions">
          <button class="tc-edit-btn" onclick="editTemplate(${t.id})">✏️ تعديل</button>
          <button class="tc-del-btn" onclick="deleteTemplate(${t.id},'${escAttr(t.subject)}',${t.grade})">🗑️ حذف</button>
        </div>
      </div>`;
    });
    list.innerHTML=html;
  }catch(e){
    list.innerHTML=`<div class="template-empty-state">❌ خطأ: ${e.message||'غير معروف'}</div>`;
  }
}

// متغيرات حالة المحرر
let _selectedGrades=new Set();
let _selectedSubject='';
let _subjectsCache=null;

function openNewTemplateModal(){
  if(!isAdmin())return;
  _editingTemplateId=null;
  _selectedGrades=new Set();
  _selectedSubject='';
  document.getElementById('te-title').textContent='➕ قالب درجات جديد';
  // ابني chips الصفوف
  renderGradeChips();
  // إخفاء حقل المواد والأعمدة حتى يختار صفوفاً
  document.getElementById('te-subjects-field').style.display='none';
  document.getElementById('te-cols-field').style.display='none';
  document.getElementById('te-subject-custom').value='';
  document.getElementById('te-cols-list').innerHTML='';
  document.getElementById('template-editor-modal').style.display='flex';
}

function renderGradeChips(){
  const container=document.getElementById('te-grades-chips');
  const grades=[
    {n:5,name:'الخامس'},{n:6,name:'السادس'},{n:7,name:'السابع'},{n:8,name:'الثامن'},
    {n:9,name:'التاسع'},{n:10,name:'العاشر'},{n:11,name:'الحادي عشر'},{n:12,name:'الثاني عشر'}
  ];
  container.innerHTML=grades.map(g=>
    `<button class="te-chip${_selectedGrades.has(g.n)?' selected':''}" onclick="toggleGradeChip(${g.n})">الصف ${g.name}</button>`
  ).join('');
}

async function toggleGradeChip(n){
  if(_selectedGrades.has(n))_selectedGrades.delete(n);
  else _selectedGrades.add(n);
  renderGradeChips();
  // عند اختيار صف واحد على الأقل، نعرض المواد
  updateSaveBtn();
  if(_selectedGrades.size>0){
    document.getElementById('te-subjects-field').style.display='block';
    await loadSubjectsForGrades();
  }else{
    document.getElementById('te-subjects-field').style.display='none';
    document.getElementById('te-cols-field').style.display='none';
  }
}

async function loadSubjectsForGrades(){
  const container=document.getElementById('te-subjects-chips');
  container.innerHTML='<div class="te-empty-state">⏳ جاري التحميل...</div>';
  try{
    const gradesArr=[..._selectedGrades];
    // اجلب كل المواد للصفوف المختارة
    const{data,error}=await sb.from('subjects').select('subject,grade').in('grade',gradesArr);
    if(error)throw error;
    // وحّد المواد (subject مكرّر لو موجود في عدة صفوف)
    const subjectsSet=new Set();
    (data||[]).forEach(r=>subjectsSet.add(r.subject));
    const subjects=[...subjectsSet].sort();
    if(!subjects.length){
      container.innerHTML='<div class="te-empty-state">📭 لا توجد مواد مسجّلة لهذه الصفوف. اكتب الاسم يدوياً ↓</div>';
      // أظهر مع ذلك حقل الأعمدة ليكتب يدوياً
      showColsField();
      return;
    }
    container.innerHTML=subjects.map(s=>
      `<button class="te-chip te-chip-subject${_selectedSubject===s?' selected':''}" onclick="selectSubjectChip('${escAttr(s)}')">${escHtml(s)}</button>`
    ).join('');
    // إن كان هناك مادة مختارة سابقاً وموجودة في القائمة، نظهر الأعمدة
    if(_selectedSubject&&subjects.includes(_selectedSubject))showColsField();
  }catch(e){
    container.innerHTML=`<div class="te-empty-state">❌ ${e.message||''}</div>`;
  }
}

function selectSubjectChip(name){
  _selectedSubject=name;
  document.getElementById('te-subject-custom').value='';
  // حدّث الـ chips ليظهر المختار
  document.querySelectorAll('#te-subjects-chips .te-chip').forEach(c=>{
    c.classList.toggle('selected',c.textContent.trim()===name);
  });
  showColsField();
}

// مستمع لحقل المادة اليدوي
document.addEventListener('input',e=>{
  if(e.target&&e.target.id==='te-subject-custom'){
    const val=e.target.value.trim();
    if(val){
      _selectedSubject=val;
      // إلغاء تحديد المادة من chips
      document.querySelectorAll('#te-subjects-chips .te-chip').forEach(c=>c.classList.remove('selected'));
      showColsField();
    }
  }
});

function showColsField(){
  document.getElementById('te-cols-field').style.display='block';
  // أضف أعمدة افتراضية إن لم تكن موجودة
  const list=document.getElementById('te-cols-list');
  if(!list.children.length){
    addTemplateCol({name:'واجبات',max:10});
    addTemplateCol({name:'اختبارات قصيرة',max:20});
    addTemplateCol({name:'اختبار نهائي',max:70});
  }
}

async function editTemplate(id){
  if(!isAdmin())return;
  try{
    const{data,error}=await sb.from('grade_templates').select('*').eq('id',id).single();
    if(error||!data){toast('❌ القالب غير موجود',true);return;}
    _editingTemplateId=id;
    _selectedGrades=new Set([data.grade]);
    _selectedSubject=data.subject||'';
    document.getElementById('te-title').textContent='✏️ تعديل القالب';
    renderGradeChips();
    document.getElementById('te-subjects-field').style.display='block';
    await loadSubjectsForGrades();
    document.getElementById('te-subject-custom').value='';
    document.getElementById('te-cols-list').innerHTML='';
    const cols=Array.isArray(data.grade_types)?data.grade_types:[];
    if(cols.length){cols.forEach(c=>addTemplateCol(c));}
    else{addTemplateCol();}
    document.getElementById('te-cols-field').style.display='block';
    document.getElementById('template-editor-modal').style.display='flex';
  }catch(e){toast('❌ خطأ: '+(e.message||''),true);}
}

function closeTemplateEditor(){
  document.getElementById('template-editor-modal').style.display='none';
  _editingTemplateId=null;
  _selectedGrades=new Set();
  _selectedSubject='';
}

function addTemplateCol(col){
  col=col||{name:'',max:10};
  const list=document.getElementById('te-cols-list');
  const row=document.createElement('div');
  row.className='te-col-row';
  row.innerHTML=`
    <input type="text" placeholder="اسم التقييم" value="${escAttr(col.name||'')}" data-fld="name"/>
    <input type="number" placeholder="الدرجة" value="${col.max||10}" min="1" max="100" data-fld="max"/>
    <button class="te-col-remove" onclick="this.closest('.te-col-row').remove()">✕</button>
  `;
  list.appendChild(row);
  // إضافة event listener لتحديث الزر عند التغيير
  row.querySelectorAll('input').forEach(inp=>inp.addEventListener('input',updateSaveBtn));
  row.querySelector('.te-col-remove').addEventListener('click',()=>setTimeout(updateSaveBtn,50));
  updateSaveBtn();
}

function updateSaveBtn(){
  const cols=document.querySelectorAll('#te-cols-list .te-col-row');
  const hasGrade=_selectedGrades.size>0;
  const hasSubject=!!(_selectedSubject||(document.getElementById('te-subject-custom')?.value?.trim()));
  const hasCols=cols.length>0;
  const btn=document.getElementById('te-save-btn');
  if(btn)btn.disabled=!(hasGrade&&hasSubject&&hasCols);
}

async function saveTemplateFromEditor(){
  if(!isAdmin()){toast('❌ غير مصرح',true);return;}
  
  // 1) الصفوف المختارة
  const grades=[..._selectedGrades];
  if(!grades.length){toast('❌ اختر صفاً واحداً على الأقل',true);return;}
  
  // 2) المادة (chip أو يدوي)
  const customSubject=document.getElementById('te-subject-custom').value.trim();
  const subject=customSubject||_selectedSubject;
  if(!subject){toast('❌ اختر المادة أو اكتبها يدوياً',true);return;}
  
  // 3) أعمدة التقييم
  const rows=document.querySelectorAll('#te-cols-list .te-col-row');
  const cols=[];
  rows.forEach(r=>{
    const name=r.querySelector('[data-fld="name"]').value.trim();
    const max=parseInt(r.querySelector('[data-fld="max"]').value)||10;
    if(name)cols.push({name,max});
  });
  if(!cols.length){toast('❌ أضف نوع تقييم واحد على الأقل',true);return;}
  
  try{
    if(_editingTemplateId){
      // تحرير قالب واحد فقط
      const{error}=await sb.from('grade_templates')
        .update({subject,grade:grades[0],grade_types:cols})
        .eq('id',_editingTemplateId);
      if(error)throw error;
      toast('✅ تم التحديث');
    }else{
      // إنشاء قالب لكل صف من الصفوف المختارة
      let created=0,replaced=0;
      for(const g of grades){
        const existing=await sb.from('grade_templates').select('id')
          .eq('subject',subject).eq('grade',g);
        if(existing.data&&existing.data.length){
          // قالب موجود → استبدل بصمت
          await sb.from('grade_templates')
            .update({grade_types:cols}).eq('id',existing.data[0].id);
          replaced++;
        }else{
          await sb.from('grade_templates').insert([{
            subject,grade:g,grade_types:cols,created_by:currentUser?.email||''
          }]);
          created++;
        }
      }
      let msg=`✅ تم: ${created} قالب جديد`;
      if(replaced>0)msg+=`، ${replaced} مُحدّث`;
      toast(msg);
    }
    closeTemplateEditor();
    loadAdminTemplates();
  }catch(e){toast('❌ خطأ: '+(e.message||''),true);}
}

async function deleteTemplate(id,subject,grade){
  if(!isAdmin())return;
  if(!confirm(`⚠️ حذف قالب ${subject} - الصف ${grade}؟\nلا يمكن التراجع.`))return;
  try{
    const{error}=await sb.from('grade_templates').delete().eq('id',id);
    if(error)throw error;
    toast('✅ تم الحذف');
    loadAdminTemplates();
  }catch(e){toast('❌ خطأ: '+(e.message||''),true);}
}

// إعادة جلب الدروس من قاعدة البيانات وتحديث teacher_config
async function refreshLessonsFromDB(){
  if(!teacherConfig||!teacherConfig.grades||!teacherConfig.grades.length){
    toast('❌ لا يوجد إعداد محفوظ',true);
    return;
  }
  if(!sb){toast('❌ لا يوجد اتصال بقاعدة البيانات',true);return;}
  
  toast('🔄 جاري تحديث الدروس...');
  clearCurriculumCache(); // مسح cache لضمان جلب آخر البيانات
  
  try{
    const semester=teacherConfig.semester||'الفصل الأول';
    let totalLessons=0;
    let updatedGrades=0;
    let issues=[];
    
    for(const grade of teacherConfig.grades){
      // جلب الدروس من جدول curriculum
      const{data,error}=await sb.from('curriculum')
        .select('*')
        .eq('semester',semester)
        .eq('subject',grade.subject)
        .eq('grade',grade.num)
        .order('sort');
      
      if(error){
        issues.push(`خطأ في جلب ${grade.subject} - الصف ${grade.num}: ${error.message}`);
        continue;
      }
      
      if(!data||!data.length){
        issues.push(`⚠️ لا توجد دروس لـ ${grade.subject} - الصف ${grade.num} في ${semester}`);
        continue;
      }
      
      // إعادة بناء الوحدات
      grade.units=buildUnitsFromRows(data,semester,grade.subject);
      totalLessons+=data.length;
      updatedGrades++;
    }
    
    // حفظ التحديثات
    await dbSave({teacher_config:teacherConfig});
    
    // إعادة بناء الواجهة
    buildTracker();
    applyFilter();
    update();
    
    if(issues.length){
      alert(`تم التحديث:\n✅ ${updatedGrades} مادة-صف تم تحديثها\n📚 ${totalLessons} درس إجمالاً\n\nملاحظات:\n${issues.join('\n')}`);
    }else{
      toast(`✅ تم تحديث ${totalLessons} درس بنجاح`,'ok');
    }
  }catch(e){
    console.error('خطأ في التحديث:',e);
    toast('❌ فشل التحديث: '+e.message,true);
  }
}

function buildTracker(){
  if(!teacherConfig||!teacherConfig.grades){document.getElementById('sections').innerHTML='';return;}
  buildGradeFilterBar();
  if(currentTrackerIdx==null||currentTrackerIdx>=teacherConfig.grades.length)currentTrackerIdx=0;
  const grade=teacherConfig.grades[currentTrackerIdx]||teacherConfig.grades[0];
  if(!grade){document.getElementById('sections').innerHTML='';return;}
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  document.getElementById('tracker-title').textContent=`${grade.subject||teacherConfig.subject||'الخطة'} — الصف ${arabicNums[(grade.num||1)-1]}`;
  const sectionsEl=document.getElementById('sections');sectionsEl.innerHTML='';
  if(!grade.units||!grade.units.length){
    sectionsEl.innerHTML=`<div style="text-align:center;padding:50px 24px;color:var(--muted)"><div style="font-size:52px;margin-bottom:14px">📚</div><div style="font-size:16px;font-weight:700;color:var(--gold);margin-bottom:8px">محتوى هذه المادة قيد الإعداد</div><div style="font-size:13px;line-height:1.7">سيتم رفع دروس "${grade.subject||''}" قريباً.<br/>ستظهر تلقائياً هنا فور توفّرها — بدون أي إعداد إضافي منك.</div></div>`;
    return;
  }
  grade.units.forEach((unit,ui)=>{
    const secEl=document.createElement('div');secEl.className='section collapsed';secEl.id='sec-u'+ui;
    const doneCount=unit.lessons.filter(l=>get(l.id).done).length;
    const pct=unit.lessons.length?Math.round(doneCount/unit.lessons.length*100):0;
    secEl.innerHTML=`<div class="sec-head" style="cursor:pointer" onclick="toggleUnit('sec-u${ui}')"><div class="sec-icon" style="background:rgba(192,57,43,.12)">📚</div><div style="flex:1"><div class="sec-title">${unit.name}</div><div class="sec-sub" id="prg-u${ui}">${doneCount}/${unit.lessons.length} دروس</div></div><div class="sec-bar-wrap"><div class="sec-bar" id="bar-u${ui}" style="width:${pct}%"></div></div><div class="unit-arrow">▼</div></div>`;
    const lEl=document.createElement('div');lEl.className='lessons';
    // تخزين بيانات الوحدة للبناء الكسول عند الفتح
    secEl._unitData={unit,grade,ui};
    secEl._lessonsEl=lEl;
    secEl._built=false;
    secEl.appendChild(lEl);sectionsEl.appendChild(secEl);
  });
}

function toggleUnit(secId){
  const sec=document.getElementById(secId);
  if(!sec)return;
  const wasCollapsed=sec.classList.contains('collapsed');
  sec.classList.toggle('collapsed');
  // بناء كسول: ابنِ الدروس فقط عند أول فتح
  if(wasCollapsed&&!sec._built&&sec._unitData){
    const {unit,grade}=sec._unitData;
    const lEl=sec._lessonsEl;
    unit.lessons.forEach(lesson=>{
      const s=get(lesson.id);if(!s.classes)s.classes={};
      const card=document.createElement('div');card.className='lesson'+(s.done?' done':'');card.dataset.id=lesson.id;
      const chips=grade.classes.map(cls=>{const checked=s.classes[cls.id];const col=cls.color;const style=checked?`border-color:${col};background:${hexToRgba(col,.12)};`:'';const chipCheckStyle=checked?`background:${col};border-color:${col};color:#fff;`:'';return`<div class="class-chip ${checked?'checked':''}" data-class="${cls.id}" style="${style}"><div class="chip-check" style="${chipCheckStyle}">✓</div><span class="chip-label" style="color:${col}">${cls.name}</span></div>`;}).join('');
      const lf=lessonFiles[lesson.id]||[];
      const filesHtml=lf.map(f=>`<div class="lesson-file-item"><span>${f.type&&f.type.startsWith('image/')?'🖼️':'📄'}</span><span class="lfi-name">${f.name}</span><span class="lfi-size">${fmtSize(f.size)}</span><button class="arc-btn" style="padding:3px 8px;font-size:10px;" onclick="${f.type&&f.type.startsWith('image/')?`viewImg('${f.path}')`:`openPdf('${f.path}','${f.name.replace(/'/g,"\\'")}')`}">👁️</button><button class="arc-btn del" style="padding:3px 8px;font-size:10px;" onclick="deleteLessonFile('${lesson.id}','${f.id}','${f.path}')">🗑️</button></div>`).join('');
      card.innerHTML=`<div class="lesson-top"><div class="chk">✓</div><div class="lesson-info"><div class="lesson-name">${lesson.name}</div><div class="lesson-unit">${unit.name}</div></div></div><div class="classes-row" onclick="event.stopPropagation()"><span class="classes-label">🏫 الشعب:</span>${chips}</div><div class="notes-row" onclick="event.stopPropagation()"><span class="notes-icon">📝</span><textarea class="notes-input" rows="1" placeholder="ملاحظاتك هنا..." data-f="notes">${s.notes||''}</textarea></div><div class="notes-row" onclick="event.stopPropagation()"><span class="notes-icon">🎬</span><input class="notes-input" type="url" inputmode="url" placeholder="رابط شرح الدرس (يوتيوب...)" data-f="videoUrl" value="${(s.videoUrl||'').replace(/"/g,'&quot;')}"/><button class="arc-btn" style="padding:5px 10px;font-size:11px;flex-shrink:0" onclick="openVideoLink('${lesson.id}')">▶️ فتح</button></div><div class="lesson-files-row" onclick="event.stopPropagation()"><div class="lesson-files-label">📎 ملفات الدرس:<label class="lesson-upload-btn" style="margin-right:auto"><input type="file" accept="application/pdf,image/*" onchange="uploadLessonFile(event,'${lesson.id}')"/>➕ إرفاق</label></div><div class="lesson-files-list" id="lfl-${lesson.id}">${filesHtml}</div></div>`;
      card.querySelector('.lesson-top').addEventListener('click',()=>{const cur=get(lesson.id);cur.done=!cur.done;state[lesson.id]=cur;card.classList.toggle('done',cur.done);toast(cur.done?'✅ درس منجز':'↩️ إلغاء',cur.done?'ok':false);applyFilter();update();scheduleSave();});
      card.querySelectorAll('.class-chip').forEach(chip=>{chip.addEventListener('click',()=>{const cls=chip.dataset.class;const cur=get(lesson.id);if(!cur.classes)cur.classes={};cur.classes[cls]=!cur.classes[cls];state[lesson.id]=cur;const col=classConfig[cls]?.color||'var(--gold)';chip.classList.toggle('checked',cur.classes[cls]);if(cur.classes[cls]){chip.style.borderColor=col;chip.style.background=hexToRgba(col,.12);chip.querySelector('.chip-check').style.cssText=`background:${col};border-color:${col};color:#fff;`;}else{chip.style.borderColor='';chip.style.background='';chip.querySelector('.chip-check').style.cssText='';}const g=teacherConfig?.grades?.[currentTrackerIdx]||teacherConfig?.grades?.[0];if(g){const allChecked=g.classes.every(c=>cur.classes[c.id]);if(allChecked&&!cur.done){cur.done=true;state[lesson.id]=cur;card.classList.add('done');toast('✅ كل الشعب خلصت — درس منجز','ok');applyFilter();update();}}scheduleSave();});});
      card.querySelectorAll('[data-f]').forEach(inp=>{inp.addEventListener('change',()=>{const cur=get(lesson.id);cur[inp.dataset.f]=inp.value;state[lesson.id]=cur;scheduleSave();});if(inp.tagName==='TEXTAREA'){inp.addEventListener('input',()=>{inp.style.height='auto';inp.style.height=inp.scrollHeight+'px';});setTimeout(()=>{inp.style.height='auto';inp.style.height=inp.scrollHeight+'px';},0);}});
      lEl.appendChild(card);
    });
    sec._built=true;
  }
}

function openVideoLink(lessonId){
  const card=document.querySelector(`.lesson[data-id="${lessonId}"]`);
  const inp=card?card.querySelector('[data-f="videoUrl"]'):null;
  let url=((inp?inp.value:'')||get(lessonId).videoUrl||'').trim();
  if(!url){toast('❌ لا يوجد رابط — الصقه أولاً',true);return;}
  // احفظ القيمة الحالية قبل الفتح
  const cur=get(lessonId);cur.videoUrl=inp?inp.value.trim():url;state[lessonId]=cur;scheduleSave();
  if(!/^https?:\/\//i.test(url))url='https://'+url;
  window.open(url,'_blank','noopener');
}

async function uploadLessonFile(e,lessonId){
  const file=e.target.files[0];e.target.value='';if(!file)return;
  if(file.size>MAX_FILE_SIZE){toast('❌ الحد الأقصى 500 ميجا',true);return;}
  const fileName=`[درس-${lessonId}] ${file.name}`;
  toast('⬆️ جاري الرفع على Drive...');
  const result=await driveUpload(file,fileName);
  if(!result){toast('❌ فشل الرفع',true);return;}
  if(!lessonFiles[lessonId])lessonFiles[lessonId]=[];
  lessonFiles[lessonId].push({id:Date.now().toString(),name:file.name,size:file.size,type:file.type,driveId:result.id,viewLink:result.viewLink,downloadLink:result.downloadLink,previewLink:result.previewLink});
  refreshLessonFiles(lessonId);
  toast('✅ تم الرفع على Drive','ok');scheduleSave();
}
function refreshLessonFiles(lessonId){
  const container=document.getElementById('lfl-'+lessonId);if(!container)return;
  const lf=lessonFiles[lessonId]||[];
  container.innerHTML=lf.map(f=>{
    const isImg=f.type&&f.type.startsWith('image/');
    const openUrl=f.previewLink||f.viewLink||'';
    return`<div class="lesson-file-item"><span>${isImg?'🖼️':'📄'}</span><span class="lfi-name">${f.name}</span><span class="lfi-size">${fmtSize(f.size)}</span><button class="arc-btn" style="padding:3px 8px;font-size:10px;" onclick="openDriveFile('${openUrl}','${f.name.replace(/'/g,"\\'")}')">👁️</button><button class="arc-btn del" style="padding:3px 8px;font-size:10px;" onclick="deleteLessonFile('${lessonId}','${f.id}','${f.driveId||''}')">🗑️</button></div>`;
  }).join('');
}

async function deleteLessonFile(lessonId,fileId,driveId){
  if(!confirm('تأكيد حذف الملف؟'))return;
  if(driveId)await driveDelete(driveId);
  lessonFiles[lessonId]=(lessonFiles[lessonId]||[]).filter(f=>f.id!==fileId);
  refreshLessonFiles(lessonId);
  toast('🗑️ تم الحذف');scheduleSave();
}

let currentFilter='all';
function setFilter(f,btn){currentFilter=f;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');applyFilter();}
function applyFilter(){
  let vis=0;
  document.querySelectorAll('.lesson').forEach(card=>{const done=get(card.dataset.id).done;let show=true;if(currentFilter==='done'&&!done)show=false;if(currentFilter==='remain'&&done)show=false;card.classList.toggle('hidden',!show);if(show)vis++;});
  document.querySelectorAll('#page-tracker .section').forEach(sec=>{
    // إذا لم تُبنَ الدروس بعد، أبقِ الوحدة ظاهرة دائماً
    if(!sec._built){sec.style.display='';return;}
    const sv=sec.querySelectorAll('.lesson:not(.hidden)').length;
    sec.style.display=sv?'':'none';
  });
  const emptyEl=document.getElementById('empty');
  // اعتبر الوحدات غير المبنية كأن لها دروس
  const unbuiltCount=document.querySelectorAll('#page-tracker .section:not([data-built])').length;
  if(vis===0&&unbuiltCount===0){emptyEl.style.display='block';if(currentFilter==='done'){document.getElementById('empty-emoji').textContent='📚';document.getElementById('empty-msg').textContent='ما خلصت أي درس بعد!';}else if(currentFilter==='remain'){document.getElementById('empty-emoji').textContent='🏆';document.getElementById('empty-msg').textContent='خلصت كل الدروس 🎉';}else{document.getElementById('empty-emoji').textContent='📋';document.getElementById('empty-msg').textContent='لا توجد دروس';}}
  else{emptyEl.style.display='none';}
}
function update(){
  const all=allLessons(),total=all.length,done=all.filter(l=>get(l.id).done).length,pct=total?Math.round(done/total*100):0;
  const C=2*Math.PI*42;
  document.getElementById('arc').style.strokeDashoffset=C-(pct/100)*C;
  document.getElementById('pct').textContent=pct+'%';
  document.getElementById('done-n').textContent=done;document.getElementById('left-n').textContent=total-done;document.getElementById('total-n').textContent=total;
  const msgs=['ابدأ أول درس 🚀','بداية رائعة! 💪','نص الطريق 🔥','شارف على الإنجاز ⚡','قريب جداً 🎯','أتممت الفصل 🏆'];
  document.getElementById('motiv').textContent=msgs[pct===0?0:pct<25?1:pct<50?2:pct<75?3:pct<100?4:5];
  if(teacherConfig&&teacherConfig.grades){
    const grade=teacherConfig.grades[currentTrackerIdx]||teacherConfig.grades[0];
    if(grade){grade.units.forEach((unit,ui)=>{const ls=unit.lessons,sd=ls.filter(l=>get(l.id).done).length,sp=ls.length?Math.round(sd/ls.length*100):0;const pg=document.getElementById('prg-u'+ui);if(pg)pg.textContent=sd+'/'+ls.length+' دروس';const br=document.getElementById('bar-u'+ui);if(br)br.style.width=sp+'%';});}
  }
}

// ══ ARCHIVE ════════════════════════════════════════════
let activeCat=null,pendingFile=null,currentInnerCat=null,currentArchiveGrade=null;
// مفتاح الأرشيف مركّب من الصف + المجلد، فيصير لكل صف أرشيفه المستقل
function arcKey(catId){return 'g'+(currentArchiveGrade!=null?currentArchiveGrade:'_')+'__'+catId;}
function getArchiveGrades(){
  if(teacherConfig&&teacherConfig.grades&&teacherConfig.grades.length)return teacherConfig.grades.map(g=>g.num);
  return [];
}
function buildGradeSelect(){
  const grid=document.getElementById('arc-gs-grid');if(!grid)return;
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  if(!teacherConfig||!teacherConfig.grades||!teacherConfig.grades.length){
    grid.innerHTML='<div style="color:var(--muted);font-size:13px;text-align:center;grid-column:1/-1">لا توجد صفوف. أكمل الإعداد أولاً.</div>';
    return;
  }
  grid.innerHTML=teacherConfig.grades.map(g=>{
    // عدّ إجمالي الملفات المؤرشفة لهذا الصف
    let fileCount=0;
    arcCategories.forEach(cat=>{fileCount+=(arcMeta['g'+g.num+'__'+cat.id]||[]).length;});
    const clsNames=g.classes.map(c=>c.name).join('، ');
    return `<div class="arc-gs-card" onclick="enterArchiveGrade(${g.num})">
      <div class="arc-gs-icon">📚</div>
      <div class="arc-gs-name">الصف ${arabicNums[g.num-1]||g.num}</div>
      <div class="arc-gs-meta">${clsNames||'—'}</div>
      <div class="arc-gs-meta" style="margin-top:8px;color:var(--gold)">🗂️ ${fileCount} ملف مؤرشف</div>
    </div>`;
  }).join('');
}
function enterArchiveGrade(n){
  currentArchiveGrade=n;
  const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];
  document.getElementById('arc-grade-banner').textContent='📚 الصف '+(arabicNums[n-1]||n);
  document.getElementById('arc-grade-select').style.display='none';
  document.getElementById('arc-inner').classList.remove('active');
  document.getElementById('arc-main').classList.remove('hidden');
  buildArchiveGrid();
}
function backToGradeSelect(){
  currentArchiveGrade=null;
  document.getElementById('arc-main').classList.add('hidden');
  document.getElementById('arc-inner').classList.remove('active');
  document.getElementById('arc-grade-select').style.display='block';
  buildGradeSelect();
}
function buildArchiveGrid(){
  const grid=document.getElementById('arc-grid');grid.innerHTML='';
  document.getElementById('arc-folders-count').textContent=arcCategories.length+' مجلد';
  arcCategories.forEach(cat=>{
    const items=(arcMeta[arcKey(cat.id)]||[]).length;const div=document.createElement('div');div.className='arc-folder';
    div.innerHTML=`<button class="arc-folder-del" onclick="event.stopPropagation();deleteCat('${cat.id}')">✕</button><div class="arc-folder-icon">${cat.icon}</div><div class="arc-folder-name">${cat.title}</div><div class="arc-folder-count">${items} ملف</div>`;
    div.addEventListener('click',()=>openArcInner(cat.id));grid.appendChild(div);
  });
}
async function loadArchive(){
  // ابدأ دائماً من شاشة اختيار الصف
  currentArchiveGrade=null;
  document.getElementById('arc-main').classList.add('hidden');
  document.getElementById('arc-inner').classList.remove('active');
  document.getElementById('arc-grade-select').style.display='block';
  buildGradeSelect();
  // احسب مجموع أحجام مرفقات التطبيق المرفوعة على Drive
  let totalBytes=0,fileCount=0;
  Object.values(lessonFiles||{}).forEach(arr=>{
    (arr||[]).forEach(f=>{totalBytes+=(f.size||0);fileCount++;});
  });
  const FREE_QUOTA=15*1024*1024*1024; // 15GB سعة Google المجانية
  const pct=Math.min(100,(totalBytes/FREE_QUOTA)*100);
  const pctTxt=pct<0.1?'< 0.1':pct.toFixed(1);
  document.getElementById('stor-fill').style.width=Math.max(pct,1)+'%';
  document.getElementById('stor-pct').textContent=`${fmtSize(totalBytes)} من 15GB · ${fileCount} ملف`;
  const badge=document.getElementById('drive-badge');if(badge){badge.style.display='inline-flex';badge.textContent='✅ Drive';}
}
function openArcInner(catId){currentInnerCat=catId;const cat=arcCategories.find(c=>c.id===catId);const arabicNums=['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢'];const gLabel=currentArchiveGrade!=null?` — الصف ${arabicNums[currentArchiveGrade-1]||currentArchiveGrade}`:'';document.getElementById('inner-icon').textContent=cat.icon;document.getElementById('inner-title').textContent=cat.title+gLabel;document.getElementById('arc-main').classList.add('hidden');document.getElementById('arc-inner').classList.add('active');renderInnerItems(catId);}
function closeArcInner(){currentInnerCat=null;document.getElementById('arc-main').classList.remove('hidden');document.getElementById('arc-inner').classList.remove('active');}
function renderInnerItems(catId){
  const c=document.getElementById('arc-inner-items');const items=arcMeta[arcKey(catId)]||[];c.innerHTML='';
  document.getElementById('inner-count').textContent=items.length+' ملف';
  if(!items.length){c.innerHTML='<div class="arc-empty">لا يوجد ملفات 📭</div>';return;}
  items.forEach(item=>{
    const el=document.createElement('div');el.className='arc-item';const isImg=item.type&&item.type.startsWith('image/');
    const ds=item.date?new Date(item.date).toLocaleDateString('ar-SA',{year:'numeric',month:'short',day:'numeric'}):'';
    const openAction=isImg?`viewImg('${item.previewLink||item.viewLink}')`:`openDriveFile('${item.previewLink||item.viewLink}','${(item.name||'').replace(/'/g,"\\'")}'  )`;
    el.innerHTML=`<div class="arc-item-top"><span class="arc-item-icon">${isImg?'🖼️':'📄'}</span><div class="arc-item-body"><div class="arc-item-name">${item.name}</div><div class="arc-item-meta">${ds?`<span>📅 ${ds}</span>`:''}<span>${fmtSize(item.size)}</span></div>${item.note?`<div class="arc-item-note">${item.note}</div>`:''}</div></div><div class="arc-item-actions"><button class="arc-btn" onclick="${openAction}">👁️ فتح</button><button class="arc-btn" onclick="downloadDriveFile('${item.downloadLink}','${(item.name||'').replace(/'/g,"\\'")}')">⬇️ تحميل</button><button class="arc-btn del" onclick="deleteArcItem('${catId}','${item.id}','${item.driveId||''}')">🗑️ حذف</button></div>`;
    c.appendChild(el);
  });
}

function resolveLocalUrl(url){
  // الروابط الآن روابط Google Drive حقيقية — تُمرّر كما هي
  return url||'';
}
function openDriveFile(url,name){
  const real=resolveLocalUrl(url);
  if(!real){toast('❌ الملف غير متاح',true);return;}
  document.getElementById('pdf-title').textContent=name;
  document.getElementById('pdf-frame').src=real;
  document.getElementById('pdf-modal').classList.remove('hidden');
}
function downloadDriveFile(url,name){
  const real=resolveLocalUrl(url);
  if(!real){toast('❌ الملف غير متاح',true);return;}
  const a=document.createElement('a');a.href=real;a.download=name||'file';a.click();
}
function handleInnerFile(e){const f=e.target.files[0];if(f)processFile(f,currentInnerCat);e.target.value='';}
function processFile(file,catId){
  if(file.size>MAX_FILE_SIZE){toast('❌ الحد الأقصى 500 ميجا',true);return;}
  pendingFile={file,name:file.name.replace(/\.[^/.]+$/,''),size:file.size};activeCat=catId;
  const cat=arcCategories.find(c=>c.id===catId);
  document.getElementById('modal-title').textContent=(file.type.startsWith('image/')?'🖼️':'📄')+' '+cat.title;
  document.getElementById('modal-file-info').innerHTML='📎 '+file.name+' <span style="color:var(--gold)">('+fmtSize(file.size)+')</span>';
  document.getElementById('m-name').value='';document.getElementById('m-date').value=new Date().toISOString().split('T')[0];document.getElementById('m-note').value='';
  document.getElementById('modal-save-btn').disabled=false;document.getElementById('modal-bg').classList.remove('hidden');
}
function closeModal(){document.getElementById('modal-bg').classList.add('hidden');activeCat=null;pendingFile=null;}
async function saveItem(){
  if(!pendingFile||!activeCat)return;const btn=document.getElementById('modal-save-btn');btn.disabled=true;btn.textContent='جاري الرفع...';
  const name=document.getElementById('m-name').value.trim()||pendingFile.name;
  const ext=pendingFile.file.name.split('.').pop();
  const fileName=`[خطتي-${activeCat}] ${name}.${ext}`;
  const prog=document.getElementById('inner-prog');const fill=document.getElementById('inner-pf');
  if(prog){prog.style.display='block';fill.style.width='40%';}
  const driveResult=await driveUpload(pendingFile.file,fileName);
  if(prog){fill.style.width='100%';setTimeout(()=>{prog.style.display='none';fill.style.width='0%';},600);}
  if(!driveResult){toast('❌ فشل الرفع',true);btn.disabled=false;btn.textContent='رفع 💾';return;}
  const aKey=arcKey(activeCat);
  if(!arcMeta[aKey])arcMeta[aKey]=[];
  arcMeta[aKey].push({
    id:Date.now().toString(),name,
    date:document.getElementById('m-date').value,
    note:document.getElementById('m-note').value.trim(),
    size:pendingFile.size,
    type:pendingFile.file.type,
    driveId:driveResult.id,
    viewLink:driveResult.viewLink,
    downloadLink:driveResult.downloadLink,
    previewLink:driveResult.previewLink,
  });
  renderInnerItems(activeCat);buildArchiveGrid();closeModal();toast('✅ تم الحفظ','ok');btn.textContent='رفع 💾';scheduleSave();
}
async function deleteArcItem(catId,itemId,driveId){
  if(!confirm('تأكيد الحذف؟'))return;
  if(driveId)await driveDelete(driveId);
  const aKey=arcKey(catId);
  arcMeta[aKey]=(arcMeta[aKey]||[]).filter(i=>i.id!==itemId);
  renderInnerItems(catId);buildArchiveGrid();toast('🗑️ تم الحذف');scheduleSave();
}
async function deleteCat(catId){
  if(!confirm('حذف هذا المجلد وكل محتوياته من جميع الصفوف؟'))return;
  // المجلد تعريف مشترك، فنحذف ملفاته من كل الصفوف
  const gNums=getArchiveGrades();
  for(const n of gNums){
    const k='g'+n+'__'+catId;
    const items=arcMeta[k]||[];
    for(const item of items)if(item.driveId)await driveDelete(item.driveId);
    delete arcMeta[k];
  }
  delete arcMeta[catId]; // تنظيف أي بيانات قديمة بالمفتاح المجرّد
  arcCategories=arcCategories.filter(c=>c.id!==catId);
  buildArchiveGrid();toast('🗑️ تم حذف المجلد');scheduleSave();
}
const ICONS=['📝','📋','❓','🎯','📚','📁','📂','🗂️','📌','📎','🖊️','📊','📈','🏫','✏️','🔖','🗒️','📓'];
let selectedIcon='📁';
function openAddCatModal(){document.getElementById('cat-name-inp').value='';selectedIcon='📁';const picker=document.getElementById('icon-picker');picker.innerHTML=ICONS.map(ic=>`<button onclick="selectIcon('${ic}',this)" style="font-size:22px;background:var(--card);border:2px solid ${ic===selectedIcon?'var(--gold)':'var(--border)'};border-radius:8px;padding:5px 8px;cursor:pointer;transition:border-color .2s;">${ic}</button>`).join('');document.getElementById('cat-modal-bg').classList.remove('hidden');}
function selectIcon(ic,btn){selectedIcon=ic;document.querySelectorAll('#icon-picker button').forEach(b=>b.style.borderColor='var(--border)');btn.style.borderColor='var(--gold)';}
function closeCatModal(){document.getElementById('cat-modal-bg').classList.add('hidden');}
function addCategory(){const name=document.getElementById('cat-name-inp').value.trim();if(!name){document.getElementById('cat-name-inp').focus();return;}const id='cat_'+Date.now();arcCategories.push({id,title:name,icon:selectedIcon});buildArchiveGrid();closeCatModal();toast('✅ تم إضافة المجلد','ok');scheduleSave();}

// ══ GRADES ══════════════════════════════════════════════
function getAllClasses(){
  if(!teacherConfig||!teacherConfig.grades)return[];
  return teacherConfig.grades.flatMap(g=>g.classes.map(cls=>({...cls,gradeNum:g.num,gradeName:`الصف ${g.num}`})));
}
function renderGrades(){
  const allCls=getAllClasses();const tabs=document.getElementById('grades-class-tabs');
  tabs.innerHTML=allCls.map(cls=>`<button class="gc-tab ${activeGradesClass===cls.id?'active':''}" onclick="setGradesClass('${cls.id}')">${cls.name} <span style="font-size:10px;opacity:.7">(${cls.gradeName})</span></button>`).join('');
  if(!allCls.length){document.getElementById('grades-empty').style.display='block';document.getElementById('grades-content').style.display='none';return;}
  if(!activeGradesClass||!allCls.find(c=>c.id===activeGradesClass))activeGradesClass=allCls[0].id;
  updateGradeAdminButtons();
  renderGradesTable();
  // محاولة تحميل قالب تلقائياً إذا كانت الشعبة فارغة
  autoLoadTemplateIfEmpty();
}
function setGradesClass(k){
  activeGradesClass=k;
  renderGrades();
}
function renderGradesTable(){
  const k=activeGradesClass;if(!k)return;
  const allCls=getAllClasses();const cls=allCls.find(c=>c.id===k);if(!cls)return;
  const sList=getUnifiedStudents(k);const cols=gradeTypes.filter(c=>c.classKey===k);
  const wrap=document.getElementById('grades-content');const empty=document.getElementById('grades-empty');
  if(!sList.length&&!cols.length){return;}
  empty.style.display='none';wrap.style.display='block';
  const totalMax=cols.reduce((a,c)=>a+Number(c.max),0);
  let sumPts=0,countSt=0;
  sList.forEach(st=>{const sg=(grades[k]||{})[st.id]||{};let pts=0;cols.forEach(c=>{if(sg[c.id]!=null&&!isNaN(sg[c.id]))pts+=Number(sg[c.id]);});if(totalMax>0){sumPts+=pts;countSt++;}});
  const classAvg=countSt&&totalMax?Math.round(sumPts/countSt):0;
  document.getElementById('grades-summary').innerHTML=`<div class="gs-stat"><div class="gs-stat-num">${sList.length}</div><div class="gs-stat-lbl">طالب</div></div><div class="gs-stat"><div class="gs-stat-num">${cols.length}</div><div class="gs-stat-lbl">تقييم</div></div><div class="gs-stat"><div class="gs-stat-num">${classAvg} / ${totalMax}</div><div class="gs-stat-lbl">متوسط الصف</div></div>`;
  const t=document.getElementById('grades-table');
  const canEditCols=isAdmin();
  // بناء الرأس
  let head='<thead><tr><th style="min-width:40px;text-align:center">م</th><th>الطالب</th>';
  cols.forEach(c=>{const delBtn=canEditCols?`<button class="gch-act-btn" onclick="delGradeCol('${c.id}')">✕</button>`:'';head+=`<th><div class="grade-col-head"><div class="gch-actions">${delBtn}</div><div class="gch-name">${c.name}</div><div class="gch-max">/${c.max}</div></div></th>`;});
  head+=`<th>المجموع / ${totalMax}</th></tr></thead>`;
  // بناء الجسم — بناء options مرة واحدة لكل عمود ثم إعادة استخدامها
  const colOptions={};
  cols.forEach(c=>{
    let opts='<option value="">—</option>';
    for(let i=0;i<=Math.floor(c.max);i++)opts+=`<option value="${i}">${i}</option>`;
    colOptions[c.id]={opts,max:Number(c.max)};
  });
  let body='<tbody>';
  sList.forEach((st,idx)=>{
    const sg=(grades[k]||{})[st.id]||{};
    body+=`<tr><td style="text-align:center;color:var(--muted);font-weight:700;width:36px">${idx+1}</td><td style="white-space:nowrap"><button class="student-del-btn" onclick="delStudent('${st.id}')">✕</button>${st.name}</td>`;
    let pts=0;
    cols.forEach(c=>{
      const v=sg[c.id];const num=v!=null&&!isNaN(v)?Number(v):null;let cl='';
      if(num!=null){const pct2=(num/c.max)*100;cl=pct2<50?'low':pct2<75?'mid':'high';pts+=num;}
      // استبدال selected في الـ options المبنية مسبقاً بدل بنائها من جديد
      let opts=colOptions[c.id].opts;
      if(num!=null)opts=opts.replace(`<option value="${num}">${num}</option>`,`<option value="${num}" selected>${num}</option>`);
      body+=`<td><select class="grade-input ${cl}" onchange="updGrade('${st.id}','${c.id}',this.value)">${opts}</select></td>`;
    });
    const totalVal=pts>0||cols.some(c=>(sg[c.id]!=null&&sg[c.id]!==''))?pts:null;
    const tColor=totalVal==null?'var(--muted)':totalMax>0&&(totalVal/totalMax)<0.5?'#e74c3c':totalMax>0&&(totalVal/totalMax)<0.75?'#f0c060':'#27ae60';
    body+=`<td style="font-weight:800;color:${tColor}">${totalVal!=null?totalVal+' / '+totalMax:'—'}</td></tr>`;
  });
  body+='</tbody>';
  t.style.opacity='0';
  t.innerHTML=head+body;
  requestAnimationFrame(()=>{ t.style.transition='opacity .2s'; t.style.opacity='1'; });
}
// تحميل lazy لمكتبات Excel (توفير ~2MB من التحميل الأولي)
let _excelLibsLoading=null;
function loadExcelLibs(){
  if(typeof ExcelJS!=='undefined'&&typeof saveAs!=='undefined')return Promise.resolve();
  if(_excelLibsLoading)return _excelLibsLoading;
  _excelLibsLoading=new Promise((resolve,reject)=>{
    let loaded=0;const total=2;
    function check(){if(++loaded===total)resolve();}
    function fail(name){reject(new Error('فشل تحميل '+name));}
    if(typeof ExcelJS==='undefined'){
      const s1=document.createElement('script');
      s1.src='https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js';
      s1.onload=check;s1.onerror=()=>fail('ExcelJS');
      document.head.appendChild(s1);
    }else check();
    if(typeof saveAs==='undefined'){
      const s2=document.createElement('script');
      s2.src='https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js';
      s2.onload=check;s2.onerror=()=>fail('FileSaver');
      document.head.appendChild(s2);
    }else check();
  });
  return _excelLibsLoading;
}
async function exportGradesExcel(){
  const k=activeGradesClass;if(!k)return;
  toast('⏳ جاري تحميل مكتبة Excel...');
  try{await loadExcelLibs();}
  catch(e){toast('❌ فشل تحميل مكتبة Excel - تحقق من الإنترنت',true);return;}
  
  const allCls=getAllClasses();const cls=allCls.find(c=>c.id===k);
  const sList=getUnifiedStudents(k);const cols=gradeTypes.filter(c=>c.classKey===k);
  if(!sList.length){toast('❌ لا يوجد طلاب',true);return;}
  
  const totalMax=cols.reduce((a,c)=>a+Number(c.max),0);
  const clsName=(cls?cls.name:'الشعبة').replace(/[:\\\/\?\*\[\]]/g,'-');
  
  // معلومات إضافية
  const info=getCurrentClassInfo();
  const subjectName=info?info.subject:'';
  const gradeName=info?`الصف ${info.grade}`:'';
  
  // ألوان الوزارة
  const COLOR_GREEN='FF006C35';    // أخضر علم عمان
  const COLOR_RED='FFC41E3A';      // أحمر علم عمان  
  const COLOR_GOLD='FFD4AF37';     // ذهبي للتأكيد
  const COLOR_LIGHT_GREEN='FFE8F5E9'; // أخضر فاتح للصفوف
  const COLOR_FAIL='FFFFEBEE';     // أحمر فاتح للراسبين
  const COLOR_WHITE='FFFFFFFF';
  const COLOR_DARK='FF1A1A1A';
  
  // إنشاء ملف Excel جديد
  const workbook=new ExcelJS.Workbook();
  workbook.creator='خطتي الفصلية';
  workbook.created=new Date();
  
  const ws=workbook.addWorksheet(clsName,{
    views:[{state:'frozen',ySplit:4,xSplit:2,rightToLeft:true}],
    pageSetup:{paperSize:9,orientation:'landscape',fitToPage:true}
  });
  
  // ═══ الصف 1: عنوان المدرسة/النظام ═══
  ws.mergeCells(1,1,1,3+cols.length);
  const titleCell=ws.getCell(1,1);
  titleCell.value='سلطنة عُمان — وزارة التربية والتعليم';
  titleCell.font={name:'Cairo',size:16,bold:true,color:{argb:COLOR_WHITE}};
  titleCell.alignment={horizontal:'center',vertical:'middle'};
  titleCell.fill={type:'pattern',pattern:'solid',fgColor:{argb:COLOR_GREEN}};
  ws.getRow(1).height=32;
  
  // ═══ الصف 2: معلومات الشعبة ═══
  ws.mergeCells(2,1,2,3+cols.length);
  const subtitleCell=ws.getCell(2,1);
  subtitleCell.value=`📋 سجل درجات ${subjectName} — ${gradeName} — ${cls?cls.name:''}`;
  subtitleCell.font={name:'Cairo',size:12,bold:true,color:{argb:COLOR_DARK}};
  subtitleCell.alignment={horizontal:'center',vertical:'middle'};
  subtitleCell.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFF5F5DC'}};
  ws.getRow(2).height=24;
  
  // ═══ الصف 3: تاريخ التصدير ═══
  ws.mergeCells(3,1,3,3+cols.length);
  const dateCell=ws.getCell(3,1);
  const today=new Date().toLocaleDateString('ar-OM',{year:'numeric',month:'long',day:'numeric'});
  dateCell.value=`📅 تاريخ التصدير: ${today}  •  عدد الطلاب: ${sList.length}  •  عدد التقييمات: ${cols.length}`;
  dateCell.font={name:'Cairo',size:10,italic:true,color:{argb:'FF555555'}};
  dateCell.alignment={horizontal:'center',vertical:'middle'};
  ws.getRow(3).height=20;
  
  // ═══ الصف 4: رؤوس الأعمدة ═══
  const headerRow=ws.getRow(4);
  headerRow.values=['م','اسم الطالب',...cols.map(c=>`${c.name}\n(/${c.max})`),`المجموع\n/ ${totalMax}`];
  headerRow.height=42;
  headerRow.eachCell((cell,colNumber)=>{
    cell.font={name:'Cairo',size:11,bold:true,color:{argb:COLOR_WHITE}};
    cell.alignment={horizontal:'center',vertical:'middle',wrapText:true};
    cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:COLOR_GREEN}};
    cell.border={
      top:{style:'medium',color:{argb:COLOR_DARK}},
      bottom:{style:'medium',color:{argb:COLOR_DARK}},
      left:{style:'thin',color:{argb:COLOR_DARK}},
      right:{style:'thin',color:{argb:COLOR_DARK}}
    };
  });
  
  // ═══ صفوف الطلاب ═══
  const colLetter=n=>{let s='';while(n>0){s=String.fromCharCode(65+(n-1)%26)+s;n=Math.floor((n-1)/26);}return s;};
  const dataStartRow=5;
  const colStart=3;
  const colEnd=colStart+cols.length-1;
  const totalCol=colEnd+1;
  
  sList.forEach((st,idx)=>{
    const rowNum=dataStartRow+idx;
    const sg=(grades[k]||{})[st.id]||{};
    const row=ws.getRow(rowNum);
    
    // أرقام الطلاب
    row.getCell(1).value=idx+1;
    row.getCell(1).font={name:'Cairo',size:11,bold:true,color:{argb:COLOR_GREEN}};
    row.getCell(1).alignment={horizontal:'center',vertical:'middle'};
    
    // اسم الطالب
    row.getCell(2).value=st.name;
    row.getCell(2).font={name:'Cairo',size:11,bold:true};
    row.getCell(2).alignment={horizontal:'right',vertical:'middle',indent:1};
    
    // الدرجات
    cols.forEach((c,ci)=>{
      const cellIdx=colStart+ci;
      const v=sg[c.id];
      const num=(v!=null&&!isNaN(v))?Number(v):null;
      const cell=row.getCell(cellIdx);
      cell.value=num;
      cell.alignment={horizontal:'center',vertical:'middle'};
      cell.font={name:'Cairo',size:11};
      
      // تلوين الدرجات الراسبة فقط (أقل من 50%)
      if(num!=null&&c.max>0&&(num/c.max)<0.5){
        cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:COLOR_FAIL}};
        cell.font={name:'Cairo',size:11,bold:true,color:{argb:COLOR_RED}};
      }
    });
    
    // المجموع التلقائي (صيغة SUM)
    const sumCell=row.getCell(totalCol);
    sumCell.value={formula:`SUM(${colLetter(colStart)}${rowNum}:${colLetter(colEnd)}${rowNum})`};
    sumCell.alignment={horizontal:'center',vertical:'middle'};
    sumCell.font={name:'Cairo',size:11,bold:true,color:{argb:COLOR_GREEN}};
    sumCell.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFF0F8F2'}};
    sumCell.numFmt='0.##';
    
    // خلفية متناوبة للصفوف
    if(idx%2===1){
      for(let c=1;c<=totalCol;c++){
        const cell=row.getCell(c);
        if(!cell.fill||!cell.fill.fgColor||cell.fill.fgColor.argb!==COLOR_FAIL){
          cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:COLOR_LIGHT_GREEN}};
        }
      }
      // إعادة تطبيق ألوان المجموع
      sumCell.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFE0F2E5'}};
    }
    
    // الحواف لجميع الخلايا
    for(let c=1;c<=totalCol;c++){
      row.getCell(c).border={
        top:{style:'thin',color:{argb:'FFCCCCCC'}},
        bottom:{style:'thin',color:{argb:'FFCCCCCC'}},
        left:{style:'thin',color:{argb:'FFCCCCCC'}},
        right:{style:'thin',color:{argb:'FFCCCCCC'}}
      };
    }
    
    row.height=26;
  });
  
  // ═══ صف الإحصائيات في النهاية ═══
  const statsRow=dataStartRow+sList.length;
  const statsRowObj=ws.getRow(statsRow);
  ws.mergeCells(statsRow,1,statsRow,2);
  statsRowObj.getCell(1).value='📊 متوسط الفصل';
  
  cols.forEach((c,ci)=>{
    const cellIdx=colStart+ci;
    const colL=colLetter(cellIdx);
    statsRowObj.getCell(cellIdx).value={formula:`IFERROR(ROUND(AVERAGE(${colL}${dataStartRow}:${colL}${dataStartRow+sList.length-1}),2),0)`};
  });
  // متوسط المجموع
  const totalColL=colLetter(totalCol);
  statsRowObj.getCell(totalCol).value={formula:`IFERROR(ROUND(AVERAGE(${totalColL}${dataStartRow}:${totalColL}${dataStartRow+sList.length-1}),2),0)`};
  
  // تنسيق صف الإحصائيات
  for(let c=1;c<=totalCol;c++){
    const cell=statsRowObj.getCell(c);
    cell.fill={type:'pattern',pattern:'solid',fgColor:{argb:COLOR_GOLD}};
    cell.font={name:'Cairo',size:11,bold:true,color:{argb:COLOR_DARK}};
    cell.alignment={horizontal:'center',vertical:'middle'};
    cell.border={
      top:{style:'medium',color:{argb:COLOR_DARK}},
      bottom:{style:'medium',color:{argb:COLOR_DARK}},
      left:{style:'thin',color:{argb:COLOR_DARK}},
      right:{style:'thin',color:{argb:COLOR_DARK}}
    };
  }
  statsRowObj.height=28;
  
  // ═══ صف التذييل ═══
  const footerRow=statsRow+2;
  ws.mergeCells(footerRow,1,footerRow,totalCol);
  const footerCell=ws.getCell(footerRow,1);
  footerCell.value='✦ تم إعداد هذا السجل من خلال منصة "خطتي الفصلية" ✦';
  footerCell.font={name:'Cairo',size:9,italic:true,color:{argb:COLOR_GREEN}};
  footerCell.alignment={horizontal:'center',vertical:'middle'};
  
  // ═══ عرض الأعمدة ═══
  ws.getColumn(1).width=6;   // م
  ws.getColumn(2).width=28;  // اسم الطالب
  cols.forEach((c,ci)=>{ws.getColumn(colStart+ci).width=16;});
  ws.getColumn(totalCol).width=18; // المجموع
  
  // ═══ حفظ الملف ═══
  try{
    const buffer=await workbook.xlsx.writeBuffer();
    const blob=new Blob([buffer],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
    const fileName=`درجات_${subjectName?subjectName+'_':''}${gradeName?gradeName+'_':''}${clsName}.xlsx`;
    saveAs(blob,fileName);
    toast('📊 تم تصدير الملف بنجاح','ok');
  }catch(e){
    console.error('Excel export error:',e);
    toast('❌ فشل التصدير: '+e.message,true);
  }
}
function updGrade(studentId,colId,val){const k=activeGradesClass;if(!grades[k])grades[k]={};if(!grades[k][studentId])grades[k][studentId]={};if(val==''||val==null){delete grades[k][studentId][colId];}else{grades[k][studentId][colId]=parseFloat(val);}renderGradesTable();scheduleSave();}
function delStudent(id){const k=activeGradesClass;if(!confirm('حذف الطالب وكل درجاته؟'))return;students[k]=(students[k]||[]).filter(s=>s.id!==id);if(grades[k])delete grades[k][id];renderGradesTable();toast('🗑️ تم الحذف');scheduleSave();}
function delGradeCol(id){if(!confirm('حذف هذا التقييم؟'))return;gradeTypes=gradeTypes.filter(c=>c.id!==id);Object.keys(grades).forEach(ck=>{Object.keys(grades[ck]).forEach(sid=>{if(grades[ck][sid][id]!=null)delete grades[ck][sid][id];});});renderGradesTable();toast('🗑️ تم الحذف');scheduleSave();}
function openImportStudents(){if(!activeGradesClass){toast('❌ اختر شعبة أولاً',true);return;}const allCls=getAllClasses();const cls=allCls.find(c=>c.id===activeGradesClass);document.getElementById('import-class-lbl').textContent='الشعبة: '+(cls?cls.name:'');document.getElementById('import-textarea').value='';document.getElementById('import-modal-bg').classList.remove('hidden');}
function closeImportStudents(){document.getElementById('import-modal-bg').classList.add('hidden');}
function importStudents(){const txt=document.getElementById('import-textarea').value;const lines=txt.split('\n').map(l=>l.trim()).filter(l=>l);if(!lines.length){toast('❌ لا يوجد أسماء',true);return;}const k=activeGradesClass;if(!students[k])students[k]=[];const existing=new Set(students[k].map(s=>s.name));const added=lines.filter(n=>!existing.has(n));added.forEach(name=>{students[k].push({id:'s_'+Date.now()+'_'+Math.random().toString(36).slice(2,7),name});});closeImportStudents();renderGradesTable();toast(`✅ تم إضافة ${added.length} طالب`+(lines.length-added.length>0?` (${lines.length-added.length} مكرر تم تجاهله)`:''),'ok');scheduleSave();}

async function importStudentsExcel(event){
  const file=event.target.files[0];
  if(!file)return;
  event.target.value='';
  toast('⏳ جاري قراءة الملف...');
  if(!window.XLSX){
    const s=document.createElement('script');
    s.src='https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
    document.head.appendChild(s);
    await new Promise(r=>s.onload=r);
  }
  const reader=new FileReader();
  reader.onload=e=>{
    try{
      const wb=XLSX.read(e.target.result,{type:'binary'});
      const ws=wb.Sheets[wb.SheetNames[0]];
      const rows=XLSX.utils.sheet_to_json(ws,{header:1});
      if(!rows.length){toast('❌ الملف فارغ',true);return;}

      // البحث عن عمود الاسم في أول 20 صف
      const nameKW=['اسم الطالب','الاسم','اسم','student','name','طالب','أسماء'];
      let nameCol=-1;
      let headerRow=0;
      for(let ri=0;ri<Math.min(20,rows.length);ri++){
        const row=rows[ri];
        row.forEach((cell,ci)=>{
          const v=String(cell||'').trim().replace(/ـ/g,'').toLowerCase();
          if(nameCol<0&&nameKW.some(kw=>v.includes(kw))){nameCol=ci;headerRow=ri;}
        });
        if(nameCol>=0)break;
      }

      // إذا لم يجد عمود الاسم → ابحث بالبيانات
      if(nameCol<0){
        const vn={};
        rows.slice(0,20).forEach(r=>{
          r.forEach((cell,i)=>{
            const v=String(cell||'').trim();
            if(/[؀-ۿ]/.test(v)&&v.length>2&&!/^\d+$/.test(v))vn[i]=(vn[i]||0)+1;
          });
        });
        const best=Object.entries(vn).sort((a,b)=>b[1]-a[1])[0];
        if(best)nameCol=+best[0];
        headerRow=0;
      }

      if(nameCol<0){toast('❌ لم يتم التعرف على عمود الاسم',true);return;}

      const names=rows.slice(headerRow+1)
        .map(r=>String(r[nameCol]||'').trim())
        .filter(n=>n&&n.length>1&&!/^\d+$/.test(n)&&!nameKW.some(kw=>n.toLowerCase().replace(/ـ/g,'').includes(kw)));

      if(!names.length){toast('❌ لم يتم العثور على أسماء',true);return;}

      // إضافة للقائمة مع تجنب التكرار
      const k=activeGradesClass;
      if(!students[k])students[k]=[];
      const existing=new Set(students[k].map(s=>s.name));
      const added=names.filter(n=>!existing.has(n));
      added.forEach(name=>{
        students[k].push({id:'s_'+Date.now()+'_'+Math.random().toString(36).slice(2,7),name});
      });
      closeImportStudents();
      renderGradesTable();
      toast(`✅ تم إضافة ${added.length} طالب من Excel`+(names.length-added.length>0?` (${names.length-added.length} مكرر)`:''),'ok');
      scheduleSave();
    }catch(err){
      toast('❌ خطأ في قراءة الملف: '+err.message,true);
    }
  };
  reader.readAsBinaryString(file);
}
function openAddGradeCol(){if(!activeGradesClass){toast('❌ اختر شعبة أولاً',true);return;}document.getElementById('gc-name').value='';document.getElementById('gc-max').value=10;document.getElementById('gc-cat').value='homework';document.getElementById('gradecol-modal-bg').classList.remove('hidden');}
function closeGradeCol(){document.getElementById('gradecol-modal-bg').classList.add('hidden');}
function addGradeCol(){const name=document.getElementById('gc-name').value.trim();if(!name){document.getElementById('gc-name').focus();return;}const max=parseFloat(document.getElementById('gc-max').value)||10;const cat=document.getElementById('gc-cat').value;gradeTypes.push({id:'g_'+Date.now(),name,category:cat,max,classKey:activeGradesClass});closeGradeCol();renderGradesTable();toast('✅ تم الإضافة','ok');scheduleSave();}

// ══ GRADE TEMPLATES (قوالب الدرجات المشتركة) ══════════
function getCurrentClassInfo(){
  if(!activeGradesClass||!teacherConfig)return null;
  for(const g of (teacherConfig.grades||[])){
    const cls=(g.classes||[]).find(c=>c.id===activeGradesClass);
    if(cls)return{subject:g.subject,grade:g.num,classKey:activeGradesClass,className:cls.name};
  }
  return null;
}

// إظهار/إخفاء أزرار المشرف حسب الصلاحية
function updateGradeAdminButtons(){
  const admin=isAdmin();
  const saveBtn=document.getElementById('save-template-btn');
  const addBtn=document.getElementById('add-gradecol-btn');
  if(saveBtn)saveBtn.style.display=admin?'inline-flex':'none';
  if(addBtn)addBtn.style.display=admin?'inline-flex':'none';
  // تحديث أزرار رفع المحتوى وإدارة الدروس
  if(typeof updateAdminButtons==='function')updateAdminButtons();
  // فحص الشعب الناقصة — مرتين للتأكد بعد تحميل البيانات
  setTimeout(()=>checkIncompleteSetup(),1500);
  setTimeout(()=>checkIncompleteSetup(),5000);
  // فحص الاستبيان النشط للمعلم
  setTimeout(()=>checkActiveSurvey(),3000);
  // فحص رابط الدعوة
  checkInviteCode();
  // إظهار زر المساعدة
  const helpBtn=document.getElementById('help-btn');if(helpBtn)helpBtn.style.display='block';
}

// حفظ قالب جديد (المشرف فقط)
async function saveGradeTemplate(){
  if(!isAdmin()){toast('❌ فقط المشرف يستطيع حفظ القوالب',true);return;}
  const info=getCurrentClassInfo();
  if(!info){toast('❌ اختر شعبة أولاً',true);return;}
  
  const cols=gradeTypes.filter(c=>c.classKey===activeGradesClass);
  if(!cols.length){toast('❌ أضف أنواع تقييم أولاً',true);return;}
  
  if(!confirm(`حفظ قالب سجل درجات لـ:\n📖 ${info.subject}\n🎓 الصف ${info.grade}\n\nسيكون متاحاً لجميع المعلمين الذين يدرّسون نفس المادة والصف.\n\nالمتابعة؟`))return;
  
  // تجريد القالب من classKey (سيتم استبداله عند الاستخدام)
  const template=cols.map(c=>({name:c.name,category:c.category,max:c.max}));
  
  try{
    const{error}=await sb.from('grade_templates').upsert({
      subject:info.subject,
      grade:info.grade,
      grade_types:template,
      created_by:currentUser.email,
      updated_at:new Date().toISOString()
    },{onConflict:'subject,grade'});
    
    if(error){
      console.error(error);
      toast('❌ فشل الحفظ: '+error.message,true);
      return;
    }
    toast(`✅ تم حفظ القالب (${template.length} نوع تقييم)`,'ok');
  }catch(e){
    console.error(e);
    toast('❌ حدث خطأ',true);
  }
}

// تحميل قالب من قاعدة البيانات للشعبة الحالية
async function loadTemplateForCurrentClass(){
  const info=getCurrentClassInfo();
  if(!info){toast('❌ اختر شعبة أولاً',true);return;}
  
  try{
    const{data,error}=await sb.from('grade_templates')
      .select('*')
      .eq('subject',info.subject)
      .eq('grade',info.grade)
      .maybeSingle();
    
    if(error){
      console.error(error);
      toast('❌ خطأ في التحميل',true);
      return;
    }
    
    if(!data||!data.grade_types||!data.grade_types.length){
      toast(`📭 لا يوجد قالب جاهز لـ ${info.subject} - الصف ${info.grade}`,true);
      return;
    }
    
    // التحقق إذا كان هناك أنواع موجودة بالفعل
    const existing=gradeTypes.filter(c=>c.classKey===activeGradesClass);
    if(existing.length){
      if(!confirm(`يوجد ${existing.length} نوع تقييم محفوظ. هل تريد استبدالها بالقالب الجاهز (${data.grade_types.length} نوع)؟`))return;
      // حذف الموجود
      gradeTypes=gradeTypes.filter(c=>c.classKey!==activeGradesClass);
    }
    
    // إضافة القالب
    data.grade_types.forEach((t,i)=>{
      gradeTypes.push({
        id:'g_'+Date.now()+'_'+i,
        name:t.name,
        category:t.category||'homework',
        max:t.max||10,
        classKey:activeGradesClass
      });
    });
    
    renderGradesTable();
    toast(`✅ تم تحميل القالب (${data.grade_types.length} نوع تقييم)`,'ok');
    scheduleSave();
  }catch(e){
    console.error(e);
    toast('❌ حدث خطأ',true);
  }
}

// محاولة تحميل القالب تلقائياً + عرض رسالة "سيتوفر قريباً" إذا لم يوجد
async function autoLoadTemplateIfEmpty(){
  if(!activeGradesClass)return;
  const existing=gradeTypes.filter(c=>c.classKey===activeGradesClass);
  if(existing.length){
    hideTemplateComingSoon();
    return;
  }
  
  const info=getCurrentClassInfo();
  if(!info)return;
  
  // تطبيع اسم المادة لمقارنة مرنة (إزالة المسافات الزائدة والمدّات)
  const normalize=s=>String(s||'').trim().replace(/\u0640/g,'').replace(/\s+/g,' ').replace(/^ال/,'');
  const targetSubject=normalize(info.subject);
  const targetGrade=parseInt(info.grade);
  
  try{
    // جلب جميع القوالب للصف ثم المطابقة محلياً
    const{data,error}=await sb.from('grade_templates')
      .select('subject,grade,grade_types')
      .eq('grade',targetGrade);
    
    if(error)throw error;
    
    // البحث عن قالب مطابق (تجاهل المسافات والاختلافات الدقيقة)
    const match=(data||[]).find(t=>normalize(t.subject)===targetSubject);
    
    if(!match||!match.grade_types||!match.grade_types.length){
      if(!isAdmin())showTemplateComingSoon(info);
      return;
    }
    
    // إضافة القالب تلقائياً
    match.grade_types.forEach((t,i)=>{
      gradeTypes.push({
        id:'g_auto_'+Date.now()+'_'+i,
        name:t.name,
        category:t.category||'homework',
        max:t.max||10,
        classKey:activeGradesClass
      });
    });
    
    hideTemplateComingSoon();
    renderGradesTable();
    toast(`✨ تم تحميل قالب الدرجات تلقائياً (${match.grade_types.length} نوع)`,'ok');
    scheduleSave();
  }catch(e){console.error('autoload error:',e);}
}

function showTemplateComingSoon(info){
  const empty=document.getElementById('grades-empty');
  const wrap=document.getElementById('grades-content');
  if(!empty||!wrap)return;
  wrap.style.display='none';
  empty.style.display='block';
  empty.innerHTML=`
    <div class="grades-empty-icon">📋</div>
    <h3 style="font-size:16px;font-weight:800;color:var(--gold);margin-bottom:8px;">سجل الدرجات سيتوفر قريباً</h3>
    <p style="font-size:13px;color:var(--text);margin-bottom:6px;">قالب درجات <strong>${info.subject}</strong> للصف <strong>${info.grade}</strong> قيد الإعداد من قبل المشرف</p>
    <p style="font-size:11px;color:var(--muted);margin-top:8px;">سيظهر القالب تلقائياً بمجرد إضافته</p>
  `;
}

function hideTemplateComingSoon(){
  // لا شيء — renderGradesTable يتعامل مع الإظهار/الإخفاء
}

// ══ STATS ══════════════════════════════════════════════
function renderStats(){
  const all=allLessons(),total=all.length,done=all.filter(l=>get(l.id).done).length,pct=total?Math.round(done/total*100):0;
  // عدد الحصص الأسبوعية من الجدول الدراسي
  let weeklyPeriods=0;
  if(timetableConfig&&timetableConfig.schedule){Object.values(timetableConfig.schedule).forEach(day=>{weeklyPeriods+=Object.values(day).filter(v=>v).length;});}
  const allCls=getAllClasses();
  const classCounts={};allCls.forEach(cls=>classCounts[cls.id]=0);
  all.forEach(l=>{const s=get(l.id);if(s.classes){Object.keys(s.classes).forEach(c=>{if(s.classes[c]&&classCounts[c]!=null)classCounts[c]++;});}});
  const cards=[{icon:'✅',label:'دروس مكتملة',val:done,sub:`من ${total}`},{icon:'⏳',label:'دروس متبقية',val:total-done,sub:`${100-pct}%`},{icon:'📈',label:'نسبة الإنجاز',val:pct+'%',sub:''},{icon:'🕐',label:'عدد الحصص الأسبوعية',val:weeklyPeriods,sub:'حصة / الأسبوع'},{icon:'🏫',label:'عدد الشعب',val:allCls.length,sub:''},];
  let totalSt=0;allCls.forEach(cls=>totalSt+=(students[cls.id]||[]).length);if(totalSt>0)cards.push({icon:'👥',label:'إجمالي الطلاب',val:totalSt,sub:''});
  document.getElementById('stats-cards').innerHTML=cards.map(c=>`<div class="stat-card"><div class="stat-card-top"><span class="stat-card-icon">${c.icon}</span><span class="stat-card-label">${c.label}</span></div><div class="stat-card-value">${c.val}</div>${c.sub?`<div class="stat-card-sub">${c.sub}</div>`:''}</div>`).join('');
  // ── إحصائية كل شعبة على حدة ──
  const perClassEl=document.getElementById('stats-per-class');
  if(perClassEl&&teacherConfig&&teacherConfig.grades){
    let html='';
    teacherConfig.grades.forEach(g=>{
      const gradeLessons=g.units.flatMap(u=>u.lessons);
      const gradeTotal=gradeLessons.length;
      g.classes.forEach(cls=>{
        // نسبة إنجاز هذه الشعبة: الدروس التي علّمت لهذه الشعبة تحديداً
        const clsDone=gradeLessons.filter(l=>{const s=get(l.id);return s.classes&&s.classes[cls.id];}).length;
        const clsPct=gradeTotal?Math.round(clsDone/gradeTotal*100):0;
        // عدد الطلاب
        const nSt=(students[cls.id]||[]).length;
        // متوسط الدرجات
        const cols=gradeTypes.filter(c=>c.classKey===cls.id);
        let sum=0,cnt=0;
        (students[cls.id]||[]).forEach(st=>{
          const sg=(grades[cls.id]||{})[st.id]||{};let pts=0,maxPts=0;
          cols.forEach(c=>{if(sg[c.id]!=null){pts+=Number(sg[c.id]);maxPts+=Number(c.max);}});
          if(maxPts>0){sum+=(pts/maxPts)*100;cnt++;}
        });
        const avgGrade=cnt?Math.round(sum/cnt):null;
        html+=`<div class="cs-card" style="border-top-color:${cls.color}">
          <div class="cs-card-head">
            <span class="cs-card-name" style="color:${cls.color}">${cls.name}</span>
            <span class="cs-card-grade">الصف ${g.num}</span>
          </div>
          <div class="cs-row"><span class="cs-row-label">✅ الدروس المنجزة</span><span class="cs-row-val">${clsDone} / ${gradeTotal}</span></div>
          <div class="cs-bar-wrap"><div class="cs-bar" style="width:${clsPct}%;background:${cls.color}"></div></div>
          <div class="cs-row"><span class="cs-row-label">📈 نسبة الإنجاز</span><span class="cs-row-val">${clsPct}%</span></div>
          <div class="cs-row"><span class="cs-row-label">👥 عدد الطلاب</span><span class="cs-row-val">${nSt}</span></div>
          <div class="cs-row"><span class="cs-row-label">🎯 متوسط الدرجات</span><span class="cs-row-val">${avgGrade!=null?avgGrade+'%':'—'}</span></div>
        </div>`;
      });
    });
    perClassEl.innerHTML=html||'<div style="color:var(--muted);font-size:12px">لا توجد شعب</div>';
  }
  const secsEl=document.getElementById('stats-sections');
  if(teacherConfig&&teacherConfig.grades){
    const grade=teacherConfig.grades[currentTrackerIdx]||teacherConfig.grades[0];
    if(grade){secsEl.innerHTML=grade.units.map(unit=>{const ls=unit.lessons,sd=ls.filter(l=>get(l.id).done).length,sp=ls.length?Math.round(sd/ls.length*100):0;return`<div class="chart-row"><span class="chart-row-label">📚 ${unit.name}</span><div class="chart-row-bar-wrap"><div class="chart-row-bar" style="width:${sp}%;background:linear-gradient(90deg,var(--red),var(--gold))">${sp}% (${sd}/${ls.length})</div></div></div>`;}).join('');}
  }
  const maxC=Math.max(...allCls.map(cls=>classCounts[cls.id]||0),1);
  document.getElementById('stats-classes').innerHTML=allCls.map(cls=>{const cnt=classCounts[cls.id]||0;const pctW=(cnt/maxC)*100;return`<div class="chart-row"><span class="chart-row-label" style="color:${cls.color}">🏫 ${cls.name}</span><div class="chart-row-bar-wrap"><div class="chart-row-bar" style="width:${pctW}%;background:${cls.color}">${cnt}</div></div></div>`;}).join('');
  const wdays=[{id:'sun',name:'أحد'},{id:'mon',name:'إثنين'},{id:'tue',name:'ثلاثاء'},{id:'wed',name:'أربعاء'},{id:'thu',name:'خميس'}];
  document.getElementById('stats-week').innerHTML=wdays.map(d=>{const sch=timetableConfig.schedule[d.id]||{};const count=Object.values(sch).filter(v=>v).length;return`<div class="week-cell"><div class="wc-day">${d.name}</div><div class="wc-count">${count}</div><div style="font-size:9px;color:var(--muted)">حصة</div></div>`;}).join('');
  const gCard=document.getElementById('stats-grades-card');const hasGrades=allCls.some(cls=>{const sList=students[cls.id]||[];const cols=gradeTypes.filter(c=>c.classKey===cls.id);return sList.length>0&&cols.length>0;});
  if(hasGrades){gCard.style.display='block';document.getElementById('stats-grades').innerHTML=allCls.map(cls=>{const sList=students[cls.id]||[];const cols=gradeTypes.filter(c=>c.classKey===cls.id);let sum=0,cnt=0;sList.forEach(st=>{const sg=(grades[cls.id]||{})[st.id]||{};let pts=0,maxPts=0;cols.forEach(c=>{if(sg[c.id]!=null){pts+=Number(sg[c.id]);maxPts+=Number(c.max);}});if(maxPts>0){sum+=(pts/maxPts)*100;cnt++;}});const avg=cnt?Math.round(sum/cnt):0;return`<div class="chart-row"><span class="chart-row-label" style="color:${cls.color}">${cls.name}</span><div class="chart-row-bar-wrap"><div class="chart-row-bar" style="width:${avg}%;background:${cls.color}">${avg}%</div></div></div>`;}).join('');}else{gCard.style.display='none';}
}

// ══ BEHAVIOR ════════════════════════════════════════════
let behaviorStudents={};   // {classKey: [{id,name,phone}]}
let behaviorViolations={}; // {studentId: [{type,date,sent}]}
let activeBehaviorClass='';

const VIOLATION_TYPES=[
  'تأخر عن الحصة',
  'غياب بدون عذر',
  'عدم إنجاز الواجب',
  'إخلال بالنظام',
  'استخدام الجوال',
  'عدم احترام المعلم',
  'الغش في الاختبار',
  'مخالفة الزي المدرسي',
  'أخرى'
];

function saveBehaviorPhone(){
  const phone=document.getElementById('behavior-teacher-phone').value.trim();
  localStorage.setItem('behaviorTeacherPhone',phone);
  // حفظ في Supabase أيضاً
  scheduleSave();
}

function loadBehaviorPhone(){
  const phone=localStorage.getItem('behaviorTeacherPhone')||'';
  const el=document.getElementById('behavior-teacher-phone');
  if(el)el.value=phone;
}

function saveBehaviorData(){
  // حفظ في Supabase (متزامن بين الأجهزة)
  scheduleSave();
}

function loadBehaviorData(){
  // البيانات تُحمَّل من Supabase في showApp تلقائياً
  // هذه الدالة تبقى للتوافق فقط
}

function initBehaviorPage(){
  loadBehaviorData();
  loadBehaviorPhone();
  renderBehaviorTabs();
  updateBehaviorStats();
}

function getAllClasses2(){
  // نفس الشعب الموجودة في الجدول والدرجات
  return getAllClasses().map(cls=>({
    id:cls.id,
    label:cls.name||(cls.gradeName+' - '+cls.id)
  }));
}

function renderBehaviorTabs(){
  const tabs=document.getElementById('behavior-tabs');
  if(!tabs)return;
  const classes=getAllClasses2();
  if(!classes.length){
    tabs.innerHTML='<div style="color:var(--muted);font-size:12px">لا توجد شعب - أكمل الإعداد أولاً</div>';
    return;
  }
  if(!activeBehaviorClass||!classes.find(c=>c.id===activeBehaviorClass)){
    activeBehaviorClass=classes[0].id;
  }
  tabs.innerHTML=classes.map(c=>`
    <button class="behavior-tab${c.id===activeBehaviorClass?' active':''}" onclick="switchBehaviorClass('${c.id}')">
      ${c.label}
      ${(behaviorStudents[c.id]||[]).length?`<span style="font-size:10px;margin-right:4px;opacity:.7">${(behaviorStudents[c.id]||[]).length}</span>`:''}
    </button>
  `).join('');
  renderBehaviorTable();
}

function switchBehaviorClass(id){
  activeBehaviorClass=id;
  renderBehaviorTabs();
}

function renderBehaviorTable(){
  const wrap=document.getElementById('behavior-table-wrap');
  if(!wrap)return;
  const list=behaviorStudents[activeBehaviorClass]||[];

  if(!list.length){
    wrap.innerHTML=`<div class="behavior-empty">📭 لا يوجد طلاب في هذه الشعبة<br><span style="font-size:11px">استورد قائمة الطلاب من الأعلى</span></div>`;
    return;
  }

  let html=`<div style="overflow-x:auto;margin:0 -4px;"><table class="behavior-table">
    <thead><tr>
      <th>#</th>
      <th>اسم الطالب</th>
      <th>رقم ولي الأمر</th>
      <th>المخالفة</th>
      <th>إرسال</th>
      <th>📊 الدرجات</th>
      <th>السجل</th>
    </tr></thead><tbody>`;

  list.forEach((s,idx)=>{
    const vList=behaviorViolations[s.id]||[];
    const lastV=vList[vList.length-1];
    const hasPhone=!!s.phone;
    html+=`<tr>
      <td style="color:var(--muted)">${idx+1}</td>
      <td style="font-weight:700;white-space:nowrap;">${escHtml(s.name)}</td>
      <td>
        <input type="tel" value="${escHtml(s.phone||'')}" 
          placeholder="أدخل الرقم"
          style="background:var(--card);border:1px solid var(--border);border-radius:6px;color:var(--text);font-family:'Cairo',sans-serif;font-size:11px;padding:4px 8px;outline:none;width:130px;direction:ltr"
          onchange="updateStudentPhone('${s.id}',this.value)"/>
      </td>
      <td>
        <select class="violation-select" id="vsel_${s.id}">
          <option value="">اختر المخالفة...</option>
          ${VIOLATION_TYPES.map(v=>`<option value="${v}">${v}</option>`).join('')}
        </select>
      </td>
      <td>
        <button class="send-wa-btn" onclick="sendViolationWA('${s.id}')" ${!hasPhone?'disabled title="أدخل رقم ولي الأمر أولاً"':''}>
          📤 واتساب
        </button>
      </td>
      <td>
        <button class="send-grades-btn" onclick="sendStudentGradesWA('${s.id}','${activeBehaviorClass}')" ${!hasPhone?'disabled title="أدخل رقم ولي الأمر أولاً"':''}>
          📊 إرسال
        </button>
      </td>
      <td>
        <span style="font-size:11px;color:var(--muted)">${vList.length?vList.length+' مخالفة':'-'}</span>
        ${lastV?`<div class="violation-log">آخر: ${lastV.type}</div>`:''}
      </td>
    </tr>`;
  });

  html+=`</tbody></table></div>
  <div style="margin-top:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
    <span style="font-size:11px;color:var(--muted)">${list.length} طالب</span>
    <button onclick="clearBehaviorClass()" style="background:none;border:1px solid var(--border);color:var(--muted);border-radius:6px;padding:5px 12px;font-size:11px;cursor:pointer;font-family:'Cairo',sans-serif">🗑️ مسح قائمة الشعبة</button>
  </div>`;

  wrap.innerHTML=html;
}

function normalizePhone(phone){
  // إزالة المسافات والرموز
  let p=phone.replace(/[\s\-\(\)]/g,'');
  // إذا كان 8 أرقام يبدأ بـ 9 أو 7 → أضف 968
  if(/^[97]\d{7}$/.test(p))p='968'+p;
  // إذا بدأ بـ 00968 → حوّل لـ 968
  if(p.startsWith('00968'))p=p.slice(2);
  // إذا بدأ بـ + → أزل الـ +
  if(p.startsWith('+'))p=p.slice(1);
  return p;
}

function updateStudentPhone(id,phone){
  const cleaned=normalizePhone(phone);
  Object.keys(behaviorStudents).forEach(cls=>{
    const s=behaviorStudents[cls].find(x=>x.id===id);
    if(s){s.phone=cleaned;}
  });
  saveBehaviorData();
  updateBehaviorStats();
}

function sendViolationWA(studentId){
  const sel=document.getElementById(`vsel_${studentId}`);
  if(!sel||!sel.value){toast('❌ اختر نوع المخالفة أولاً',true);return;}
  
  const cls=activeBehaviorClass;
  const student=(behaviorStudents[cls]||[]).find(s=>s.id===studentId);
  if(!student){return;}
  if(!student.phone){toast('❌ أدخل رقم ولي الأمر أولاً',true);return;}

  const teacherPhone=localStorage.getItem('behaviorTeacherPhone')||'';
  const teacherName=displayName||'المعلم';
  const clsLabel=getAllClasses2().find(c=>c.id===cls)?.label||cls;
  const today=new Date().toLocaleDateString('ar-OM',{year:'numeric',month:'long',day:'numeric'});
  const violation=sel.value;

  const msg=`السلام عليكم ورحمة الله وبركاته 🌿

ولي أمر الطالب/ *${student.name}*

نود إعلامكم بأنه تم تسجيل المخالفة التالية:
📋 *المخالفة:* ${violation}
🏫 *الشعبة:* ${clsLabel}
📅 *التاريخ:* ${today}

نأمل منكم المتابعة مع الطالب وتوجيهه.

*${teacherName}*${teacherPhone?' | '+teacherPhone:''}
خطتي الفصلية 📚`;

  // تسجيل المخالفة
  if(!behaviorViolations[studentId])behaviorViolations[studentId]=[];
  behaviorViolations[studentId].push({
    type:violation,
    date:new Date().toISOString(),
    sent:true
  });
  saveBehaviorData();
  updateBehaviorStats();
  renderBehaviorTable();

  // فتح واتساب - يكتشف تلقائياً الجهاز
  const phone=student.phone.replace(/[^0-9]/g,'');
  const encodedMsg=encodeURIComponent(msg);
  const isMobile=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  // على الموبايل: wa.me يفتح التطبيق مباشرة
  // على اللابتوب: web.whatsapp.com أكثر موثوقية
  const url=isMobile
    ?`https://wa.me/${phone}?text=${encodedMsg}`
    :`https://web.whatsapp.com/send?phone=${phone}&text=${encodedMsg}`;
  window.open(url,'_blank');
  
  toast('✅ تم فتح واتساب - اضغط إرسال');
}

// استيراد من Excel
async function importBehaviorExcel(event){
  const file=event.target.files[0];
  if(!file)return;
  
  // تحميل SheetJS
  if(!window.XLSX){
    const script=document.createElement('script');
    script.src='https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
    document.head.appendChild(script);
    await new Promise(r=>script.onload=r);
  }

  const reader=new FileReader();
  reader.onload=e=>{
    try{
      const wb=XLSX.read(e.target.result,{type:'binary'});
      const ws=wb.Sheets[wb.SheetNames[0]];
      const rows=XLSX.utils.sheet_to_json(ws,{header:1});
      
      if(!rows.length){toast('❌ الملف فارغ',true);return;}

      const nameKW=['الاسم','اسم الطالب','اسم','student','name','طالب','أسماء'];
      const phoneKW=['الهاتف النقال','هاتف ولي','ولي الأمر','هاتف','جوال','رقم الهاتف','phone','mobile','ولي','أولياء'];

      // ═══ البحث عن صف العناوين في أول 50 صف ═══
      let headerRowIdx=-1;
      let nameCol=-1;
      let phoneCol=-1;

      // المرور الأول: صف يحتوي على الاسم والهاتف معاً
      for(let ri=0;ri<Math.min(50,rows.length);ri++){
        const row=rows[ri];
        let fn=-1,fp=-1;
        row.forEach((cell,ci)=>{
          const v=String(cell||'').trim().replace(/ـ/g,'').replace(/\s+/g,' ').toLowerCase();
          if(fn<0&&nameKW.some(kw=>v.includes(kw)))fn=ci;
          if(fp<0&&phoneKW.some(kw=>v.includes(kw)))fp=ci;
        });
        if(fn>=0&&fp>=0){headerRowIdx=ri;nameCol=fn;phoneCol=fp;break;}
      }

      // المرور الثاني: أحدهما فقط
      if(headerRowIdx<0){
        for(let ri=0;ri<Math.min(50,rows.length);ri++){
          const row=rows[ri];
          let fn=-1,fp=-1;
          row.forEach((cell,ci)=>{
            const v=String(cell||'').trim().replace(/ـ/g,'').replace(/\s+/g,' ').toLowerCase();
            if(fn<0&&nameKW.some(kw=>v.includes(kw)))fn=ci;
            if(fp<0&&phoneKW.some(kw=>v.includes(kw)))fp=ci;
          });
          if(fn>=0||fp>=0){
            headerRowIdx=ri;
            if(fn>=0)nameCol=fn;
            if(fp>=0)phoneCol=fp;
            break;
          }
        }
      }

      // إذا لم يجد عناوين → حلل البيانات
      if(nameCol<0||phoneCol<0){
        const vn={},vp={};
        rows.slice(0,30).forEach(r=>{
          r.forEach((cell,i)=>{
            const v=String(cell||'').trim().replace(/[\s\-\(\)]/g,'');
            if(!v||v==='null')return;
            if(/^[\d\+]{7,15}$/.test(v))vp[i]=(vp[i]||0)+1;
            else if(/[؀-ۿ]/.test(v)&&v.length>3)vn[i]=(vn[i]||0)+1;
          });
        });
        if(nameCol<0){const b=Object.entries(vn).sort((a,b)=>b[1]-a[1])[0];if(b)nameCol=+b[0];}
        if(phoneCol<0){const b=Object.entries(vp).sort((a,b)=>b[1]-a[1]).find(e=>+e[0]!==nameCol);if(b)phoneCol=+b[0];}
        if(headerRowIdx<0)headerRowIdx=0;
      }

      if(nameCol<0)nameCol=0;
      if(phoneCol<0||phoneCol===nameCol)phoneCol=nameCol===0?1:0;

      // ═══ قراءة الطلاب - تجاهل الصفوف الفارغة ═══
      const dataRows=rows.slice(headerRowIdx+1).filter(r=>{
        const name=String(r[nameCol]||'').trim();
        return name&&name.length>2&&name!=='null'&&!/^\d+$/.test(name)&&!nameKW.some(kw=>name.toLowerCase().includes(kw));
      });

      const hdr=headerRowIdx>=0?(rows[headerRowIdx]||[]):[];
      console.log('[Excel] اسم:col'+nameCol+'('+String(hdr[nameCol]||'').trim()+') هاتف:col'+phoneCol+'('+String(hdr[phoneCol]||'').trim()+') طلاب:'+dataRows.length);

      if(!dataRows.length){toast('❌ لم يتم العثور على بيانات - تحقق من الملف',true);return;}

      const students=dataRows.map(r=>{
        const nameVal=String(r[nameCol]||'').trim();
        const rawPhone=String(r[phoneCol]||'').trim();
        const phone=rawPhone&&rawPhone!=='null'?normalizePhone(rawPhone):'';
        return{id:'bs_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name:nameVal,phone};
      }).filter(s=>s.name&&s.name.length>2);

      if(!students.length){toast('❌ لم يتم التعرف على أسماء الطلاب',true);return;}
      // إظهار معاينة قبل الإضافة
      showBehaviorPreview(students);
    }catch(e){
      toast('❌ خطأ في قراءة الملف: '+e.message,true);
    }
  };
  reader.readAsBinaryString(file);
  event.target.value='';
}

// استيراد من لصق
function importBehaviorPaste(){
  const text=document.getElementById('behavior-paste-area').value.trim();
  if(!text){toast('❌ الصق البيانات أولاً',true);return;}
  
  const lines=text.split('\n').map(l=>l.trim()).filter(l=>l);
  const students=lines.map(line=>{
    // فصل الاسم والرقم بالفاصلة أو التاب
    const parts=line.split(/[,،\t]+/).map(p=>p.trim());
    let name='',phone='';
    parts.forEach(p=>{
      const pClean=p.replace(/[\s\-\(\)]/g,'');
      if(/^[\d+]{7,15}$/.test(pClean))phone=normalizePhone(p);
      else if(p)name=p;
    });
    return{id:'bs_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name,phone};
  }).filter(s=>s.name);

  if(!students.length){toast('❌ لم يتم التعرف على أي طالب',true);return;}
  addBehaviorStudents(students);
  document.getElementById('behavior-paste-area').value='';
}

function addBehaviorStudents(newStudents){
  if(!behaviorStudents[activeBehaviorClass])behaviorStudents[activeBehaviorClass]=[];
  const existing=new Set(behaviorStudents[activeBehaviorClass].map(s=>s.name));
  const added=newStudents.filter(s=>!existing.has(s.name));
  behaviorStudents[activeBehaviorClass].push(...added);
  saveBehaviorData();
  renderBehaviorTabs();
  updateBehaviorStats();
  toast(`✅ تم إضافة ${added.length} طالب`);
}

function clearBehaviorClass(){
  if(!confirm(`هل تريد مسح قائمة هذه الشعبة؟`))return;
  behaviorStudents[activeBehaviorClass]=[];
  saveBehaviorData();
  renderBehaviorTable();
  renderBehaviorTabs();
  updateBehaviorStats();
  toast('✅ تم المسح');
}

function clearAllBehaviorData(){
  const total=Object.values(behaviorStudents).reduce((s,a)=>s+a.length,0);
  if(!confirm(`هل تريد حذف كامل سجل السلوك؟\n${total} طالب و${Object.values(behaviorViolations).reduce((s,a)=>s+a.length,0)} مخالفة\n\nلا يمكن التراجع!`))return;
  behaviorStudents={};
  behaviorViolations={};
  saveBehaviorData();
  renderBehaviorTabs();
  updateBehaviorStats();
  toast('✅ تم حذف كامل السجل');
}

// ═══ معاينة قبل الرفع ═══
let _previewStudents=[];

function previewBehaviorPaste(){
  const text=document.getElementById('behavior-paste-area').value.trim();
  if(!text){toast('❌ الصق البيانات أولاً',true);return;}
  const lines=text.split('\n').map(l=>l.trim()).filter(l=>l);
  const students=lines.map(line=>{
    const parts=line.split(/[,،\t]+/).map(p=>p.trim());
    let name='',phone='';
    parts.forEach(p=>{
      const pClean=p.replace(/[\s\-\(\)]/g,'');
      if(/^[\d+]{7,15}$/.test(pClean))phone=normalizePhone(p);
      else if(p)name=p;
    });
    return{id:'bs_'+Date.now()+'_'+Math.random().toString(36).slice(2,6),name,phone};
  }).filter(s=>s.name&&s.name.length>1);

  if(!students.length){toast('❌ لم يتم التعرف على أي طالب',true);return;}
  showBehaviorPreview(students);
}

function showBehaviorPreview(students){
  _previewStudents=students;
  const withPhone=students.filter(s=>s.phone).length;
  const noPhone=students.length-withPhone;

  document.getElementById('bprev-stats').textContent=
    `${students.length} طالب | ${withPhone} برقم | ${noPhone} بدون رقم`;

  document.getElementById('bprev-body').innerHTML=students.map((s,i)=>`
    <div class="bprev-item">
      <span class="bprev-num">${i+1}</span>
      <span class="bprev-name">${escHtml(s.name)}</span>
      ${s.phone
        ?`<span class="bprev-phone">${escHtml(s.phone)}</span>`
        :`<span class="bprev-nophone">بدون رقم</span>`}
    </div>
  `).join('');

  document.getElementById('bprev-modal').style.display='flex';
}

function closeBehaviorPreview(e){
  if(e&&e.target!==document.getElementById('bprev-modal'))return;
  document.getElementById('bprev-modal').style.display='none';
  _previewStudents=[];
}

function confirmBehaviorPreview(){
  if(!_previewStudents.length)return;
  addBehaviorStudents(_previewStudents);
  document.getElementById('bprev-modal').style.display='none';
  document.getElementById('behavior-paste-area').value='';
  _previewStudents=[];
}

function updateBehaviorStats(){
  const totalStudents=Object.values(behaviorStudents).reduce((s,arr)=>s+arr.length,0);
  const totalViolations=Object.values(behaviorViolations).reduce((s,arr)=>s+arr.length,0);
  const totalSent=Object.values(behaviorViolations).reduce((s,arr)=>s+arr.filter(v=>v.sent).length,0);
  const s1=document.getElementById('bstat-students');
  const s2=document.getElementById('bstat-violations');
  const s3=document.getElementById('bstat-sent');
  if(s1)s1.textContent=totalStudents;
  if(s2)s2.textContent=totalViolations;
  if(s3)s3.textContent=totalSent;
}

function downloadBehaviorTemplate(){
  const csv='\uFEFFاسم الطالب,رقم ولي الأمر\nمحمد أحمد,96812345678\nسالم علي,96898765432';
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;a.download='قالب_السلوك.csv';
  a.click();URL.revokeObjectURL(url);
  toast('✅ تم تحميل القالب');
}

// ════════════════════════════════════════════════════════════════
// 📡 إرسال Push من السيرفر
// ════════════════════════════════════════════════════════════════
async function sendPushToAll(title, body){
  if(!isAdmin())return;
  try{
    await fetch(`${SUPABASE_URL}/functions/v1/send-push`,{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'Authorization':`Bearer ${SUPABASE_ANON_KEY}`
      },
      body:JSON.stringify({title,message:body,send_to_all:true})
    });
  }catch(e){console.warn('[Push] خطأ في الإرسال:',e.message);}
}

async function sendPushToUser(userId, title, body){
  if(!isAdmin())return;
  try{
    await fetch(`${SUPABASE_URL}/functions/v1/send-push`,{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'Authorization':`Bearer ${SUPABASE_ANON_KEY}`
      },
      body:JSON.stringify({title,message:body,target_user_id:userId})
    });
  }catch(e){console.warn('[Push] خطأ في الإرسال:',e.message);}
}

// ════════════════════════════════════════════════════════════════
// 🔔 نظام الإشعارات المتكاملة
// ════════════════════════════════════════════════════════════════
let _notifPermission='default';
let _lastBellCount=0;
let _lastAnnouncementId=null;
let _lastMsgId=null;

let _swRegistration=null;
const VAPID_PUBLIC_KEY='BH26yx18ploy0jp3Wou2UkM-5DLqxR7b184avv487XcaPv7oYvnAMPZ2JItHCkmOnXjaA779Dvoeq1VrRKvjMgo';

async function initPushNotifications(){
  if(!('Notification' in window))return;
  _notifPermission=Notification.permission;

  // تسجيل Service Worker
  if('serviceWorker' in navigator){
    try{
      _swRegistration=await navigator.serviceWorker.register('/khotta/sw.js',{scope:'/khotta/'});
      console.log('[SW] مسجّل بنجاح');
      // إذا الإذن ممنوح → اشترك في Push
      if(Notification.permission==='granted'){
        await subscribeToPush();
      }
    }catch(e){
      console.warn('[SW] فشل التسجيل:',e.message);
    }
  }

  if(_notifPermission==='default'){
    setTimeout(()=>requestNotifPermission(),2000);
  }
  _lastBellCount=getBellReadIds().length;
}

async function subscribeToPush(){
  if(!_swRegistration||!currentUser)return;
  try{
    // تحويل VAPID Key
    const keyBytes=base64urlToUint8Array(VAPID_PUBLIC_KEY);
    const sub=await _swRegistration.pushManager.subscribe({
      userVisibleOnly:true,
      applicationServerKey:keyBytes
    });
    // حفظ الـ subscription في Supabase
    await sb.from('push_subscriptions').upsert({
      user_id:currentUser.id,
      subscription:JSON.parse(JSON.stringify(sub))
    },{onConflict:'user_id'});
    console.log('[Push] تم الاشتراك بنجاح');
  }catch(e){
    console.warn('[Push] فشل الاشتراك:',e.message);
  }
}

function base64urlToUint8Array(base64url){
  const base64=base64url.replace(/-/g,'+').replace(/_/g,'/');
  const padded=base64.padEnd(base64.length+(4-base64.length%4)%4,'=');
  const binary=atob(padded);
  return new Uint8Array([...binary].map(c=>c.charCodeAt(0)));
}

async function requestNotifPermission(){
  if(!('Notification' in window)){
    toast('❌ متصفحك لا يدعم الإشعارات',true);
    return;
  }
  // إذا كانت مرفوضة مسبقاً
  if(Notification.permission==='denied'){
    toast('⚠️ الإشعارات محظورة - افتح إعدادات المتصفح وأعد السماح',true);
    return;
  }
  // إذا كانت مفعّلة مسبقاً
  if(Notification.permission==='granted'){
    toast('✅ الإشعارات مفعّلة بالفعل');
    sendBrowserNotif('خطتي الفصلية 📚','الإشعارات تعمل بشكل صحيح ✅');
    return;
  }
  // طلب الإذن
  const result=await Notification.requestPermission();
  _notifPermission=result;
  if(result==='granted'){
    toast('✅ تم تفعيل الإشعارات بنجاح!');
    sendBrowserNotif('خطتي الفصلية 📚','مرحباً! ستصلك تنبيهات الحصص والإعلانات والرسائل 🔔');
    // الاشتراك في Push
    await subscribeToPush();
  }else if(result==='denied'){
    toast('❌ تم رفض الإشعارات - يمكنك تفعيلها من إعدادات المتصفح',true);
  }
}

function updateNotifMenuBtn(){
  const btn=document.getElementById('notif-menu-item');
  if(!btn)return;
  // لا نخفي الزر أبداً - فقط نغير النص
  btn.style.display='flex';
  if(!('Notification' in window)){
    btn.innerHTML='🔔 الإشعارات غير مدعومة';
    btn.style.color='var(--muted)';
    return;
  }
  if(Notification.permission==='granted'){
    btn.innerHTML='✅ الإشعارات مفعّلة';
    btn.style.color='var(--green)';
  }else if(Notification.permission==='denied'){
    btn.innerHTML='⚠️ الإشعارات محظورة';
    btn.style.color='var(--red2)';
  }else{
    btn.innerHTML='🔔 تفعيل الإشعارات';
    btn.style.color='';
  }
}

function sendBrowserNotif(title, body, tag=''){
  if(!('Notification' in window)||Notification.permission!=='granted')return;
  // تشغيل الصوت حسب النوع
  const soundType=tag==='msg'?'message':tag==='class'?'class':'default';
  playNotifSound(soundType);
  try{
    if(_swRegistration){
      _swRegistration.showNotification(title,{
        body,
        dir:'rtl',
        lang:'ar',
        tag:tag||title,
        icon:'https://teacher-plan.github.io/khotta/favicon.ico',
        badge:'https://teacher-plan.github.io/khotta/favicon.ico',
        requireInteraction:false,
        data:{url:'https://teacher-plan.github.io/khotta/'}
      });
    }else{
      const n=new Notification(title,{body,dir:'rtl',lang:'ar',tag:tag||title});
      n.onclick=()=>{window.focus();n.close();};
      setTimeout(()=>n.close(),6000);
    }
  }catch(e){}
}

// ── مراقبة الإعلانات الجديدة ──
function checkNewAnnouncements(){
  if(!_bellAnnouncements||!_bellAnnouncements.length)return;
  const readIds=getBellReadIds();
  const unread=_bellAnnouncements.filter(a=>!readIds.includes(`${a._type}_${a.id}`));
  
  // إشعار عند وصول إعلان جديد
  const newAnns=unread.filter(a=>a._type==='ann');
  const newMsgs=unread.filter(a=>a._type==='msg');

  if(newAnns.length>0&&newAnns[0].id!==_lastAnnouncementId){
    _lastAnnouncementId=newAnns[0].id;
    sendBrowserNotif(
      `📢 إعلان جديد: ${newAnns[0].title}`,
      newAnns[0].body||''
    );
  }

  if(newMsgs.length>0&&newMsgs[0].id!==_lastMsgId){
    _lastMsgId=newMsgs[0].id;
    sendBrowserNotif(
      `✉️ رسالة خاصة: ${newMsgs[0].title}`,
      newMsgs[0].body||'',
      'msg'
    );
  }

  // تحديث عدد الإشعارات غير المقروءة في عنوان الصفحة
  const count=unread.length;
  document.title=count>0?`(${count}) خطتي الفصلية`:'خطتي الفصلية';
}

// ── إشعار بداية الحصة (تحسين الموجود) ──
const _origFireReminder=typeof fireReminder==='function'?fireReminder:null;
function fireReminder(period,classKey,diff){
  const cls=classConfig[classKey];
  const name=cls?cls.name:classKey;
  const msg=`حصة ${name} تبدأ بعد ${diff} دقيقة`;
  
  // التوست الداخلي
  const el=document.getElementById('reminder-text');
  const toast2=document.getElementById('reminder-toast');
  if(el)el.textContent=msg;
  if(toast2)toast2.classList.add('show');
  
  // إشعار المتصفح
  sendBrowserNotif(`🔔 تذكير حصة`,msg,'class');
  // اهتزاز (موبايل)
  if(navigator.vibrate)navigator.vibrate([300,100,300,100,300]);
}

// ── صوت الإشعار ──
function playNotifSound(type='default'){
  try{
    const ctx=new (window.AudioContext||window.webkitAudioContext)();
    const gain=ctx.createGain();
    gain.connect(ctx.destination);
    gain.gain.setValueAtTime(0.25,ctx.currentTime);

    if(type==='class'){
      // صوت الحصة: ثلاث نغمات تصاعدية
      [600,700,900].forEach((freq,i)=>{
        const osc=ctx.createOscillator();
        osc.connect(gain);
        osc.frequency.value=freq;
        osc.start(ctx.currentTime+i*0.15);
        osc.stop(ctx.currentTime+i*0.15+0.12);
      });
    }else if(type==='message'){
      // صوت الرسالة: نغمتان قصيرتان
      [700,900].forEach((freq,i)=>{
        const osc=ctx.createOscillator();
        osc.connect(gain);
        osc.frequency.value=freq;
        osc.start(ctx.currentTime+i*0.12);
        osc.stop(ctx.currentTime+i*0.12+0.1);
      });
    }else{
      // صوت الإعلان العام: نغمة واحدة ناعمة
      const osc=ctx.createOscillator();
      osc.connect(gain);
      osc.type='sine';
      osc.frequency.setValueAtTime(750,ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(550,ctx.currentTime+0.3);
      gain.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.4);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime+0.4);
    }
  }catch(e){}
}

// ── تحديث عنوان الصفحة وإشعارات الجرس ──
// نضيف checkNewAnnouncements لـ renderBell
const _origRenderBell=typeof renderBell==='function'?renderBell:null;

// ══ HELP GUIDE ═════════════════════════════════════════
function toggleHelp(){
  const bg=document.getElementById('help-modal-bg');
  if(!bg)return;
  bg.style.display=bg.style.display==='none'?'flex':'none';
}

// ══ ANALYTICS ══════════════════════════════════════════
async function loadAnalytics(){
  if(!isAdmin())return;
  try{
    // جلب جميع البيانات
    const{data:profiles}=await sb.from('profiles').select('id,data,updated_at');
    const{data:msgs}=await sb.from('private_messages').select('id');
    const{data:surveyRes}=await sb.from('survey_responses').select('id');

    const now=new Date();
    const weekAgo=new Date(now-7*24*60*60*1000);

    // ══ KPIs ══
    const total=profiles?.length||0;
    const active=(profiles||[]).filter(p=>{
      if(!p.updated_at)return false;
      return new Date(p.updated_at)>weekAgo;
    }).length;

    // حساب إجمالي الطلاب والمخالفات
    let totalStudents=0,totalViolations=0;
    const subjectCount={},gradeCount={};
    (profiles||[]).forEach(p=>{
      const d=p.data||{};
      // الطلاب
      const sts=d.students||{};
      Object.values(sts).forEach(arr=>{totalStudents+=arr.length;});
      // المخالفات
      const vios=d.behavior_violations||{};
      Object.values(vios).forEach(arr=>{totalViolations+=arr.length;});
      // المواد
      const subj=(d.teacher_config?.subjects||[d.teacher_config?.subject]).filter(Boolean);
      subj.forEach(s=>{subjectCount[s]=(subjectCount[s]||0)+1;});
      // الصفوف
      const grades=d.teacher_config?.grades||[];
      grades.forEach(g=>{
        const key=`الصف ${g.num||g}`;
        gradeCount[key]=(gradeCount[key]||0)+1;
      });
    });

    // تحديث KPIs
    document.getElementById('an-total').textContent=total;
    document.getElementById('an-active').textContent=active;
    document.getElementById('an-grades').textContent=totalStudents.toLocaleString('ar');
    document.getElementById('an-violations').textContent=totalViolations.toLocaleString('ar');
    document.getElementById('an-msgs').textContent=(msgs?.length||0).toLocaleString('ar');
    document.getElementById('an-survey-res').textContent=(surveyRes?.length||0).toLocaleString('ar');

    // ══ جدول النشاط ══
    const sorted=[...(profiles||[])].sort((a,b)=>new Date(b.updated_at||0)-new Date(a.updated_at||0));
    const actTable=document.getElementById('an-activity-table');
    actTable.innerHTML=`<table class="analytics-table">
      <thead><tr><th>#</th><th>اسم المعلم</th><th>المادة</th><th>الصف</th><th>آخر دخول</th><th>الحالة</th></tr></thead>
      <tbody>${sorted.map((p,i)=>{
        const d=p.data||{};
        const name=d.display_name||d.teacher_name||d.full_name||d.email||'—';
        const subj=d.teacher_config?.subject||'—';
        const grade=d.teacher_config?.grades?.[0]?.num?`الصف ${d.teacher_config.grades[0].num}`:'—';
        const last=p.updated_at?getLastSeenText(p.updated_at):'لم يدخل';
        const isAct=p.updated_at&&new Date(p.updated_at)>weekAgo;
        return `<tr>
          <td style="color:var(--muted)">${i+1}</td>
          <td style="font-weight:700">${escHtml(name)}</td>
          <td>${escHtml(subj)}</td>
          <td>${escHtml(grade)}</td>
          <td style="color:var(--muted)">${last}</td>
          <td><span class="${isAct?'active':'inactive'}-dot"></span> ${isAct?'نشط':'غائب'}</td>
        </tr>`;
      }).join('')}</tbody>
    </table>`;

    // ══ مخطط المواد ══
    const subjEl=document.getElementById('an-subjects-chart');
    const subjSorted=Object.entries(subjectCount).sort((a,b)=>b[1]-a[1]).slice(0,8);
    const maxSubj=subjSorted[0]?.[1]||1;
    subjEl.innerHTML=subjSorted.length?subjSorted.map(([s,c])=>`
      <div class="analytics-bar-row">
        <div class="analytics-bar-label">${escHtml(s)}</div>
        <div class="analytics-bar"><div class="analytics-bar-fill gold" style="width:${Math.round(c/maxSubj*100)}%"></div></div>
        <div class="analytics-bar-val">${c}</div>
      </div>`).join(''):'<div style="color:var(--muted);font-size:12px;padding:10px">لا توجد بيانات بعد</div>';

    // ══ مخطط الصفوف ══
    const gradeEl=document.getElementById('an-grades-chart');
    const gradeSorted=Object.entries(gradeCount).sort((a,b)=>{
      const na=parseInt(a[0].replace(/\D/g,''))||0;
      const nb=parseInt(b[0].replace(/\D/g,''))||0;
      return na-nb;
    });
    const maxGrade=gradeSorted[0]?.[1]||1;
    gradeEl.innerHTML=gradeSorted.length?gradeSorted.map(([g,c])=>`
      <div class="analytics-bar-row">
        <div class="analytics-bar-label">${escHtml(g)}</div>
        <div class="analytics-bar"><div class="analytics-bar-fill blue" style="width:${Math.round(c/maxGrade*100)}%"></div></div>
        <div class="analytics-bar-val">${c}</div>
      </div>`).join(''):'<div style="color:var(--muted);font-size:12px;padding:10px">لا توجد بيانات بعد</div>';

    // ══ المعلمون الغائبون ══
    const inactiveEl=document.getElementById('an-inactive-list');
    const inactive=sorted.filter(p=>!p.updated_at||new Date(p.updated_at)<=weekAgo);
    if(!inactive.length){
      inactiveEl.innerHTML='<div style="color:var(--green2);font-size:13px;text-align:center;padding:10px">✅ جميع المعلمين نشطون هذا الأسبوع!</div>';
    }else{
      inactiveEl.innerHTML=`<table class="analytics-table">
        <thead><tr><th>اسم المعلم</th><th>المادة</th><th>آخر دخول</th></tr></thead>
        <tbody>${inactive.map(p=>{
          const d=p.data||{};
          const name=d.display_name||d.teacher_name||d.full_name||d.email||'—';
          const subj=d.teacher_config?.subject||'—';
          const last=p.updated_at?getLastSeenText(p.updated_at):'لم يدخل قط';
          return `<tr>
            <td style="font-weight:700;color:var(--red2)">${escHtml(name)}</td>
            <td>${escHtml(subj)}</td>
            <td style="color:var(--muted)">${last}</td>
          </tr>`;
        }).join('')}</tbody>
      </table>`;
    }

  }catch(e){
    toast('❌ خطأ في تحميل الإحصائيات: '+e.message,true);
  }
}

// ══ CERTIFICATES & TOP STUDENTS ══════════════════════════
let _tsSelectedCol=null;

function openTopStudents(){
  if(!activeGradesClass){toast('❌ اختر شعبة أولاً',true);return;}
  const cols=gradeTypes.filter(c=>c.classKey===activeGradesClass);
  if(!cols.length){toast('❌ لا توجد أنواع تقييم في هذه الشعبة',true);return;}
  const sList=getUnifiedStudents(activeGradesClass);
  if(!sList.length){toast('❌ لا يوجد طلاب في هذه الشعبة',true);return;}
  
  _tsSelectedCol=null;
  document.getElementById('ts-step1').style.display='block';
  document.getElementById('ts-step2').style.display='none';
  
  // عرض أنواع التقييم
  const colList=document.getElementById('ts-col-list');
  colList.innerHTML=cols.map(c=>{
    const sList2=getUnifiedStudents(activeGradesClass);
    const gradeData=grades[activeGradesClass]||{};
    const fullScoreCount=sList2.filter(s=>{
      const val=gradeData[s.id]?.[c.id];
      return val!=null&&!isNaN(val)&&Number(val)===Number(c.max);
    }).length;
    return `<button class="ts-col-btn" onclick="selectTsCol('${c.id}','${escAttr(c.name)}',${c.max})">
      <span>${escHtml(c.name)}</span>
      <span style="font-size:11px;color:var(--green2)">${fullScoreCount>0?`🏆 ${fullScoreCount} طالب`:''}</span>
    </button>`;
  }).join('');
  
  document.getElementById('top-students-modal').style.display='flex';
}

function closeTopStudents(){
  document.getElementById('top-students-modal').style.display='none';
}

function backToStep1(){
  document.getElementById('ts-step1').style.display='block';
  document.getElementById('ts-step2').style.display='none';
  _tsSelectedCol=null;
}

function selectTsCol(colId, colName, colMax){
  _tsSelectedCol={id:colId, name:colName, max:colMax};
  
  document.getElementById('ts-selected-col-label').textContent=`🏆 المتفوقون في: ${colName}`;
  
  // جلب الطلاب الحاصلين على العلامة الكاملة
  const sList=getUnifiedStudents(activeGradesClass);
  const gradeData=grades[activeGradesClass]||{};
  const topStudents=sList.filter(s=>{
    const val=gradeData[s.id]?.[colId];
    return val!=null&&!isNaN(val)&&Number(val)===Number(colMax);
  });
  
  const listEl=document.getElementById('ts-students-list');
  const exportAllBtn=document.getElementById('ts-export-all-btn');
  
  if(!topStudents.length){
    listEl.innerHTML=`<div class="ts-empty">😔 لا يوجد طلاب حصلوا على العلامة الكاملة (${colMax}/${colMax}) في هذا التقييم بعد</div>`;
    exportAllBtn.style.display='none';
  }else{
    listEl.innerHTML=topStudents.map((s,i)=>`
      <div class="ts-student-row">
        <div class="ts-student-rank">${i+1}</div>
        <div class="ts-student-name">${escHtml(s.name)}</div>
        <div class="ts-student-score">${colMax}/${colMax} ✅</div>
        <button class="ts-cert-btn" onclick="downloadCertificate('${s.id}','${escAttr(s.name)}')">📜 شهادة</button>
      </div>
    `).join('');
    exportAllBtn.style.display='block';
    exportAllBtn.textContent=`📥 تصدير جميع الشهادات (${topStudents.length})`;
  }
  
  document.getElementById('ts-step1').style.display='none';
  document.getElementById('ts-step2').style.display='block';
}

// ─── توليد الشهادة ───
function generateCertHTML(studentName, colName, classKey){
  const allCls=getAllClasses();
  const cls=allCls.find(c=>c.id===classKey);
  const className=cls?cls.name:'';
  const gradeName=cls?cls.gradeName:'';
  const subject=teacherConfig?.subject||'';
  const semester=teacherConfig?.semester||'الفصل الأول';
  const teacherName=teacherConfig?.display_name||teacherConfig?.teacher_name||'المعلم';
  const year='٢٠٢٦/٢٠٢٥';
  const today=new Date().toLocaleDateString('ar-SA',{year:'numeric',month:'long',day:'numeric'});
  
  return `<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Tajawal:wght@900&family=Scheherazade+New:wght@700&family=Cairo:wght@400;700&display=swap"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tajawal:wght@900&family=Scheherazade+New:wght@700&family=Cairo:wght@400;700&display=swap" media="print" onload="this.media='all'"/>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{width:700px;height:490px;overflow:hidden;font-family:'Cairo',sans-serif;}
.cert{width:700px;height:490px;background:#fff;position:relative;overflow:hidden;}
.shape-tr{position:absolute;top:-30px;left:-20px;width:200px;height:160px;background:#2DC4B2;border-radius:0 0 60% 40%;opacity:.9;}
.shape-tr2{position:absolute;top:-20px;left:20px;width:160px;height:120px;background:#fff;border-radius:0 0 60% 40%;}
.shape-tr3{position:absolute;top:0;left:30px;width:130px;height:90px;background:#2DC4B2;border-radius:0 0 50% 50%;opacity:.5;}
.shape-tl{position:absolute;top:-40px;right:-40px;width:220px;height:200px;background:#F0C040;border-radius:40% 0 40% 60%;opacity:.85;}
.shape-tl2{position:absolute;top:-20px;right:-20px;width:180px;height:160px;background:#fff;border-radius:40% 0 40% 60%;}
.shape-tl3{position:absolute;top:10px;right:10px;width:140px;height:120px;background:#F0C040;border-radius:40% 0 40% 60%;opacity:.4;}
.shape-bl{position:absolute;bottom:-40px;left:-50px;width:200px;height:180px;background:#1a237e;border-radius:50%;opacity:.9;}
.shape-bl2{position:absolute;bottom:-20px;left:20px;width:160px;height:140px;background:#006C35;border-radius:50%;opacity:.7;}
.shape-bl3{position:absolute;bottom:10px;left:30px;width:120px;height:100px;background:#2DC4B2;border-radius:50%;opacity:.6;}
.shape-br{position:absolute;bottom:-30px;right:-30px;width:220px;height:180px;background:#E8654A;border-radius:60% 0 0 40%;opacity:.9;}
.shape-br2{position:absolute;bottom:20px;right:20px;width:100px;height:80px;background:#F0C040;border-radius:50%;opacity:.6;}
.triangles{position:absolute;top:28px;left:50%;transform:translateX(-50%);display:flex;gap:3px;}
.tri{width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:12px solid #E8654A;}
.tri.gold{border-bottom-color:#F0C040;}
.tri.sm{border-left-width:5px;border-right-width:5px;border-bottom-width:9px;}
.dots-tr{position:absolute;top:60px;left:28px;display:grid;grid-template-columns:repeat(5,8px);gap:4px;}
.dot-sm{width:5px;height:5px;border-radius:50%;background:#1a237e;opacity:.5;}
.dots-br{position:absolute;bottom:50px;right:40px;display:grid;grid-template-columns:repeat(6,8px);gap:4px;}
.dot-sm2{width:5px;height:5px;border-radius:50%;background:#fff;opacity:.7;}
.cert-content{position:relative;z-index:10;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 80px;text-align:center;}
.cert-main-title{font-family:'Tajawal',sans-serif;font-size:52px;font-weight:900;color:#1a237e;margin-bottom:8px;line-height:1;}
.cert-presented{font-size:12px;color:#888;margin-bottom:4px;letter-spacing:1px;}
.cert-name{font-family:'Scheherazade New',serif;font-size:34px;font-weight:700;color:#E8654A;margin-bottom:8px;}
.cert-desc{font-size:13px;color:#555;line-height:1.8;margin-bottom:20px;}
.cert-subject{color:#006C35;font-weight:700;}
.cert-footer{display:flex;align-items:center;gap:40px;margin-top:4px;}
.cert-sig{text-align:center;}
.cert-sig-line{width:100px;height:1px;background:#ccc;margin-bottom:4px;}
.cert-sig-lbl{font-size:10px;color:#E8654A;letter-spacing:1px;margin-bottom:2px;}
.cert-sig-name{font-size:11px;color:#555;}
.cert-medal-circle{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#F0C040,#C9A84C);border:3px solid #E8654A;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 4px 12px rgba(201,168,76,.4);}
</style>
</head>
<body>
<div class="cert">
  <div class="shape-tr"></div><div class="shape-tr2"></div><div class="shape-tr3"></div>
  <div class="shape-tl"></div><div class="shape-tl2"></div><div class="shape-tl3"></div>
  <div class="shape-bl"></div><div class="shape-bl2"></div><div class="shape-bl3"></div>
  <div class="shape-br"></div><div class="shape-br2"></div>
  <div class="triangles">
    <div class="tri sm gold"></div><div class="tri sm gold"></div><div class="tri gold"></div>
    <div class="tri"></div><div class="tri"></div><div class="tri"></div>
    <div class="tri gold"></div><div class="tri sm gold"></div><div class="tri sm gold"></div>
  </div>
  <div class="dots-tr">${'<div class="dot-sm"></div>'.repeat(15)}</div>
  <div class="dots-br">${'<div class="dot-sm2"></div>'.repeat(12)}</div>
  <div class="cert-content">
    <div class="cert-main-title">شهادة تقدير</div>
    <div class="cert-presented">تُمنح للطالب المتفوق</div>
    <div class="cert-name">${studentName}</div>
    <div class="cert-desc">
      بحصوله على <strong>العلامة الكاملة</strong> في<br/>
      <span class="cert-subject">${colName} — ${subject}</span><br/>
      ${gradeName} / ${className} — ${semester} ${year}
    </div>
    <div class="cert-footer">
      <div class="cert-sig">
        <div class="cert-sig-lbl">التوقيع</div>
        <div class="cert-sig-line"></div>
        <div class="cert-sig-name">أ. ${teacherName}</div>
      </div>
      <div class="cert-medal-circle">⭐</div>
      <div class="cert-sig">
        <div class="cert-sig-lbl">التاريخ</div>
        <div class="cert-sig-line"></div>
        <div class="cert-sig-name">${today}</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>`;
}

async function downloadCertificate(studentId, studentName){
  if(!_tsSelectedCol){toast('❌ اختر نوع التقييم أولاً',true);return;}
  closeTopStudents();
  await new Promise(r=>setTimeout(r,300));
  toast('⏳ جاري إنشاء الشهادة...');

  const certHTML=generateCertHTML(studentName,_tsSelectedCol.name,activeGradesClass);
  const iframe=document.createElement('iframe');
  iframe.style.cssText='position:fixed;left:-9999px;top:0;width:700px;height:490px;border:none;';
  document.body.appendChild(iframe);
  iframe.contentDocument.open();
  iframe.contentDocument.write(certHTML);
  iframe.contentDocument.close();
  await new Promise(r=>setTimeout(r,1500));

  try{
    if(typeof html2canvas==='undefined'){
      await new Promise((res,rej)=>{
        const s=document.createElement('script');
        s.src='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
        s.onload=res; s.onerror=rej;
        document.head.appendChild(s);
      });
    }
    const certEl=iframe.contentDocument.querySelector('.cert');
    const canvas=await html2canvas(certEl,{scale:2,useCORS:true,allowTaint:true,backgroundColor:'#ffffff',width:700,height:490});
    const imgSrc=canvas.toDataURL('image/png');
    const isMobile=/iPhone|iPad|Android/i.test(navigator.userAgent);
    const canShare=navigator.share&&isMobile;

    const modal=document.createElement('div');
    modal.className='cert-preview-modal';
    modal.innerHTML=`
      <div class="cert-preview-card">
        <img src="${imgSrc}" alt="شهادة ${studentName}" style="max-width:100%;border-radius:12px;display:block;margin:0 auto;"/>
        <div style="display:flex;gap:10px;justify-content:center;margin-top:14px;flex-wrap:wrap;">
          ${canShare
            ? `<button onclick="shareCert('${imgSrc}','${studentName}')" style="padding:11px 24px;border-radius:99px;border:none;background:linear-gradient(135deg,#25D366,#128C7E);color:#fff;font-family:'Cairo',sans-serif;font-size:13px;font-weight:700;cursor:pointer;">📤 مشاركة</button>`
            : `<button onclick="downloadCertImg('${imgSrc}','${studentName}')" style="padding:11px 24px;border-radius:99px;border:none;background:linear-gradient(135deg,#1a237e,#283593);color:#fff;font-family:'Cairo',sans-serif;font-size:13px;font-weight:700;cursor:pointer;">⬇️ تحميل</button>`
          }
          <button onclick="this.closest('.cert-preview-modal').remove()" style="padding:11px 24px;border-radius:99px;border:none;background:#3a2020;color:#f5f0e8;font-family:'Cairo',sans-serif;font-size:13px;font-weight:700;cursor:pointer;">✕ إغلاق</button>
        </div>
        ${isMobile&&!canShare?'<div style="color:#a08878;font-size:11px;margin-top:10px;">اضغط مطولاً على الصورة لحفظها في المعرض</div>':''}
      </div>
    `;
    document.body.appendChild(modal);
    toast('✅ الشهادة جاهزة','ok');
  }catch(e){
    toast('❌ حدث خطأ: '+e.message,true);
  }finally{
    document.body.removeChild(iframe);
  }
}

function downloadCertImg(imgSrc, studentName){
  const link=document.createElement('a');
  link.download='شهادة-'+studentName+'.png';
  link.href=imgSrc;
  link.click();
}

async function shareCert(imgSrc, studentName){
  try{
    const res=await fetch(imgSrc);
    const blob=await res.blob();
    const file=new File([blob],'شهادة-'+studentName+'.png',{type:'image/png'});
    await navigator.share({files:[file],title:'شهادة تقدير - '+studentName});
  }catch(e){
    toast('❌ تعذرت المشاركة',true);
  }
}

async function exportAllCertificates(){
  if(!_tsSelectedCol)return;
  const sList=getUnifiedStudents(activeGradesClass);
  const gradeData=grades[activeGradesClass]||{};
  const topStudents=sList.filter(s=>{
    const val=gradeData[s.id]?.[_tsSelectedCol.id];
    return val!=null&&!isNaN(val)&&Number(val)===Number(_tsSelectedCol.max);
  });
  if(!topStudents.length)return;
  // فتح شهادة كل طالب واحدة تلو الأخرى
  for(let i=0;i<topStudents.length;i++){
    await downloadCertificate(topStudents[i].id, topStudents[i].name);
    if(i<topStudents.length-1)await new Promise(r=>setTimeout(r,500));
  }
}


// ══ STUDENTS MANAGER (موحّد بين الدرجات والسلوك) ═══════
let _smgrClassKey=null;
let _smgrContext='grades'; // 'grades' أو 'behavior'

// ─── فحص الشعب الناقصة لشارة "إكمال الإعداد" ───
function checkIncompleteSetup(){
  if(!teacherConfig||!teacherConfig.grades||!teacherConfig.setupDone)return;
  if(isAdmin())return; // المشرف لا يحتاج هذا
  const allCls=getAllClasses();
  const missingClasses=allCls.filter(c=>{
    const list=students[c.id]||behaviorStudents[c.id]||[];
    return !list.length;
  });
  
  const userToggle=document.getElementById('user-toggle');
  const menuItem=document.getElementById('complete-setup-item');
  
  // حذف الشارة القديمة
  const oldBadge=document.getElementById('setup-incomplete-badge');
  if(oldBadge)oldBadge.remove();
  
  if(missingClasses.length){
    // شارة دائمة على زر الحساب
    if(userToggle){
      const badge=document.createElement('span');
      badge.className='setup-incomplete-badge';
      badge.id='setup-incomplete-badge';
      badge.title=`${missingClasses.length} شعبة بحاجة لإكمال`;
      userToggle.appendChild(badge);
    }
    // خانة في القائمة
    if(menuItem){
      menuItem.style.display='block';
      menuItem.textContent=`📋 إكمال الإعداد (${missingClasses.length} شعبة)`;
    }
  }else{
    // اكتمل الإعداد — أخفِ كل شيء نهائياً
    if(menuItem)menuItem.style.display='none';
  }
}

// ─── فتح مودال إكمال الإعداد ───
function openCompleteStudentsSetup(){
  document.getElementById('user-menu').classList.remove('show');
  const allCls=getAllClasses();
  const missingClasses=allCls.filter(c=>{
    const list=students[c.id]||behaviorStudents[c.id]||[];
    return !list.length;
  });
  if(!missingClasses.length){
    toast('✅ جميع الشعب مكتملة!','ok');
    return;
  }
  
  // فتح مودال إكمال الإعداد
  const modal=document.getElementById('complete-setup-modal');
  if(!modal)return;
  
  // بناء قائمة الشعب الناقصة
  const list=document.getElementById('cs-classes-list');
  list.innerHTML=missingClasses.map(c=>`
    <div class="setup-class-row" id="cs-row-${c.id}">
      <div class="scr-name">📚 ${escHtml(c.gradeName)} — ${escHtml(c.name)}</div>
      <span class="scr-status empty" id="cs-status-${c.id}">⚠️ فارغة</span>
      <div class="scr-actions">
        <label class="scr-upload">
          📂 رفع Excel
          <input type="file" accept=".xlsx,.xls,.csv" style="display:none" onchange="uploadCompleteSetupExcel(event,'${c.id}')"/>
        </label>
      </div>
    </div>
  `).join('');
  
  modal.style.display='flex';
}

async function uploadCompleteSetupExcel(event, classId){
  const file=event.target.files[0];
  if(!file)return;
  event.target.value='';
  toast('⏳ جاري قراءة الملف...');
  
  if(!window.XLSX){
    const s=document.createElement('script');
    s.src='https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
    document.head.appendChild(s);
    await new Promise(r=>s.onload=r);
  }
  
  const reader=new FileReader();
  reader.onload=e=>{
    try{
      const wb=XLSX.read(e.target.result,{type:'binary'});
      const ws=wb.Sheets[wb.SheetNames[0]];
      const rows=XLSX.utils.sheet_to_json(ws,{header:1});
      if(!rows.length){toast('❌ الملف فارغ',true);return;}
      
      const nameKW=['اسم الطالب','الاسم','اسم','student','name','طالب','أسماء'];
      const phoneKW=['الهاتف النقال','هاتف ولي','ولي الأمر','هاتف','جوال','رقم','phone','mobile'];
      let nameCol=-1,phoneCol=-1,headerRow=0;
      
      // المرور الأول: صف يحتوي الاسم والهاتف معاً
      for(let ri=0;ri<Math.min(50,rows.length);ri++){
        const row=rows[ri]||[];
        let fn=-1,fp=-1;
        row.forEach((cell,ci)=>{
          const v=String(cell||'').trim().replace(/ـ/g,'').toLowerCase();
          if(fn<0&&nameKW.some(kw=>v.includes(kw)))fn=ci;
          if(fp<0&&phoneKW.some(kw=>v.includes(kw)))fp=ci;
        });
        if(fn>=0&&fp>=0){nameCol=fn;phoneCol=fp;headerRow=ri;break;}
      }
      // المرور الثاني: أحدهما فقط
      if(nameCol<0){
        for(let ri=0;ri<Math.min(50,rows.length);ri++){
          const row=rows[ri]||[];
          row.forEach((cell,ci)=>{
            const v=String(cell||'').trim().replace(/ـ/g,'').toLowerCase();
            if(nameCol<0&&nameKW.some(kw=>v.includes(kw))){nameCol=ci;headerRow=ri;}
            if(phoneCol<0&&phoneKW.some(kw=>v.includes(kw)))phoneCol=ci;
          });
          if(nameCol>=0)break;
        }
      }
      
      if(nameCol<0){toast('❌ لم يتم التعرف على عمود الاسم',true);return;}
      
      const studentsList=[];
      rows.slice(headerRow+1).forEach(r=>{
        if(!r)return;
        const name=String(r[nameCol]||'').trim();
        const phone=phoneCol>=0?String(r[phoneCol]||'').trim():'';
        if(name&&name.length>1&&!/^\d+$/.test(name)&&!nameKW.some(kw=>name.toLowerCase().replace(/ـ/g,'').includes(kw))){
          studentsList.push({
            id:'s_'+Date.now()+'_'+Math.random().toString(36).slice(2,7),
            name, phone
          });
        }
      });
      
      if(!studentsList.length){toast('❌ لم يتم العثور على طلاب',true);return;}
      
      // ترتيب أبجدي وحفظ
      studentsList.sort((a,b)=>a.name.localeCompare(b.name,'ar'));
      syncStudentsToBoth(classId, studentsList);
      
      // تحديث واجهة المودال
      const row=document.getElementById(`cs-row-${classId}`);
      const status=document.getElementById(`cs-status-${classId}`);
      if(row)row.className='setup-class-row has-students';
      if(status){status.className='scr-status filled';status.textContent=`✓ ${studentsList.length} طالب`;}
      
      toast(`✅ تم إضافة ${studentsList.length} طالب`,'ok');
      
      // فحص إذا اكتملت جميع الشعب
      setTimeout(()=>checkIncompleteSetup(),500);
    }catch(err){
      toast('❌ خطأ: '+err.message,true);
    }
  };
  reader.readAsBinaryString(file);
}

function openStudentsManager(classKey, context='grades'){
  _smgrClassKey=classKey;
  _smgrContext=context;
  if(!classKey){toast('❌ اختر شعبة أولاً',true);return;}
  
  // اسم الشعبة
  let className='الشعبة';
  if(context==='grades'){
    const allCls=getAllClasses();
    const cls=allCls.find(c=>c.id===classKey);
    if(cls)className=cls.name;
  }else{
    const allCls=getAllClasses();
    const cls=allCls.find(c=>c.id===classKey);
    if(cls)className=cls.name;
  }
  document.getElementById('smgr-title').textContent=`🖊️ تعديل قائمة طلاب — ${className}`;
  document.getElementById('smgr-search').value='';
  document.getElementById('smgr-new-name').value='';
  document.getElementById('smgr-new-phone').value='';
  document.getElementById('students-mgr-modal').style.display='flex';
  renderStudentsManagerList();
}

function closeStudentsManager(){
  document.getElementById('students-mgr-modal').style.display='none';
  // تحديث القسمين بعد الإغلاق
  if(typeof renderGradesTable==='function')renderGradesTable();
  if(typeof renderBehaviorTable==='function')renderBehaviorTable();
  // إعادة فحص الشعب الناقصة
  checkIncompleteSetup();
}

function getUnifiedStudents(classKey){
  // دمج طلاب الدرجات والسلوك (الاسم + الهاتف)
  const fromGrades=(students[classKey]||[]).map(s=>({...s, phone: s.phone||''}));
  const fromBehavior=behaviorStudents[classKey]||[];
  
  // ابدأ من الدرجات، ثم أضف الهواتف من السلوك بالاسم
  const merged=fromGrades.map(s=>{
    const bMatch=fromBehavior.find(b=>b.name===s.name);
    return{...s, phone: s.phone||bMatch?.phone||''};
  });
  
  // أضف من السلوك إذا لم يكونوا في الدرجات
  fromBehavior.forEach(b=>{
    if(!merged.find(m=>m.name===b.name)){
      merged.push({id:b.id, name:b.name, phone:b.phone||''});
    }
  });
  
  return merged;
}

function sortStudentsAr(list){
  // ترتيب أبجدي بالاسم ثم اسم الأب
  return [...list].sort((a,b)=>{
    const aName=(a.name||'').trim();
    const bName=(b.name||'').trim();
    return aName.localeCompare(bName,'ar');
  });
}

function syncStudentsToBoth(classKey, unifiedList){
  // كتابة على students (للدرجات)
  students[classKey]=unifiedList.map(s=>({id:s.id, name:s.name, phone:s.phone||''}));
  // كتابة على behaviorStudents (للسلوك)
  if(!behaviorStudents[classKey])behaviorStudents[classKey]=[];
  behaviorStudents[classKey]=unifiedList.map(s=>({id:s.id, name:s.name, phone:s.phone||''}));
  scheduleSave();
}

function renderStudentsManagerList(){
  const listEl=document.getElementById('smgr-list');
  const search=(document.getElementById('smgr-search').value||'').trim();
  let list=getUnifiedStudents(_smgrClassKey);
  list=sortStudentsAr(list);
  if(search){
    list=list.filter(s=>s.name.includes(search)||(s.phone||'').includes(search));
  }
  if(!list.length){
    listEl.innerHTML='<div class="smgr-empty">📭 لا يوجد طلاب — أضف من الأعلى</div>';
    return;
  }
  listEl.innerHTML=list.map((s,i)=>`
    <div class="smgr-item">
      <div class="smgr-num">${i+1}</div>
      <div class="smgr-name">${escHtml(s.name)}</div>
      ${s.phone?`<div class="smgr-phone">${escHtml(s.phone)}</div>`:''}
      <button class="smgr-del" onclick="deleteStudentFromList('${s.id}')">🗑️</button>
    </div>
  `).join('');
}

function addStudentManually(){
  const name=document.getElementById('smgr-new-name').value.trim();
  const phone=document.getElementById('smgr-new-phone').value.trim();
  if(!name){toast('❌ اكتب اسم الطالب',true);return;}
  
  let unified=getUnifiedStudents(_smgrClassKey);
  // تحقق من التكرار
  if(unified.some(s=>s.name===name)){
    toast('❌ هذا الطالب موجود بالفعل',true);
    return;
  }
  unified.push({
    id:'s_'+Date.now()+'_'+Math.random().toString(36).slice(2,7),
    name, phone
  });
  unified=sortStudentsAr(unified);
  syncStudentsToBoth(_smgrClassKey, unified);
  
  document.getElementById('smgr-new-name').value='';
  document.getElementById('smgr-new-phone').value='';
  renderStudentsManagerList();
  toast('✅ تم إضافة الطالب','ok');
}

function deleteStudentFromList(studentId){
  let unified=getUnifiedStudents(_smgrClassKey);
  const student=unified.find(s=>s.id===studentId);
  if(!student)return;
  if(!confirm(`هل تريد حذف الطالب "${student.name}"؟`))return;
  
  unified=unified.filter(s=>s.id!==studentId);
  syncStudentsToBoth(_smgrClassKey, unified);
  
  // حذف درجاته ومخالفاته أيضاً
  if(grades[_smgrClassKey]&&grades[_smgrClassKey][studentId]){
    delete grades[_smgrClassKey][studentId];
  }
  if(behaviorViolations&&behaviorViolations[studentId]){
    delete behaviorViolations[studentId];
  }
  scheduleSave();
  
  renderStudentsManagerList();
  toast('✅ تم حذف الطالب','ok');
}

// ─── إرسال درجات الطالب عبر واتساب ───
function sendStudentGradesWA(studentId, classKey){
  const student=(behaviorStudents[classKey]||[]).find(s=>s.id===studentId)
              ||(students[classKey]||[]).find(s=>s.id===studentId);
  if(!student){toast('❌ لم يتم العثور على الطالب',true);return;}
  if(!student.phone){toast('❌ لا يوجد رقم لولي الأمر',true);return;}
  
  // جلب معلومات الشعبة
  const info=getClassInfoById(classKey);
  if(!info){toast('❌ خطأ في معلومات الشعبة',true);return;}
  
  // جلب الدرجات
  const cols=gradeTypes.filter(c=>c.classKey===classKey);
  const studentGrades=(grades[classKey]||{})[studentId]||{};
  
  // بناء الرسالة
  const semesterName=teacherConfig?.semester||'الفصل';
  let msg=`🎓 *تقرير درجات الطالب*\n\n`;
  msg+=`📌 *الاسم:* ${student.name}\n`;
  msg+=`📚 *المادة:* ${info.subject}\n`;
  msg+=`🏫 *الصف:* ${info.className}\n`;
  msg+=`📅 *${semesterName}*\n\n`;
  msg+=`━━━━━━━━━━━━━━\n`;
  msg+=`📊 *الدرجات:*\n\n`;
  
  if(!cols.length){
    msg+=`(لا توجد تقييمات مسجّلة بعد)\n`;
  }else{
    let totalPts=0, totalMax=0, hasAnyGrade=false;
    cols.forEach(c=>{
      const val=studentGrades[c.id];
      if(val!=null&&val!==''&&!isNaN(val)){
        msg+=`• ${c.name}: *${val}/${c.max}*\n`;
        totalPts+=Number(val);
        totalMax+=Number(c.max);
        hasAnyGrade=true;
      }else{
        msg+=`• ${c.name}: _لم يُقيَّم بعد_\n`;
      }
    });
    
    if(hasAnyGrade){
      const pct=totalMax>0?Math.round(totalPts/totalMax*100):0;
      msg+=`\n━━━━━━━━━━━━━━\n`;
      msg+=`📈 *المجموع: ${totalPts}/${totalMax} (${pct}%)*\n`;
    }
  }
  
  // اسم المعلم
  const teacherName=teacherConfig?.display_name||teacherConfig?.teacher_name||'';
  if(teacherName){
    msg+=`\nتحياتي،\nأ. ${teacherName}`;
  }
  
  // فتح واتساب
  const phone=normalizePhone(student.phone);
  if(!phone){toast('❌ رقم ولي الأمر غير صحيح',true);return;}
  
  const encodedMsg=encodeURIComponent(msg);
  const isMobile=/Android|iPhone|iPad/i.test(navigator.userAgent);
  const url=isMobile
    ?`https://wa.me/${phone}?text=${encodedMsg}`
    :`https://web.whatsapp.com/send?phone=${phone}&text=${encodedMsg}`;
  window.open(url,'_blank');
}

function getClassInfoById(classKey){
  if(!teacherConfig||!teacherConfig.grades)return null;
  for(const g of teacherConfig.grades){
    const cls=(g.classes||[]).find(c=>c.id===classKey);
    if(cls)return{subject:g.subject, grade:g.num, className:cls.name};
  }
  return null;
}

// (normalizePhone موجودة أعلاه)

// ══ INVITES ═════════════════════════════════════════════

function generateInviteCode(){
  const chars='ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
  return Array.from({length:8},()=>chars[Math.floor(Math.random()*chars.length)]).join('');
}

async function createInvite(){
  if(!isAdmin())return;
  try{
    const code=generateInviteCode();
    const expiresAt=new Date(Date.now()+24*60*60*1000).toISOString();
    const{error}=await sb.from('invites').insert({code,expires_at:expiresAt,status:'pending'});
    if(error)throw error;
    toast('✅ تم إنشاء رابط الدعوة!','ok');
    loadInvites();
  }catch(e){toast('❌ خطأ: '+e.message,true);}
}

async function loadInvites(){
  if(!isAdmin())return;
  const list=document.getElementById('invites-list');
  if(!list)return;
  try{
    const{data,error}=await sb.from('invites').select('*').order('created_at',{ascending:false}).limit(20);
    if(error)throw error;

    // تحديث الحالة: انتهت صلاحيتها
    const now=new Date();
    const expired=(data||[]).filter(i=>i.status==='pending'&&new Date(i.expires_at)<now);
    if(expired.length){
      await Promise.all(expired.map(i=>sb.from('invites').update({status:'expired'}).eq('id',i.id)));
      expired.forEach(i=>i.status='expired');
    }

    if(!data||!data.length){
      list.innerHTML='<div style="text-align:center;padding:10px;color:var(--muted);font-size:12px">لا توجد دعوات بعد</div>';
      return;
    }

    list.innerHTML=data.map(inv=>{
      const link=`${location.origin}${location.pathname}?invite=${inv.code}`;
      const expDate=new Date(inv.expires_at).toLocaleString('ar');
      const statusLabel={pending:'متاح ✅',used:'مستخدم 👤',cancelled:'ملغى ❌',expired:'منتهي ⏰'}[inv.status]||inv.status;
      const isPending=inv.status==='pending';
      return `<div class="invite-card">
        <div style="flex:1;min-width:0;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap;">
            <span class="invite-status ${inv.status}">${statusLabel}</span>
            ${inv.used_by?`<span style="font-size:11px;color:var(--muted)">→ ${escHtml(inv.used_by)}</span>`:''}
          </div>
          <div class="invite-code">${link}</div>
          <div class="invite-meta" style="margin-top:4px;">
            ${isPending?`⏰ ينتهي: ${expDate}`:`📅 أُنشئ: ${new Date(inv.created_at).toLocaleString('ar')}`}
          </div>
        </div>
        <div class="invite-actions">
          ${isPending?`<button class="invite-copy-btn" onclick="copyInviteLink('${link}')">📋 نسخ</button>`:''}
          ${isPending?`<button class="invite-cancel-btn" onclick="cancelInvite('${inv.id}')">إلغاء</button>`:''}
        </div>
      </div>`;
    }).join('');
  }catch(e){
    list.innerHTML='<div style="color:var(--red);font-size:12px;padding:8px">❌ خطأ في التحميل</div>';
  }
}

function copyInviteLink(link){
  navigator.clipboard.writeText(link).then(()=>{
    toast('✅ تم نسخ الرابط!','ok');
  }).catch(()=>{
    // fallback
    const ta=document.createElement('textarea');
    ta.value=link;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    toast('✅ تم نسخ الرابط!','ok');
  });
}

async function cancelInvite(id){
  if(!confirm('هل تريد إلغاء هذه الدعوة؟'))return;
  try{
    const{error}=await sb.from('invites').update({status:'cancelled'}).eq('id',id);
    if(error)throw error;
    toast('✅ تم إلغاء الدعوة','ok');
    loadInvites();
  }catch(e){toast('❌ خطأ: '+e.message,true);}
}

async function handleInviteOnBoot(code, email){
  try{
    const{data,error}=await sb.from('invites').select('*').eq('code',code).maybeSingle();
    if(error||!data)return false;
    if(data.status!=='pending')return false;
    if(new Date(data.expires_at)<new Date()){
      await sb.from('invites').update({status:'expired'}).eq('id',data.id);
      return false;
    }
    // إضافة البريد لـ allowed_emails
    const{data:existing}=await sb.from('allowed_emails').select('email').eq('email',email).maybeSingle();
    if(!existing){
      await sb.from('allowed_emails').insert({email});
    }
    // تحديث حالة الدعوة
    await sb.from('invites').update({
      status:'used',used_by:email,used_at:new Date().toISOString()
    }).eq('id',data.id);
    // إزالة الكود من الرابط
    history.replaceState({},'',location.pathname);
    return true;
  }catch(e){
    console.warn('handleInviteOnBoot error:',e);
    return false;
  }
}

async function checkInviteCode(){
  const params=new URLSearchParams(location.search);
  const code=params.get('invite');
  if(!code||!currentUser)return;
  try{
    const{data,error}=await sb.from('invites').select('*').eq('code',code).maybeSingle();
    if(error||!data)return;
    if(data.status!=='pending'){
      toast('❌ هذا الرابط '+(data.status==='used'?'مستخدم مسبقاً':'منتهي الصلاحية'),true);
      return;
    }
    if(new Date(data.expires_at)<new Date()){
      await sb.from('invites').update({status:'expired'}).eq('id',data.id);
      toast('❌ انتهت صلاحية هذا الرابط',true);
      return;
    }
    // إضافة البريد لـ allowed_emails
    const email=currentUser.email;
    const{data:existing}=await sb.from('allowed_emails').select('email').eq('email',email).maybeSingle();
    if(!existing){
      await sb.from('allowed_emails').insert({email});
    }
    // تحديث حالة الدعوة
    await sb.from('invites').update({status:'used',used_by:email,used_at:new Date().toISOString()}).eq('id',data.id);
    // إزالة الكود من الرابط
    history.replaceState({},'',location.pathname);
    toast('✅ تم تفعيل حسابك! مرحباً 🎉','ok');
  }catch(e){console.warn('invite check error:',e);}
}

// ══ NETWORK STATUS ═════════════════════════════════════
function updateOnlineStatus(){
  const banner=document.getElementById('offline-banner');
  if(!banner)return;
  if(navigator.onLine){
    banner.classList.remove('show');
  }else{
    banner.classList.add('show');
  }
}

function retryConnection(){
  if(navigator.onLine){
    document.getElementById('offline-banner').classList.remove('show');
    toast('✅ الاتصال يعمل بشكل طبيعي');
    // إعادة حفظ إذا كان هناك تغييرات معلقة
    scheduleSave();
  }else{
    toast('📵 لا يزال لا يوجد اتصال',true);
  }
}

window.addEventListener('online', ()=>{
  updateOnlineStatus();
  toast('✅ عاد الاتصال بالإنترنت');
  scheduleSave();
});
window.addEventListener('offline', ()=>{
  updateOnlineStatus();
  toast('📵 انقطع الاتصال بالإنترنت',true);
});

// ══ SURVEYS ════════════════════════════════════════════
let _surveyQuestions=[];
let _activeSurvey=null;
let _surveyAnswers={};

// ─── بناء الاستبيان ───
function addOptField(){
  const wrap=document.getElementById('new-q-opts');
  const div=document.createElement('div');
  div.className='survey-opt-inp';
  const n=wrap.querySelectorAll('.new-opt-inp').length+1;
  div.innerHTML=`<input placeholder="خيار ${n}" class="new-opt-inp"/><button class="survey-opt-del" onclick="removeOpt(this)">✕</button>`;
  wrap.appendChild(div);
}

function removeOpt(btn){
  const wrap=btn.closest('.survey-opts-wrap')||btn.closest('.survey-opt-inp').parentElement;
  if(wrap.querySelectorAll('.survey-opt-inp').length>2){btn.closest('.survey-opt-inp').remove();}
  else toast('❌ يجب وجود خيارين على الأقل',true);
}

function addQuestion(){
  const text=document.getElementById('new-q-text').value.trim();
  if(!text){toast('❌ اكتب نص السؤال أولاً',true);return;}
  const opts=[...document.querySelectorAll('.new-opt-inp')].map(i=>i.value.trim()).filter(v=>v);
  if(opts.length<2){toast('❌ أضف خيارين على الأقل',true);return;}
  _surveyQuestions.push({id:'q_'+Date.now(),text,options:opts});
  renderSurveyBuilder();
  // إعادة تعيين الحقول
  document.getElementById('new-q-text').value='';
  document.querySelectorAll('.new-opt-inp').forEach((inp,i)=>{inp.value='';});
  toast('✅ تم إضافة السؤال');
}

function removeQuestion(idx){
  _surveyQuestions.splice(idx,1);
  renderSurveyBuilder();
}

function renderSurveyBuilder(){
  const list=document.getElementById('survey-q-list');
  if(!list)return;
  if(!_surveyQuestions.length){list.innerHTML='';return;}
  list.innerHTML=_surveyQuestions.map((q,i)=>`
    <div class="survey-q-item">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div class="survey-q-text">${i+1}. ${escHtml(q.text)}</div>
        <button onclick="removeQuestion(${i})" style="background:none;border:none;color:var(--muted);cursor:pointer;font-size:14px;padding:0">✕</button>
      </div>
      <div class="survey-q-options">${q.options.map(o=>`<span class="survey-q-opt">${escHtml(o)}</span>`).join('')}</div>
    </div>
  `).join('');
}

function clearSurveyBuilder(){
  if(!confirm('هل تريد مسح الاستبيان الحالي؟'))return;
  _surveyQuestions=[];
  document.getElementById('survey-title').value='';
  renderSurveyBuilder();
}

// ─── نشر الاستبيان ───
async function publishSurvey(){
  const title=document.getElementById('survey-title').value.trim();
  if(!title){toast('❌ اكتب عنوان الاستبيان',true);return;}
  if(!_surveyQuestions.length){toast('❌ أضف سؤالاً واحداً على الأقل',true);return;}
  try{
    // إلغاء تفعيل الاستبيانات السابقة
    await sb.from('surveys').update({is_active:false}).eq('is_active',true);
    // نشر الاستبيان الجديد
    const{error}=await sb.from('surveys').insert({
      title,
      questions:_surveyQuestions,
      is_active:true
    });
    if(error)throw error;
    toast('✅ تم نشر الاستبيان للمعلمين!');
    _surveyQuestions=[];
    document.getElementById('survey-title').value='';
    renderSurveyBuilder();
    loadSurveyResults();
  }catch(e){toast('❌ خطأ: '+e.message,true);}
}

// ─── إحصائيات الاستبيان ───
async function loadSurveyResults(){
  const wrap=document.getElementById('survey-results-wrap');
  if(!wrap)return;
  try{
    const{data:surveys}=await sb.from('surveys').select('*').order('created_at',{ascending:false}).limit(5);
    if(!surveys||!surveys.length){wrap.innerHTML='<div style="text-align:center;color:var(--muted);padding:20px;font-size:13px">لا توجد استبيانات منشورة بعد</div>';return;}

    let html='<div class="survey-results"><h4>📊 نتائج الاستبيانات</h4>';
    for(const survey of surveys){
      const{data:responses}=await sb.from('survey_responses').select('answers').eq('survey_id',survey.id);
      const resCount=responses?.length||0;
      html+=`<div style="margin-bottom:24px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;flex-wrap:wrap;gap:8px;">
          <div>
            <div style="font-size:14px;font-weight:700;color:var(--text)">${escHtml(survey.title)}</div>
            <div style="font-size:11px;color:var(--muted);margin-top:2px">${resCount} إجابة ${survey.is_active?'<span style="color:var(--green2)">● نشط</span>':'<span style="color:var(--muted)">● منتهي</span>'}</div>
          </div>
          <div style="display:flex;gap:8px;">
            ${!survey.is_active?`<button onclick="reactivateSurvey('${survey.id}')" style="background:rgba(0,108,53,.15);border:1px solid var(--green);color:var(--green2);border-radius:8px;padding:5px 12px;font-size:11px;cursor:pointer;font-family:'Cairo',sans-serif;">▶️ إعادة تفعيل</button>`:''}
            <button onclick="deactivateSurvey('${survey.id}')" style="background:rgba(192,57,43,.1);border:1px solid var(--red);color:var(--red2);border-radius:8px;padding:5px 12px;font-size:11px;cursor:pointer;font-family:'Cairo',sans-serif;">⏹️ إيقاف</button>
          </div>
        </div>`;

      if(resCount>0){
        const questions=survey.questions||[];
        questions.forEach(q=>{
          const counts={};
          q.options.forEach(o=>counts[o]=0);
          responses.forEach(r=>{const ans=r.answers[q.id];if(ans&&counts[ans]!==undefined)counts[ans]++;});
          html+=`<div class="result-q">
            <div class="result-q-title">${escHtml(q.text)}</div>
            <div class="result-bar-wrap">
              ${q.options.map(o=>{
                const cnt=counts[o]||0;
                const pct=resCount>0?Math.round(cnt/resCount*100):0;
                return `<div class="result-bar-row">
                  <div class="result-bar-label">${escHtml(o)}</div>
                  <div class="result-bar"><div class="result-bar-fill" style="width:${pct}%"></div></div>
                  <div class="result-bar-count">${cnt} (${pct}%)</div>
                </div>`;
              }).join('')}
            </div>
          </div>`;
        });
      }else{
        html+=`<div style="font-size:12px;color:var(--muted);padding:10px 0">لا توجد إجابات بعد</div>`;
      }
      html+=`<div style="height:1px;background:var(--border);margin-top:16px;"></div></div>`;
    }
    html+='</div>';
    wrap.innerHTML=html;
  }catch(e){console.warn('survey results error:',e);}
}

async function deactivateSurvey(id){
  await sb.from('surveys').update({is_active:false}).eq('id',id);
  loadSurveyResults();
  toast('✅ تم إيقاف الاستبيان');
}

async function reactivateSurvey(id){
  await sb.from('surveys').update({is_active:false}).eq('is_active',true);
  await sb.from('surveys').update({is_active:true}).eq('id',id);
  loadSurveyResults();
  toast('✅ تم إعادة تفعيل الاستبيان');
}

// ─── عرض الاستبيان للمعلم ───
async function checkActiveSurvey(){
  if(!currentUser)return;
  // المشرف لا يرى الاستبيان
  if(isAdmin())return;
  try{
    const{data:surveys}=await sb.from('surveys').select('*').eq('is_active',true).limit(1);
    if(!surveys||!surveys.length)return;
    const survey=surveys[0];
    // تحقق إذا أجاب المعلم مسبقاً
    const{data:existing}=await sb.from('survey_responses').select('id').eq('survey_id',survey.id).eq('user_id',currentUser.id).maybeSingle();
    if(existing)return;
    // عرض الاستبيان
    _activeSurvey=survey;
    _surveyAnswers={};
    showSurveyModal(survey);
  }catch(e){}
}

function showSurveyModal(survey){
  document.getElementById('survey-modal-title').textContent='📋 '+survey.title;
  const body=document.getElementById('survey-modal-body');
  body.innerHTML=(survey.questions||[]).map(q=>`
    <div class="survey-modal-q">
      <div class="survey-modal-q-title">${escHtml(q.text)}</div>
      <div class="survey-modal-opts">
        ${q.options.map(o=>`
          <label class="survey-modal-opt" id="opt_${q.id}_${escHtml(o).replace(/\s/g,'_')}">
            <input type="radio" name="q_${q.id}" value="${escHtml(o)}" onchange="selectSurveyOpt('${q.id}','${escHtml(o)}',this)"/>
            ${escHtml(o)}
          </label>
        `).join('')}
      </div>
    </div>
  `).join('');
  document.getElementById('survey-modal-bg').style.display='flex';
}

function selectSurveyOpt(qId,val,radio){
  _surveyAnswers[qId]=val;
  // تحديث التصميم
  const allOpts=document.querySelectorAll(`[name="q_${qId}"]`);
  allOpts.forEach(r=>r.closest('.survey-modal-opt').classList.remove('selected'));
  radio.closest('.survey-modal-opt').classList.add('selected');
}

async function submitSurvey(){
  if(!_activeSurvey)return;
  const questions=_activeSurvey.questions||[];
  const unanswered=questions.filter(q=>!_surveyAnswers[q.id]);
  if(unanswered.length){toast(`❌ أجب على جميع الأسئلة (${unanswered.length} متبقية)`,true);return;}
  try{
    const{error}=await sb.from('survey_responses').insert({
      survey_id:_activeSurvey.id,
      user_id:currentUser.id,
      answers:_surveyAnswers
    });
    if(error)throw error;
    document.getElementById('survey-modal-bg').style.display='none';
    toast('✅ شكراً! تم إرسال إجاباتك');
    _activeSurvey=null;
    _surveyAnswers={};
  }catch(e){toast('❌ خطأ: '+e.message,true);}
}

function closeSurveyModal(e){
  if(e&&e.target!==document.getElementById('survey-modal-bg'))return;
  document.getElementById('survey-modal-bg').style.display='none';
}

// ══ CV ════════════════════════════════════════════════
function loadTeacherPhoto(e){
  const file=e.target.files[0];if(!file)return;
  const reader=new FileReader();
  reader.onload=function(ev){
    const src=ev.target.result;
    document.getElementById('cv-photo-img').src=src;
    document.getElementById('cv-photo-img').style.display='block';
    document.getElementById('cv-photo-placeholder').style.display='none';
    if(cvProfile)cvProfile.photo=src;
    saveCvProfile();
    toast('✅ تم حفظ الصورة','ok');
  };
  reader.readAsDataURL(file);
}
function loadCvProfile(){
  if(!cvProfile)return;
  document.getElementById('cv-pname').value=cvProfile.name||'';
  document.getElementById('cv-pschool').value=cvProfile.school||'';
  document.getElementById('cv-psubject').value=cvProfile.subject||teacherConfig?.subject||'';
  document.getElementById('cv-pyears').value=cvProfile.years||'';
  document.getElementById('cv-pbio').value=cvProfile.bio||'';
  // Load photo if saved
  if(cvProfile.photo){
    document.getElementById('cv-photo-img').src=cvProfile.photo;
    document.getElementById('cv-photo-img').style.display='block';
    document.getElementById('cv-photo-placeholder').style.display='none';
  }
}
function saveCvProfile(){
  const photo=cvProfile?.photo||'';
  cvProfile={
    name:document.getElementById('cv-pname').value.trim(),
    school:document.getElementById('cv-pschool').value.trim(),
    subject:document.getElementById('cv-psubject').value.trim(),
    years:document.getElementById('cv-pyears').value,
    bio:document.getElementById('cv-pbio').value.trim(),
    photo,
  };
  toast('✅ تم حفظ النبذة','ok');scheduleSave();
}
let cvPendingFiles=[];
function openCvModal(){document.getElementById('cv-title-inp').value='';document.getElementById('cv-date').value=new Date().toISOString().split('T')[0];document.getElementById('cv-desc').value='';document.getElementById('cv-type').value='achievement';document.getElementById('cv-files-preview').innerHTML='';cvPendingFiles=[];document.getElementById('cv-modal-bg').classList.remove('hidden');}
function closeCvModal(){document.getElementById('cv-modal-bg').classList.add('hidden');cvPendingFiles=[];}
document.getElementById('cv-files-input').addEventListener('change',e=>{Array.from(e.target.files).forEach(f=>{if(f.size>MAX_FILE_SIZE){toast('❌ ملف أكبر من 500 ميجا',true);return;}cvPendingFiles.push(f);});updateCvPreview();e.target.value='';});
function updateCvPreview(){const preview=document.getElementById('cv-files-preview');preview.innerHTML='';cvPendingFiles.forEach((f,i)=>{const row=document.createElement('div');row.style.cssText='display:flex;align-items:center;gap:8px;padding:6px 10px;background:var(--card);border:1px solid var(--border);border-radius:8px;font-size:12px;';row.innerHTML=`<span>${f.type.startsWith('image/')?'🖼️':'📄'}</span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--text)">${f.name}</span><span style="color:var(--muted)">${fmtSize(f.size)}</span><button onclick="removeCvFile(${i})" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:13px;">✕</button>`;preview.appendChild(row);});}
function removeCvFile(i){cvPendingFiles.splice(i,1);updateCvPreview();}
async function saveCvItem(){
  const title=document.getElementById('cv-title-inp').value.trim();if(!title){document.getElementById('cv-title-inp').focus();return;}
  const btn=document.getElementById('cv-save-btn');btn.disabled=true;btn.textContent='جاري...';
  const id=Date.now().toString(),type=document.getElementById('cv-type').value,date=document.getElementById('cv-date').value,desc=document.getElementById('cv-desc').value.trim();
  const attachments=[];
  for(const file of cvPendingFiles){
    const fileName=`[سيرة-${id}] ${file.name}`;
    const result=await driveUpload(file,fileName);
    if(result)attachments.push({name:file.name,type:file.type,size:file.size,driveId:result.id,viewLink:result.viewLink,downloadLink:result.downloadLink,previewLink:result.previewLink});
  }
  cvItems.unshift({id,type,title,date,desc,attachments});closeCvModal();renderCv();toast('✅ تم الحفظ','ok');btn.disabled=false;btn.textContent='حفظ ✅';scheduleSave();
}
function renderCv(){
  const timeline=document.getElementById('cv-timeline');const empty=document.getElementById('cv-empty');
  document.getElementById('cv-count').textContent=cvItems.length+' إنجاز / مبادرة';
  if(!cvItems.length){empty.style.display='block';timeline.innerHTML='';return;}
  empty.style.display='none';timeline.innerHTML='';
  cvItems.forEach(item=>{
    const el=document.createElement('div');el.className='cv-item';
    const ds=item.date?new Date(item.date).toLocaleDateString('ar-SA',{year:'numeric',month:'long',day:'numeric'}):'';
    const tLabel=item.type==='achievement'?'🏆 إنجاز':'🚀 مبادرة';const tClass=item.type==='achievement'?'type-achievement':'type-initiative';
    let filesHtml='';
    if(item.attachments&&item.attachments.length){
      const rows=item.attachments.map(a=>{
        const isImg=a.type&&a.type.startsWith('image/');
        const openUrl=a.previewLink||a.viewLink||'';
        return`<div class="cv-file-row"><span>${isImg?'🖼️':'📄'}</span><span class="cv-file-name">${a.name}</span><span style="font-size:10px;color:var(--muted)">${fmtSize(a.size)}</span><button class="arc-btn" onclick="openDriveFile('${openUrl}','${a.name.replace(/'/g,"\\'")}')" style="padding:3px 8px;font-size:10px;">👁️</button></div>`;
      }).join('');
      filesHtml=`<div class="cv-files"><div class="cv-files-label">📎 المرفقات (${item.attachments.length})</div><div class="cv-files-list">${rows}</div></div>`;
    }
    el.innerHTML=`<div class="cv-item-head"><div class="cv-badge">${item.type==='achievement'?'🏆':'🚀'}</div><div class="cv-item-body"><div class="cv-item-title">${item.title}</div><div class="cv-item-meta">${ds?`<span class="cv-item-date">📅 ${ds}</span>`:''}<span class="cv-item-type ${tClass}">${tLabel}</span></div>${item.desc?`<div class="cv-item-desc">${item.desc}</div>`:''}<div class="cv-item-actions"><button class="arc-btn del" onclick="deleteCvItem('${item.id}')">🗑️ حذف</button></div></div></div>${filesHtml}`;
    timeline.appendChild(el);
  });
}
async function deleteCvItem(id){
  if(!confirm('تأكيد الحذف؟'))return;
  const item=cvItems.find(i=>i.id===id);
  if(item&&item.attachments)for(const a of item.attachments)if(a.driveId)await driveDelete(a.driveId);
  cvItems=cvItems.filter(i=>i.id!==id);renderCv();toast('🗑️ تم الحذف');scheduleSave();
}

// ══ PDF/IMG ════════════════════════════════════════════
function closePdf(){document.getElementById('pdf-modal').classList.add('hidden');document.getElementById('pdf-frame').src='';}
async function viewImg(url){
  const real=resolveLocalUrl(url);
  if(!real){toast('❌ الصورة غير متاحة',true);return;}
  document.getElementById('img-viewer').src=real;
  document.getElementById('img-modal').classList.remove('hidden');
}
function closeImg(){document.getElementById('img-modal').classList.add('hidden');document.getElementById('img-viewer').src='';}

// ══ REMINDERS ══════════════════════════════════════════
function parseTime12(str){if(!str)return null;const m=str.trim().match(/^(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?$/);if(!m)return null;let h=parseInt(m[1]),mn=parseInt(m[2]);const ap=(m[3]||'').toUpperCase();if(ap==='PM'&&h<12)h+=12;if(ap==='AM'&&h===12)h=0;if(!ap&&h<7)h+=12;return h*60+mn;}
function nowMins(){const d=new Date();return d.getHours()*60+d.getMinutes();}
function findCurrentAndNextPeriod(){
  const dayKey=currentDayKey();if(!timetableConfig)return{current:null,next:null};const daySched=timetableConfig.schedule[dayKey]||{};const now=nowMins();let current=null,next=null;
  timetableConfig.periods.forEach((p,idx)=>{const s=parseTime12(p.start),e=parseTime12(p.end);const classKey=daySched[idx];if(s===null||e===null)return;if(now>=s&&now<e){current={idx,period:p,start:s,end:e,classKey,dayKey};}else if(now<s&&!next){if(classKey)next={idx,period:p,start:s,end:e,classKey,dayKey};}});
  return{current,next};
}
function updateCurrentClassBanner(){
  const banner=document.getElementById('ccb');if(!banner)return;
  document.querySelectorAll('.cell.current-period').forEach(el=>el.classList.remove('current-period'));
  const{current}=findCurrentAndNextPeriod();
  if(current&&current.classKey){const cls=classConfig[current.classKey];banner.classList.add('show');document.getElementById('ccb-class').textContent=(cls?cls.name:current.classKey);document.getElementById('ccb-label').textContent=`الحصة ${current.period.num} • الآن`;document.getElementById('ccb-timer').textContent=(current.end-nowMins())+' د';document.getElementById('ccb-timer-lbl').textContent='المتبقي';}
  else{const{next}=findCurrentAndNextPeriod();if(next&&next.classKey){const cls=classConfig[next.classKey];const mins=next.start-nowMins();if(mins>0&&mins<=60){banner.classList.add('show');document.getElementById('ccb-class').textContent=(cls?cls.name:next.classKey);document.getElementById('ccb-label').textContent=`الحصة ${next.period.num} • قادمة`;document.getElementById('ccb-timer').textContent=mins+' د';document.getElementById('ccb-timer-lbl').textContent='تبدأ بعد';}else{banner.classList.remove('show');}}else{banner.classList.remove('show');}}
  checkReminders();
}
function checkReminders(){if(!remindersConfig.enabled)return;const dayKey=currentDayKey();const daySched=(timetableConfig&&timetableConfig.schedule[dayKey])||{};const now=nowMins();timetableConfig.periods.forEach((p,idx)=>{const s=parseTime12(p.start);const classKey=daySched[idx];if(s===null||!classKey)return;const diff=s-now;const target=remindersConfig.minutes||10;if(diff===target||diff===target-1){const key=`${dayKey}_${idx}_${new Date().toDateString()}`;if(reminderState[key])return;reminderState[key]=true;fireReminder(p,classKey,diff);}});}
function fireReminder(period,classKey,diff){const cls=classConfig[classKey];const name=cls?cls.name:classKey;const msg=`حصة ${name} تبدأ بعد ${diff} دقيقة`;document.getElementById('reminder-text').textContent=msg;document.getElementById('reminder-toast').classList.add('show');if('Notification' in window&&Notification.permission==='granted'){try{new Notification('تذكير حصة 🔔',{body:msg});}catch(e){}}if(navigator.vibrate)navigator.vibrate([200,100,200]);}
function dismissReminder(){document.getElementById('reminder-toast').classList.remove('show');}
function loadRemindersUI(){const t=document.getElementById('rs-toggle');t.classList.toggle('on',remindersConfig.enabled);document.getElementById('rs-mins').value=remindersConfig.minutes||10;}
function toggleReminders(){remindersConfig.enabled=!remindersConfig.enabled;document.getElementById('rs-toggle').classList.toggle('on',remindersConfig.enabled);if(remindersConfig.enabled&&'Notification' in window&&Notification.permission==='default'){Notification.requestPermission().then(p=>{if(p==='granted')toast('✅ تم تفعيل التذكيرات','ok');else toast('🔔 التذكيرات داخل الصفحة فقط');});}else{toast(remindersConfig.enabled?'✅ تم التفعيل':'❌ تم الإيقاف',remindersConfig.enabled?'ok':false);}scheduleSave();}
function updReminderMins(){const v=parseInt(document.getElementById('rs-mins').value);if(v>0&&v<=60){remindersConfig.minutes=v;scheduleSave();}}
function testReminder(){fireReminder({num:1},Object.keys(classConfig)[0]||'test',remindersConfig.minutes||10);}
let watcherInterval;
function startClassWatcher(){if(watcherInterval)clearInterval(watcherInterval);updateCurrentClassBanner();watcherInterval=setInterval(updateCurrentClassBanner,30000);}

// ══ SAVE ═══════════════════════════════════════════════
let saveTimer3;
function scheduleSave(){
  clearTimeout(saveTimer3);
  saveTimer3=setTimeout(()=>{
    // Update classConfig in teacherConfig
    if(teacherConfig&&teacherConfig.grades){teacherConfig.grades.forEach(g=>{g.classes.forEach(cls=>{if(classConfig[cls.id]){cls.name=classConfig[cls.id].name;cls.color=classConfig[cls.id].color;}});});}
    dbSave({plan_state:state,arc_meta:arcMeta,cv_items:cvItems,cv_profile:cvProfile,lesson_files:lessonFiles,arc_categories:arcCategories,timetable_config:timetableConfig,class_config:classConfig,students,grades,grade_types:gradeTypes,reminders_config:remindersConfig,teacher_config:teacherConfig,behavior_students:behaviorStudents,behavior_violations:behaviorViolations,behavior_teacher_phone:localStorage.getItem('behaviorTeacherPhone')||''});
  },800);
}

// ══ TOAST ══════════════════════════════════════════════
let tt2;
function toast(msg,type=false){const el=document.getElementById('toast');el.textContent=msg;el.className='toast show'+(type==='ok'?' ok':type===true?' err':'');clearTimeout(tt2);tt2=setTimeout(()=>el.classList.remove('show'),2500);}

// ══ LIBRARY ════════════════════════════════════════════
const ADMIN_EMAIL='teacherplane2026project@gmail.com';
let libraryLinks=[];
let editingLinkId=null;

function isAdmin(){
  if(!currentUser)return false;
  const email=(currentUser.email||'').toLowerCase().trim();
  return email===ADMIN_EMAIL.toLowerCase();
}

async function loadLibrary(){
  if(!sb)return;
  try{
    const{data,error}=await sb.from('library_links').select('*').order('created_at',{ascending:false});
    if(error){console.error('خطأ تحميل المكتبة:',error);return;}
    libraryLinks=data||[];
    populateLibraryFilters();
    renderLibrary();
  }catch(e){console.error('خطأ:',e);}
}

function populateLibraryFilters(){
  const subjects=[...new Set(libraryLinks.map(l=>l.subject))];
  const grades=[...new Set(libraryLinks.map(l=>l.grade))].sort((a,b)=>parseInt(a)-parseInt(b));
  
  const subSelect=document.getElementById('lib-filter-subject');
  const grdSelect=document.getElementById('lib-filter-grade');
  if(!subSelect||!grdSelect)return;
  
  const curSub=subSelect.value;
  const curGrd=grdSelect.value;
  
  subSelect.innerHTML='<option value="">📖 جميع المواد</option>'+subjects.map(s=>`<option value="${s}">${s}</option>`).join('');
  grdSelect.innerHTML='<option value="">🎓 جميع الصفوف</option>'+grades.map(g=>`<option value="${g}">الصف ${g}</option>`).join('');
  
  subSelect.value=curSub;
  grdSelect.value=curGrd;
}

function renderLibrary(){
  const content=document.getElementById('library-content');
  const adminBar=document.getElementById('library-admin-bar');
  if(!content)return;
  
  // إظهار شريط المشرف إذا كان المستخدم مشرفاً
  if(adminBar)adminBar.style.display=isAdmin()?'flex':'none';
  
  const filterSub=document.getElementById('lib-filter-subject').value;
  const filterGrd=document.getElementById('lib-filter-grade').value;
  
  let filtered=libraryLinks;
  if(filterSub)filtered=filtered.filter(l=>l.subject===filterSub);
  if(filterGrd)filtered=filtered.filter(l=>l.grade===filterGrd);
  
  if(!filtered.length){
    content.innerHTML='<div class="lib-empty">📭 لا توجد روابط حالياً<br><small>'+(isAdmin()?'اضغط على "إضافة رابط" لبدء المشاركة':'سيتم إضافة المحتوى قريباً')+'</small></div>';
    return;
  }
  
  // تجميع حسب المادة ثم الصف
  const grouped={};
  filtered.forEach(l=>{
    if(!grouped[l.subject])grouped[l.subject]={};
    if(!grouped[l.subject][l.grade])grouped[l.subject][l.grade]=[];
    grouped[l.subject][l.grade].push(l);
  });
  
  let html='';
  Object.keys(grouped).forEach(subject=>{
    html+=`<div class="lib-section"><div class="lib-section-title">📖 ${subject}</div>`;
    const grades=Object.keys(grouped[subject]).sort((a,b)=>parseInt(a)-parseInt(b));
    grades.forEach(grade=>{
      html+=`<div class="lib-grade-group">
        <div class="lib-grade-label">🎓 الصف ${grade}</div>
        <div class="lib-links-grid">`;
      grouped[subject][grade].forEach(link=>{
        const icon=link.type==='folder'?'📁':'📄';
        const delBtn=isAdmin()?`<button class="lib-link-delete" onclick="event.stopPropagation();deleteLibraryLink(${link.id})" title="حذف">✕</button>`:'';
        html+=`<div class="lib-link-card" onclick="window.open('${link.url}','_blank')">
          <div class="lib-link-icon">${icon}</div>
          <div class="lib-link-info">
            <div class="lib-link-title">${link.title}</div>
            <div class="lib-link-meta">${link.type==='folder'?'مجلد':'ملف'} • اضغط للفتح</div>
          </div>
          ${delBtn}
        </div>`;
      });
      html+=`</div></div>`;
    });
    html+=`</div>`;
  });
  
  content.innerHTML=html;
}

function openLibraryModal(){
  if(!isAdmin()){toast('فقط المشرف يمكنه إضافة الروابط',true);return;}
  editingLinkId=null;
  document.getElementById('lib-modal-title').textContent='➕ إضافة رابط جديد';
  document.getElementById('lib-subject').value='';
  document.getElementById('lib-grade').value='';
  document.getElementById('lib-title').value='';
  document.getElementById('lib-url').value='';
  document.getElementById('lib-type').value='file';
  document.getElementById('library-modal-bg').classList.remove('hidden');
}

function closeLibraryModal(){
  document.getElementById('library-modal-bg').classList.add('hidden');
  editingLinkId=null;
}

async function saveLibraryLink(){
  if(!isAdmin()){toast('فقط المشرف يمكنه إضافة الروابط',true);return;}
  
  const subject=document.getElementById('lib-subject').value;
  const grade=document.getElementById('lib-grade').value;
  const title=document.getElementById('lib-title').value.trim();
  const url=document.getElementById('lib-url').value.trim();
  const lnkType=document.getElementById('lib-type').value;
  
  if(!subject||!grade||!title||!url){
    toast('يرجى ملء جميع الحقول',true);
    return;
  }
  
  if(!url.startsWith('http')){
    toast('الرابط غير صحيح',true);
    return;
  }
  
  try{
    const{error}=await sb.from('library_links').insert({
      subject,grade,title,url,type:lnkType,
      created_by:currentUser.email
    });
    if(error){
      console.error(error);
      toast('فشل الحفظ: '+error.message,true);
      return;
    }
    toast('تم إضافة الرابط بنجاح','ok');
    closeLibraryModal();
    loadLibrary();
  }catch(e){
    console.error(e);
    toast('حدث خطأ',true);
  }
}

async function deleteLibraryLink(id){
  if(!isAdmin()){toast('فقط المشرف يمكنه الحذف',true);return;}
  if(!confirm('هل أنت متأكد من حذف هذا الرابط؟'))return;
  
  try{
    const{error}=await sb.from('library_links').delete().eq('id',id);
    if(error){
      console.error(error);
      toast('فشل الحذف',true);
      return;
    }
    toast('تم الحذف','ok');
    loadLibrary();
  }catch(e){
    console.error(e);
    toast('حدث خطأ',true);
  }
}

// ══ CALENDAR ═══════════════════════════════════════════
let currentMonth=new Date().getMonth();
let currentYear=new Date().getFullYear();
let calendarEvents=JSON.parse(localStorage.getItem('calendarEvents')||'{}');
let selectedDate=null;
const monthNames=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
const dayNames=['أحد','إثن','ثلا','أرب','خمي','جمع','سبت'];

function prevMonth(){currentMonth--;if(currentMonth<0){currentMonth=11;currentYear--;}renderCalendar();}
function nextMonth(){currentMonth++;if(currentMonth>11){currentMonth=0;currentYear++;}renderCalendar();}

function saveCalendarEvents(){localStorage.setItem('calendarEvents',JSON.stringify(calendarEvents));}

function selectDate(year,month,day){
  const key=`${year}-${month}-${day}`;
  const input=document.getElementById('event-input');
  const currentEvent=calendarEvents[key]||'';
  
  // إظهار الحدث الحالي إذا كان موجوداً
  if(currentEvent){
    const confirmMsg=`الحدث: "${currentEvent}"\n\nاضغط OK للتعديل أو Cancel للحذف`;
    const userChoice=confirm(confirmMsg);
    if(!userChoice){
      delete calendarEvents[key];
      saveCalendarEvents();
      renderCalendar();
      return;
    }
  }
  
  input.style.display='block';
  input.value=currentEvent;
  input.placeholder=`حدث ليوم ${day} ${monthNames[month]}`;
  input.focus();
  
  const saveEvent=()=>{
    const val=input.value.trim();
    if(val){
      calendarEvents[key]=val;
    }else{
      delete calendarEvents[key];
    }
    saveCalendarEvents();
    input.style.display='none';
    input.value='';
    renderCalendar();
  };
  
  input.onkeypress=(e)=>{
    if(e.key==='Enter'){
      e.preventDefault();
      saveEvent();
    }
  };
  
  input.onblur=()=>{
    setTimeout(saveEvent,150);
  };
}

function renderCalendar(){
  const calEl=document.getElementById('calendar');
  if(!calEl){
    console.error('عنصر التقويم غير موجود!');
    return;
  }
  
  document.getElementById('cal-title').textContent=monthNames[currentMonth]+' '+currentYear;
  const firstDay=new Date(currentYear,currentMonth,1).getDay();
  const daysInMonth=new Date(currentYear,currentMonth+1,0).getDate();
  const daysInPrevMonth=new Date(currentYear,currentMonth,0).getDate();
  const today=new Date();
  let html='';
  
  // رؤوس الأيام
  dayNames.forEach(d=>html+=`<div class="cal-day-header">${d}</div>`);
  
  // أيام الشهر السابق
  for(let i=firstDay-1;i>=0;i--){
    html+=`<div class="cal-day other-month">${daysInPrevMonth-i}</div>`;
  }
  
  // أيام الشهر الحالي
  for(let d=1;d<=daysInMonth;d++){
    const isToday=d===today.getDate()&&currentMonth===today.getMonth()&&currentYear===today.getFullYear();
    const key=`${currentYear}-${currentMonth}-${d}`;
    const hasEvent=!!calendarEvents[key];
    let classStr='cal-day';
    if(isToday)classStr+=' today';
    if(hasEvent)classStr+=' has-event';
    const eventTitle=calendarEvents[key]?` title="${calendarEvents[key]}"`:'';
    html+=`<div class="${classStr}" onclick="selectDate(${currentYear},${currentMonth},${d})"${eventTitle}>${d}</div>`;
  }
  
  // أيام الشهر التالي لإكمال الجدول
  const remaining=42-(firstDay+daysInMonth);
  for(let i=1;i<=remaining;i++){
    html+=`<div class="cal-day other-month">${i}</div>`;
  }
  
  calEl.innerHTML=html;
}

// ══ TASKS ══════════════════════════════════════════════
let tasks=JSON.parse(localStorage.getItem('userTasks')||'[]');

function saveTasks(){localStorage.setItem('userTasks',JSON.stringify(tasks));}

function renderTasks(){
  const list=document.getElementById('tasks-list');
  if(!tasks.length){list.innerHTML='<div style="text-align:center;color:var(--muted);font-size:12px;padding:20px">لا توجد مهام</div>';return;}
  list.innerHTML=tasks.map((t,i)=>`
    <div class="task-item${t.done?' done':''}" onclick="toggleTask(${i})">
      <div class="task-checkbox">${t.done?'✓':''}</div>
      <div class="task-text">${t.text}</div>
      <span class="task-delete" onclick="event.stopPropagation();deleteTask(${i})">✕</span>
    </div>
  `).join('');
}

function addTask(){
  const input=document.getElementById('task-input');
  const text=input.value.trim();
  if(!text)return;
  tasks.push({text,done:false,id:Date.now()});
  input.value='';
  saveTasks();
  renderTasks();
}

function toggleTask(idx){
  tasks[idx].done=!tasks[idx].done;
  saveTasks();
  renderTasks();
}

function deleteTask(idx){
  tasks.splice(idx,1);
  saveTasks();
  renderTasks();
}

// تهيئة التقويم والمهام عند تحميل الصفحة بالكامل
window.addEventListener('DOMContentLoaded',()=>{
  if(document.getElementById('calendar'))renderCalendar();
  if(document.getElementById('tasks-list'))renderTasks();
  // أيقونات شاشة الدخول المتحركة
  (function initAuthIcons(){
    const screen=document.getElementById('auth-screen');
    if(!screen)return;
    const icons=['📊','📚','📐','📏','🗺️','📝','✏️','📋'];
    const zones=[
      {x:[2,18],y:[5,40]},{x:[2,18],y:[55,90]},
      {x:[82,96],y:[5,40]},{x:[82,96],y:[55,90]},
      {x:[25,42],y:[2,14]},{x:[58,75],y:[2,14]},
      {x:[25,42],y:[86,96]},{x:[58,75],y:[86,96]}
    ];
    zones.forEach((zone,i)=>{
      const el=document.createElement('div');
      el.className='floating-icon';
      const x=zone.x[0]+Math.random()*(zone.x[1]-zone.x[0]);
      const y=zone.y[0]+Math.random()*(zone.y[1]-zone.y[0]);
      const size=Math.random()*8+18;
      const dur=Math.random()*3+4;
      const delay=`${(Math.random()*-6).toFixed(1)}s`;
      const r0=(Math.random()*20-10).toFixed(1);
      const r1=(parseFloat(r0)+Math.random()*14-7).toFixed(1);
      el.textContent=icons[i%icons.length];
      el.style.cssText=`left:${x.toFixed(1)}%;top:${y.toFixed(1)}%;--size:${size.toFixed(0)}px;--dur:${dur.toFixed(1)}s;--delay:${delay};--r0:${r0}deg;--r1:${r1}deg;`;
      screen.appendChild(el);
      for(let s=0;s<3;s++){
        const spark=document.createElement('div');
        spark.className='auth-spark';
        const sw=Math.random()*3+2;
        const angle=Math.random()*Math.PI*2;
        const dist=Math.random()*18+8;
        const sx=(Math.cos(angle)*dist).toFixed(1);
        const sy=(Math.sin(angle)*dist).toFixed(1);
        const sd=(Math.random()*1.5+1).toFixed(1);
        const sdel=`${(Math.random()*-3).toFixed(1)}s`;
        spark.style.cssText=`left:calc(${x.toFixed(1)}% + ${(Math.random()*10-5).toFixed(0)}px);top:calc(${y.toFixed(1)}% + ${(Math.random()*10-5).toFixed(0)}px);--sw:${sw.toFixed(1)}px;--sx:${sx}px;--sy:${sy}px;--sd:${sd}s;--sdel:${sdel};`;
        screen.appendChild(spark);
      }
    });
  })();
});
