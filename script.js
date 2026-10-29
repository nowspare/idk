/* ============================================================
   Student ID Card Studio -- logic
   Vertical ID card, 200 male + 200 female names, 250 phone numbers,
   QR with optional center logo, drawable/uploadable signature.
   ============================================================ */

'use strict';

const STORAGE_KEY = 'pkidstudio.v4';
const DEFAULT_PHOTO = 'assets/default-student.jpg';

/* ---------- NAMES -- 200 MALE ---------- */
const NAMES_MALE = [
'Ali Hassan','Ahmed Raza','Hamza Khan','Muhammad Abdullah','Usman Tariq','Bilal Ahmed','Faisal Iqbal','Zain Malik','Hassan Raza','Ibrahim Shah',
'Saad Farooq','Arsalan Yousaf','Danish Khan','Rehan Akhtar','Talha Siddiqui','Umer Riaz','Haris Mehmood','Shayan Ali','Faizan Haider','Ayan Qureshi',
'Rizwan Abbas','Kamran Akmal','Adnan Sami','Salman Butt','Imran Nazir','Asad Shafiq','Azhar Ali','Sarfaraz Ahmed','Babar Azam','Shaheen Afridi',
'Naseem Shah','Haris Rauf','Mohammad Rizwan','Fakhar Zaman','Imam-ul-Haq','Shan Masood','Abid Ali','Abdullah Shafique','Saud Shakeel','Agha Salman',
'Iftikhar Ahmed','Khushdil Shah','Asif Ali','Haider Ali','Mohammad Nawaz','Shadab Khan','Imad Wasim','Wahab Riaz','Hasan Ali','Junaid Khan',
'Aizaz Khan','Arshad Iqbal','Dilbar Hussain','Ehsan Adil','Fawad Alam','Hammad Azam','Irfan Khan','Jahandad Khan','Kashif Bhatti','Mohammad Abbas',
'Numan Ali','Rahat Ali','Sohail Khan','Tabish Khan','Umaid Asif','Yasir Shah','Zahid Mahmood','Zafar Gohar','Bilawal Bhatti','Mohammad Amir',
'Umar Gul','Saeed Ajmal','Abdur Rehman','Danish Kaneria','Mushtaq Ahmed','Saqlain Mushtaq','Wasim Akram','Waqar Younis','Shoaib Akhtar','Inzamam-ul-Haq',
'Younis Khan','Misbah-ul-Haq','Mohammad Yousuf','Saeed Anwar','Aamer Sohail','Rameez Raja','Javed Miandad','Imran Khan','Zaheer Abbas','Mudassar Nazar',
'Mohsin Khan','Saleem Malik','Ijaz Ahmed','Basit Ali','Aaqib Javed','Wajahatullah Wasti','Shahid Afridi','Abdul Razzaq','Azhar Mahmood','Moin Khan',
'Hamza Ali','Ali Raza','Ahmed Ali','Muhammad Usman','Abdullah Khan','Hassan Ali','Hussain Raza','Zain Abbas','Umar Farooq','Bilal Khan',
'Fahad Mustafa','Farhan Saeed','Atif Aslam','Ali Zafar','Rahat Fateh Ali','Sheheryar Munawar','Fawad Khan','Humayun Saeed','Mikaal Zulfiqar','Osman Khalid',
'Imran Abbas','Bilal Abbas','Wahaj Ali','Feroze Khan','Danish Taimoor','Ahad Raza','Asim Azhar','Zohaib Khan','Zubair Ali','Zeeshan Ahmed',
'Zulfiqar Ali','Zakir Hussain','Yunus Khan','Yasin Malik','Yawar Abbas','Wajid Ali','Waqas Ahmed','Waleed Khan','Wahab Shah','Uzair Khan',
'Usama Bin','Umair Khan','Taimoor Ali','Tahir Mehmood','Sohail Ahmed','Shoaib Malik','Shiraz Ahmed','Sheraz Khan','Shakeel Ahmed','Shahzaib Khan',
'Shahbaz Ahmed','Shafqat Ali','Shafiq Ahmed','Sarmad Khan','Saqib Ali','Sajid Khan','Sajjad Ali','Sahil Ahmed','Sabir Hussain','Raza Ali',
'Rashid Khan','Rauf Ahmed','Rasheed Ali','Qasim Ali','Qaiser Khan','Naveed Ahmed','Nadeem Aslam','Naeem Khan','Mubashir Hussain','Moiz Khan',
'Mohsin Ali','Moeen Khan','Mirza Ali','Mian Umer','Mehmood Khan','Mazhar Ali','Mateen Khan','Masood Ahmed','Maroof Khan','Maqsood Ali',
'Mansoor Khan','Muneeb Ali','Mumtaz Hussain','Mukhtar Ahmed','Mudassir Khan','Mubarak Ali','Moinuddin Khan','Mian Hamza','Meraj Khan','Mehran Ali',
'Mazhar Iqbal','Maaz Khan','Liaqat Ali','Khalid Mahmood','Khurram Shahzad','Khizar Hayat','Kashif Ali','Karim Khan','Junaid Akram','Jibran Khan'
];

/* ---------- NAMES -- 200 FEMALE ---------- */
const NAMES_FEMALE = [
'Ayesha Noor','Fatima Zahra','Sara Ahmed','Hira Khan','Zainab Malik','Iqra Fatima','Maryam Riaz','Sana Yousuf','Maham Ali','Amna Sheikh',
'Noor Fatima','Rida Awan','Areeba Khan','Aiman Fatima','Alina Khan','Anam Raza','Anaya Malik','Anoushay Abbasi','Aqsa Khan','Arisha Ahmed',
'Arooj Fatima','Asma Bibi','Ayesha Khan','Azka Malik','Bisma Riaz','Bushra Ahmed','Dua Fatima','Eman Ali','Eshal Khan','Faiza Iqbal',
'Fariha Khan','Farah Naz','Fareeha Ahmed','Fiza Ali','Gulnaz Khan','Hafsa Malik','Hania Ahmed','Hania Amir','Hareem Farooq','Hina Khan',
'Hina Dilpazeer','Hira Mani','Hoorain Khan','Iqra Aziz','Iman Ali','Inaya Khan','Iqra Khan','Isha Khan','Javeria Khan','Javeria Saud',
'Kainat Khan','Kanwal Ahmed','Kanza Khan','Kausar Khan','Khadija Khan','Kinza Khan','Kiran Khan','Komal Khan','Laiba Khan','Laiba Ali',
'Laraib Khan','Mahira Khan','Mahnoor Khan','Malaika Khan','Maria Khan','Mariam Khan','Maryam Nawaz','Mathira Khan','Maya Khan','Mehak Khan',
'Mehwish Hayat','Mehreen Khan','Minal Khan','Minahil Khan','Mishal Khan','Momina Khan','Momina Mustehsan','Muskan Khan','Myra Khan','Nadia Khan',
'Nadia Afgan','Nafeesa Khan','Naila Khan','Nargis Khan','Naseem Khan','Neelam Khan','Neha Khan','Nida Khan','Nimra Khan','Nina Khan',
'Noor Khan','Noor Bukhari','Nosheen Khan','Nusrat Khan','Parveen Khan','Rabia Khan','Rabia Butt','Rameen Khan','Rania Khan','Rabab Khan',
'Reema Khan','Resham Khan','Rida Khan','Rimsha Khan','Riya Khan','Romaisa Khan','Rubina Khan','Rubab Khan','Sadia Khan','Sadia Imam',
'Saima Khan','Sajal Aly','Sana Khan','Sana Javed','Sanam Khan','Sanam Saeed','Sana Fakhar','Sara Khan','Sarwat Gilani','Sehar Khan',
'Shabnam Khan','Shagufta Khan','Shaista Khan','Shazia Khan','Shehnaaz Khan','Sherry Khan','Sila Khan','Sobia Khan','Sohai Khan','Sonya Khan',
'Sumaira Khan','Sumbul Khan','Suneeta Khan','Syra Khan','Syra Yousuf','Tahira Khan','Tania Khan','Tooba Khan','Urooj Khan','Ushna Khan',
'Ushna Shah','Uzma Khan','Wajiha Khan','Wania Khan','Yumna Khan','Yumna Zaidi','Zara Khan','Zara Noor','Zara Sheikh','Zarnish Khan',
'Zeb Khan','Zeba Khan','Zhalay Khan','Zoya Khan','Zoya Nasir','Zunaira Khan','Aiman Khan','Aiman Muneeb','Areeba Habib','Ayesha Omar',
'Ayesha Gul','Beenish Khan','Faryal Khan','Faryal Mehmood','Ghana Khan','Hania Aamir','Hira Tareen','Iffat Khan','Iqra Kanwal','Kiran Malik',
'Maham Javaid','Minal Khan','Mira Khan','Nadia Hussain','Nimra Rafiq','Rabia Rizwan','Saba Khan','Sabeeka Khan','Sadia Faisal','Saima Nadeem',
'Sana Askari','Sanam Jung','Sara Loren','Sarwat Khan','Sehrish Khan','Shaista Lodhi','Sumbul Iqbal','Ushna Shah','Zara Tareen','Zeba Bakhtiar',
'Areej Khan','Aroosa Khan','Asma Khan','Farah Khan','Fiza Khan','Huma Khan','Huma Nawab','Juggun Khan','Meera Khan','Meesha Khan'
];

/* ---------- PHONE POOL -- 250 Pakistani numbers ---------- */
const PHONE_PREFIXES = ['300','301','302','303','304','305','306','307','308','309','311','312','313','314','315','316','317','318','320','321','322','323','324','325','330','331','332','333','334','335','336','337','340','341','342','343','344','345','346','347','355'];

function buildPhonePool(){
  const pool = new Set();
  while(pool.size < 250){
    const p = PHONE_PREFIXES[Math.floor(Math.random()*PHONE_PREFIXES.length)];
    const n = String(Math.floor(Math.random()*10000000)).padStart(7,'0');
    pool.add(`+92 ${p} ${n}`);
  }
  return Array.from(pool);
}
const PHONE_NUMBERS = buildPhonePool();

/* ---------- INSTITUTIONS ---------- */
const INSTITUTIONS = [
  { name:'University of Peshawar', abbr:'UOP', type:'University', city:'Peshawar' },
  { name:'University of the Punjab', abbr:'PU', type:'University', city:'Lahore' },
  { name:'Quaid-i-Azam University', abbr:'QAU', type:'University', city:'Islamabad' },
  { name:'University of Karachi', abbr:'UOK', type:'University', city:'Karachi' },
  { name:'COMSATS University Islamabad', abbr:'CUI', type:'University', city:'Islamabad' },
  { name:'National University of Sciences and Technology', abbr:'NUST', type:'University', city:'Islamabad' },
  { name:'University of Engineering and Technology, Lahore', abbr:'UET', type:'Engineering College', city:'Lahore' },
  { name:'Government College University Lahore', abbr:'GCUL', type:'College', city:'Lahore' },
  { name:'University of Agriculture Faisalabad', abbr:'UAF', type:'University', city:'Faisalabad' },
  { name:'Bahria University', abbr:'BU', type:'University', city:'Islamabad' },
  { name:'Air University', abbr:'AU', type:'University', city:'Islamabad' },
  { name:'Virtual University of Pakistan', abbr:'VU', type:'University', city:'Lahore' },
  { name:'Allama Iqbal Open University', abbr:'AIOU', type:'University', city:'Islamabad' },
  { name:'International Islamic University Islamabad', abbr:'IIUI', type:'University', city:'Islamabad' },
  { name:'Institute of Business Administration Karachi', abbr:'IBA', type:'Business School', city:'Karachi' },
  { name:'Khyber Medical University', abbr:'KMU', type:'Medical College', city:'Peshawar' }
];

/* ---------- DEPARTMENTS ---------- */
const DEPARTMENTS = [
  { name:'Computer Science', abbr:'CS', degree:'BS Computer Science' },
  { name:'Information Technology', abbr:'IT', degree:'BS Information Technology' },
  { name:'Software Engineering', abbr:'SE', degree:'BS Software Engineering' },
  { name:'Artificial Intelligence', abbr:'AI', degree:'BS Artificial Intelligence' },
  { name:'Cybersecurity', abbr:'CY', degree:'BS Cybersecurity' },
  { name:'Data Science', abbr:'DS', degree:'BS Data Science' },
  { name:'Medicine', abbr:'MED', degree:'MBBS' },
  { name:'Nursing', abbr:'NUR', degree:'BS Nursing' },
  { name:'Pharmacy', abbr:'PHM', degree:'Pharm-D' },
  { name:'Dentistry', abbr:'DEN', degree:'BDS' },
  { name:'Biotechnology', abbr:'BIO', degree:'BS Biotechnology' },
  { name:'Medical Laboratory Technology', abbr:'MLT', degree:'BS MLT' },
  { name:'Electrical Engineering', abbr:'EE', degree:'BSc Electrical Engineering' },
  { name:'Mechanical Engineering', abbr:'ME', degree:'BSc Mechanical Engineering' },
  { name:'Civil Engineering', abbr:'CE', degree:'BSc Civil Engineering' },
  { name:'Computer Engineering', abbr:'COE', degree:'BSc Computer Engineering' },
  { name:'Chemical Engineering', abbr:'CHE', degree:'BSc Chemical Engineering' },
  { name:'Business Administration', abbr:'BBA', degree:'BBA' },
  { name:'Accounting and Finance', abbr:'AF', degree:'BS Accounting & Finance' },
  { name:'Economics', abbr:'ECO', degree:'BS Economics' },
  { name:'Mathematics', abbr:'MATH', degree:'BS Mathematics' },
  { name:'Physics', abbr:'PHY', degree:'BS Physics' },
  { name:'Chemistry', abbr:'CHEM', degree:'BS Chemistry' },
  { name:'English', abbr:'ENG', degree:'BS English' },
  { name:'Psychology', abbr:'PSY', degree:'BS Psychology' },
  { name:'Law', abbr:'LAW', degree:'LLB' }
];

const LOCATIONS = {
  Peshawar:['University Campus Area, Peshawar','University Road, Peshawar','Board Bazaar, Peshawar','Tehkal, Peshawar','Hayatabad, Peshawar','Hayatabad Phase 3','Hayatabad Phase 5','Hayatabad Phase 7','DHA Peshawar','Saddar, Peshawar','Shah Alam, Peshawar'],
  Lahore:['Johar Town','Gulberg','Model Town','DHA Lahore'],
  Islamabad:['H-12 Campus Area','G-10','G-11','Blue Area','F-10'],
  Karachi:['University Road','Gulshan-e-Iqbal','Clifton','DHA Karachi'],
  Faisalabad:['University Campus Area','D-Ground','Madina Town']
};

const LOGOS = [
  { id:'default', label:'Shield', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2 3 6v6c0 5 4 9 9 10 5-1 9-5 9-10V6l-9-4Z"/></svg>' },
  { id:'book', label:'Book', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 5h8v15H3zM13 5h8v15h-8z"/><path d="M11 5v15"/></svg>' },
  { id:'cap', label:'Cap', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 9 12 4l10 5-10 5-10-5Z"/><path d="M6 11v4c0 1 3 2 6 2s6-1 6-2v-4"/></svg>' },
  { id:'atom', label:'Atom', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/></svg>' },
  { id:'cross', label:'Medical', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/></svg>' },
  { id:'gear', label:'Tech', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>' },
  { id:'chart', label:'Business', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/></svg>' },
  { id:'globe', label:'Global', svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>' }
];

const THEMES = [
  { id:'navy', label:'Navy', accent:'#D4AF37', bg:'#0B1B33' },
  { id:'emerald', label:'Emerald', accent:'#34D399', bg:'#06251E' },
  { id:'maroon', label:'Maroon', accent:'#F5C26B', bg:'#2A0B14' },
  { id:'royal', label:'Royal', accent:'#A78BFA', bg:'#140B2E' },
  { id:'slate', label:'Slate', accent:'#06B6D4', bg:'#101418' }
];

const I18N = {
  en:{
    profile:'Profile', institution:'Institution', department:'Department', identifiers:'Identifiers',
    contact:'Contact & QR', design:'Design', signature:'Signature', library:'Library',
    print:'Print', downloadBoth:'Download Both',
    gender:'Gender', photo:'Portrait', upload:'Upload', restoreDefault:'Restore',
    fullName:'Full Name', nameUrdu:'Name in Urdu', fatherName:'Father / Guardian Name',
    pickName:'Pick Random Name', lockName:'Lock Name',
    searchInstitution:'Search Institution', selectInstitution:'Select Institution',
    institutionType:'Type', abbreviation:'Abbreviation', customInstitution:'Custom Institution Name',
    logo:'Institution Logo', pickInstitution:'Pick Random Institution', reset:'Reset',
    selectDepartment:'Select Department', degree:'Degree Program', session:'Academic Session',
    admissionYear:'Admission Year', customDepartment:'Custom Department',
    pickDepartment:'Pick Random Department',
    studentId:'Student ID', regNumber:'Registration Number', rollNumber:'Roll Number',
    admissionNumber:'Admission Number', libraryNumber:'Library Number', examNumber:'Examination Number',
    campusRef:'Campus Reference', deptRef:'Department Reference', cardRef:'Card Reference',
    regenAll:'Regenerate All Unlocked', email:'Email Address',
    phone:'Pakistani Mobile Number', city:'City', area:'Area', customLocation:'Custom Location',
    qrPayload:'QR Content (URL or text)', qrUpload:'Upload file for QR content',
    qrLogo:'QR Center Logo (optional)', notes:'Card Notes (back)', clear:'Clear',
    preset:'Theme Preset', cardAccent:'Accent Color', cardBg:'Card Background',
    radius:'Corner Radius', scale:'Font Scale', cardTitle:'Card Title',
    displayOptions:'Display Options', issueDate:'Issue Date', expiryDate:'Expiry Date',
    saveConfig:'Save Configuration', resetConfig:'Reset Configuration',
    sigDraw:'Draw Signature', sigUpload:'Upload Signature', saveSignature:'Use Signature',
    removeWhite:'Remove white background', sigLabel:'Signature Label', noSignature:'No signature set',
    genFull:'Generate Complete Profile', randomizeAll:'Randomize All Unlocked',
    quantity:'Quantity', genMany:'Generate Many', searchId:'Search',
    exportCsv:'Export CSV', exportJson:'Export JSON', importJson:'Import JSON',
    front:'Front', back:'Back', both:'Both'
  },
  ur:{
    profile:'طالب علم کی معلومات', institution:'ادارہ', department:'شعبہ', identifiers:'شناختی نمبر',
    contact:'رابطہ اور QR', design:'ڈیزائن', signature:'دستخط', library:'کتب خانہ',
    print:'پرنٹ', downloadBoth:'دونوں ڈاؤن لوڈ',
    gender:'جنس', photo:'تصویر', upload:'اپ لوڈ', restoreDefault:'بحال کریں',
    fullName:'پورا نام', nameUrdu:'اردو نام', fatherName:'والد / سرپرست کا نام',
    pickName:'بے ترتیب نام', lockName:'نام مقفل کریں',
    searchInstitution:'ادارہ تلاش کریں', selectInstitution:'ادارہ منتخب کریں',
    institutionType:'قسم', abbreviation:'مختصر نام', customInstitution:'حسبِ ضرورت ادارہ',
    logo:'ادارے کا لوگو', pickInstitution:'بے ترتیب ادارہ', reset:'ری سیٹ',
    selectDepartment:'شعبہ منتخب کریں', degree:'ڈگری پروگرام', session:'تعلیمی سیشن',
    admissionYear:'داخلہ سال', customDepartment:'حسبِ ضرورت شعبہ',
    pickDepartment:'بے ترتیب شعبہ',
    studentId:'شناختی نمبر', regNumber:'رجسٹریشن نمبر', rollNumber:'رول نمبر',
    admissionNumber:'داخلہ نمبر', libraryNumber:'لائبریری نمبر', examNumber:'امتحانی نمبر',
    campusRef:'کیمپس حوالہ', deptRef:'شعبہ حوالہ', cardRef:'کارڈ حوالہ',
    regenAll:'تمام غیر مقفل دوبارہ بنائیں', email:'ای میل پتہ',
    phone:'پاکستانی موبائل نمبر', city:'شہر', area:'علاقہ', customLocation:'حسبِ ضرورت مقام',
    qrPayload:'QR مواد', qrUpload:'QR کے لیے فائل اپ لوڈ',
    qrLogo:'QR درمیانی لوگو', notes:'کارڈ نوٹس', clear:'صاف کریں',
    preset:'تھیم', cardAccent:'کارڈ کا رنگ', cardBg:'کارڈ کا پس منظر',
    radius:'کونے کا رداس', scale:'فونٹ سائز', cardTitle:'کارڈ کا عنوان',
    displayOptions:'ڈسپلے اختیارات', issueDate:'اجرا تاریخ', expiryDate:'اختتام تاریخ',
    saveConfig:'ترتیبات محفوظ کریں', resetConfig:'ترتیبات ری سیٹ کریں',
    sigDraw:'دستخط بنائیں', sigUpload:'دستخط اپ لوڈ کریں', saveSignature:'دستخط استعمال کریں',
    removeWhite:'سفید پس منظر ہٹائیں', sigLabel:'دستخط کا لیبل', noSignature:'کوئی دستخط نہیں',
    genFull:'مکمل پروفائل بنائیں', randomizeAll:'تمام غیر مقفل بدلیں',
    quantity:'کتنے بنائیں', genMany:'کئی بنائیں', searchId:'تلاش',
    exportCsv:'CSV ایکسپورٹ', exportJson:'JSON ایکسپورٹ', importJson:'JSON درآمد',
    front:'سامنے', back:'پیچھے', both:'دونوں'
  }
};

/* ---------- STATE ---------- */
function defaultState(){
  const inst = INSTITUTIONS[0];
  const dept = DEPARTMENTS[0];
  const today = new Date().toISOString().slice(0,10);
  const expiry = new Date(); expiry.setFullYear(expiry.getFullYear()+4);
  return {
    lang:'en',
    surface:'front',
    profile:{
      gender:'male',
      firstName:'Ali', lastName:'Hassan', name:'Ali Hassan', nameUr:'علی حسن',
      fatherName:'Muhammad Hassan',
      photo: DEFAULT_PHOTO,
      logo:'default', logoCustom:null,
      institution:inst.name, institutionShort:inst.abbr, institutionType:inst.type,
      department:dept.name, departmentShort:dept.abbr, degree:dept.degree,
      session:'2024–2028', year:'2026',
      studentId:'', regNumber:'', rollNumber:'', admissionNumber:'',
      libraryNumber:'', examNumber:'', cardRef:'', campusRef:'CMP01', deptRef:'CS',
      email:'', emailNumber:'',
      phone: PHONE_NUMBERS[0],
      city:'Peshawar', area:'University Campus Area, Peshawar', customLoc:'',
      qrPayload:'https://t.me/ih5zz', qrLogo:null,
      notes:'This card is the property of the institution and must be surrendered on request.',
      signature:null, signatureLabel:'Principal Signature',
      issueDate: today, expiryDate: expiry.toISOString().slice(0,10)
    },
    design:{
      theme:'navy', accent:'#D4AF37', bg:'#0B1B33',
      radius:18, scale:1, title:'Student Identity Card',
      showEmail:true, showPhone:true, showLocation:true,
      showIssue:true, showSignature:true, showQrLogo:true
    },
    locks:{ name:false, studentId:false, regNumber:false, rollNumber:false, admissionNumber:false, libraryNumber:false, examNumber:false, cardRef:false, email:false },
    profiles:[], customInstitutions:[], customDepartments:[]
  };
}

let state = defaultState();

/* ---------- UTILITIES ---------- */
const $ = (s, el=document) => el.querySelector(s);
const $$ = (s, el=document) => Array.from(el.querySelectorAll(s));
const rand = a => a[Math.floor(Math.random()*a.length)];
const randInt = (a,b) => Math.floor(Math.random()*(b-a+1))+a;
const pad = (n,w=3) => String(n).padStart(w,'0');
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function toast(msg, type='ok'){
  const t = $('#toast');
  t.textContent = msg;
  t.className = 'toast show ' + type;
  clearTimeout(toast._t);
  toast._t = setTimeout(()=>t.classList.remove('show'), 2200);
}
function save(){ try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }catch(e){} }
function load(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return;
    const p = JSON.parse(raw);
    state = Object.assign(defaultState(), p);
    state.profile = Object.assign(defaultState().profile, p.profile||{});
    state.design = Object.assign(defaultState().design, p.design||{});
    state.locks = Object.assign(defaultState().locks, p.locks||{});
  }catch(e){}
}

/* ---------- NAME / GUARDIAN LOGIC ---------- */
function randomNameFor(gender){
  return rand(gender === 'female' ? NAMES_FEMALE : NAMES_MALE);
}
function lastNameOf(full){
  const parts = String(full||'').trim().split(/\s+/);
  return parts.length ? parts[parts.length-1] : '';
}
function guardianFromName(full){
  const last = lastNameOf(full);
  return last ? `Muhammad ${last}` : '';
}
function applyGenderAndName(gender, force=true){
  state.profile.gender = gender;
  if(force && !state.locks.name){
    const name = randomNameFor(gender);
    state.profile.name = name;
    const parts = name.split(' ');
    state.profile.firstName = parts[0];
    state.profile.lastName = parts[parts.length-1];
    state.profile.nameUr = '';
  }
  state.profile.fatherName = guardianFromName(state.profile.name);
}

/* ---------- IDENTIFIER GENERATION ----------
   INST(abbr) + 2-digit year + DEPT(abbr) + 3/4 digits
*/
function makeIdentifier(p, digits=3){
  const inst = (p.institutionShort||'INST').toUpperCase();
  const yr = String(p.year||'2026').slice(-2);
  const dept = (p.departmentShort||'GEN').toUpperCase();
  const max = Math.pow(10, digits) - 1;
  const num = pad(randInt(0,max), digits);
  return `${inst}${yr}${dept}${num}`;
}
function makeEmail(p){
  const inst = (p.institutionShort||'inst').toLowerCase();
  const yr = String(p.year||'2026').slice(-2);
  const dept = (p.departmentShort||'gen').toLowerCase();
  const num = p.emailNumber || pad(randInt(1,999),3);
  return `${inst}${yr}${dept}${num}@${inst}.edu.pk`;
}

function regenIdentifiers(){
  const p = state.profile;
  if(!state.locks.studentId) p.studentId = makeIdentifier(p,3);
  if(!state.locks.regNumber) p.regNumber = makeIdentifier(p,4);
  if(!state.locks.rollNumber) p.rollNumber = makeIdentifier(p,3);
  if(!state.locks.admissionNumber) p.admissionNumber = makeIdentifier(p,4);
  if(!state.locks.libraryNumber) p.libraryNumber = makeIdentifier(p,3);
  if(!state.locks.examNumber) p.examNumber = makeIdentifier(p,3);
  if(!state.locks.cardRef) p.cardRef = makeIdentifier(p,3);
  if(!state.locks.email){
    p.emailNumber = pad(randInt(1,999),3);
    p.email = makeEmail(p);
  }
}

/* ---------- QR ---------- */
function qrSVG(payload){
  if(typeof qrcode === 'undefined'){
    return `<div style="font-size:7px;color:#000;text-align:center;padding:4px;word-break:break-all">${esc(payload)}</div>`;
  }
  try{
    const qr = qrcode(0,'M');
    qr.addData(payload || 'https://t.me/ih5zz');
    qr.make();
    return qr.createSvgTag({ cellSize:4, margin:0, scalable:true });
  }catch(e){
    return `<div style="font-size:7px;color:#000;text-align:center;padding:4px">QR error</div>`;
  }
}

/* ---------- SIGNATURE ---------- */
function removeWhiteBg(dataUrl, threshold=238){
  return new Promise(resolve => {
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d');
      ctx.drawImage(img,0,0);
      const d = ctx.getImageData(0,0,c.width,c.height);
      const data = d.data;
      for(let i=0;i<data.length;i+=4){
        const r=data[i], g=data[i+1], b=data[i+2];
        if(r>threshold && g>threshold && b>threshold) data[i+3]=0;
        else {
          const avg=(r+g+b)/3;
          if(avg>200) data[i+3]=Math.round(data[i+3]*0.35);
        }
      }
      ctx.putImageData(d,0,0);
      resolve(c.toDataURL('image/png'));
    };
    img.onerror = () => resolve(dataUrl);
    img.src = dataUrl;
  });
}

/* ---------- RENDER ---------- */
function logoMarkup(p){
  if(p.logoCustom) return `<img src="${p.logoCustom}" alt="logo">`;
  const l = LOGOS.find(x=>x.id===p.logo) || LOGOS[0];
  return l.svg;
}
function photoMarkup(p){
  const src = p.photo || DEFAULT_PHOTO;
  const fb = `data:image/svg+xml;utf8,${encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120"><rect width="100" height="120" fill="%23222"/><circle cx="50" cy="45" r="20" fill="%23555"/><path d="M15 120c5-25 20-35 35-35s30 10 35 35z" fill="%23555"/></svg>')}`;
  return `<img src="${esc(src)}" alt="portrait" onerror="this.onerror=null;this.src='${fb}'">`;
}

function row(k,v){
  if(!v) return '';
  return `<div class="data-row"><span class="k">${esc(k)}</span><span class="v">${esc(v)}</span></div>`;
}

function renderFront(){
  const p = state.profile, d = state.design;
  const card = $('#card-front');
  card.style.setProperty('--c-accent', d.accent);
  card.style.setProperty('--c-bg', d.bg);
  card.style.setProperty('--c-radius', d.radius + 'px');
  card.style.setProperty('--c-scale', d.scale);
  card.dir = state.lang === 'ur' ? 'rtl' : 'ltr';

  const rows = [
    row('Registration', p.regNumber),
    row('Student ID', p.studentId),
    row('Department', p.department),
    row('Session', p.session),
    d.showEmail ? row('Email', p.email) : '',
    d.showPhone ? row('Phone', p.phone) : '',
    d.showLocation ? row('Location', p.area) : ''
  ].filter(Boolean).join('');

  const footer = d.showIssue ? `
    <div class="card-foot">
      <div>Issued<b>${esc(p.issueDate || '')}</b></div>
      <div style="text-align:right">Valid Until<b>${esc(p.expiryDate || '')}</b></div>
    </div>` : '';

  card.innerHTML = `
    <div class="card-glow"></div>
    <div class="card-inner">
      <div class="card-top">
        <div class="brand-logo">${logoMarkup(p)}</div>
        <div class="brand-text">
          <div class="brand-name">${esc(p.institution)}</div>
          <div class="brand-type">${esc(p.institutionType)}</div>
        </div>
        <div class="card-badge">ID</div>
      </div>

      <div class="portrait-row">
        <div class="portrait-ring"><div class="portrait">${photoMarkup(p)}</div></div>
      </div>

      <div class="identity">
        <div class="name">${esc(p.name)}</div>
        ${p.nameUr ? `<div class="name-ur">${esc(p.nameUr)}</div>` : ''}
        <div class="degree">${esc(p.degree)}</div>
      </div>

      <div class="data-grid">${rows}</div>
      ${footer}
    </div>
  `;
}

function renderBack(){
  const p = state.profile, d = state.design;
  const card = $('#card-back');
  card.style.setProperty('--c-accent', d.accent);
  card.style.setProperty('--c-bg', d.bg);
  card.style.setProperty('--c-radius', d.radius + 'px');
  card.style.setProperty('--c-scale', d.scale);
  card.dir = state.lang === 'ur' ? 'rtl' : 'ltr';

  const qr = qrSVG(p.qrPayload);
  const qrLogo = (d.showQrLogo && p.qrLogo) ? `<img class="qr-logo" src="${p.qrLogo}" alt="">` : '';
  const rows = [
    row('Guardian', p.fatherName),
    row('Roll No', p.rollNumber),
    row('Admission No', p.admissionNumber),
    row('Library No', p.libraryNumber),
    row('Exam No', p.examNumber),
    row('Card Ref', p.cardRef),
    row('Phone', p.phone),
    row('Email', p.email)
  ].filter(Boolean).join('');

  const sig = (d.showSignature && p.signature)
    ? `<div class="sig-section"><img src="${p.signature}" alt="signature"><div class="sig-line">${esc(p.signatureLabel||'Principal Signature')}</div></div>`
    : `<div class="sig-section"><div class="sig-line">${esc(p.signatureLabel||'Principal Signature')}</div></div>`;

  card.innerHTML = `
    <div class="card-glow"></div>
    <div class="card-inner">
      <div class="card-top">
        <div class="brand-logo">${logoMarkup(p)}</div>
        <div class="brand-text">
          <div class="brand-name">${esc(d.title || 'Student Identity Card')}</div>
          <div class="brand-type">${esc(p.institutionShort)} · ${esc(p.institutionType)}</div>
        </div>
        <div class="card-badge">BACK</div>
      </div>

      <div class="qr-section">
        <div class="qr-frame">${qr}${qrLogo}</div>
      </div>

      <div class="back-rows">${rows}</div>
      <div class="back-note">${esc(p.notes)}</div>
      ${sig}
    </div>
  `;
}

function render(){ renderFront(); renderBack(); applySurface(); }
function applySurface(){
  const s = state.surface;
  $('#wrap-front').hidden = s === 'back';
  $('#wrap-back').hidden = s === 'front';
}

/* ---------- FORM SYNC ---------- */
function syncForm(){
  const p = state.profile, d = state.design;
  const set = (id,v)=>{ const el=$(id); if(el && el.value !== (v??'')) el.value = v??''; };

  set('#in-gender', p.gender);
  set('#in-name', p.name);
  set('#in-nameUr', p.nameUr);
  set('#in-fatherName', p.fatherName);
  set('#in-instType', p.institutionType);
  set('#in-instShort', p.institutionShort);
  set('#in-deptShort', p.departmentShort);
  set('#in-degree', p.degree);
  set('#in-session', p.session);
  set('#in-year', p.year);
  set('#in-studentId', p.studentId);
  set('#in-regNumber', p.regNumber);
  set('#in-rollNumber', p.rollNumber);
  set('#in-admissionNumber', p.admissionNumber);
  set('#in-libraryNumber', p.libraryNumber);
  set('#in-examNumber', p.examNumber);
  set('#in-campusRef', p.campusRef);
  set('#in-deptRef', p.deptRef);
  set('#in-cardRef', p.cardRef);
  set('#in-email', p.email);
  set('#in-phone', p.phone);
  set('#in-customLoc', p.customLoc);
  set('#in-qrPayload', p.qrPayload);
  set('#in-notes', p.notes);
  set('#in-accent', d.accent);
  set('#in-cardBg', d.bg);
  set('#in-radius', d.radius);
  set('#in-scale', d.scale);
  set('#in-cardTitle', d.title);
  set('#in-issueDate', p.issueDate);
  set('#in-expiryDate', p.expiryDate);
  set('#in-signatureLabel', p.signatureLabel);

  $('#tg-showEmail').checked = d.showEmail;
  $('#tg-showPhone').checked = d.showPhone;
  $('#tg-showLocation').checked = d.showLocation;
  $('#tg-showIssue').checked = d.showIssue;
  $('#tg-showSignature').checked = d.showSignature;
  $('#tg-showQrLogo').checked = d.showQrLogo;

  const instSel = $('#in-institution');
  if(instSel) instSel.value = p.institution;
  const deptSel = $('#in-department');
  if(deptSel) deptSel.value = p.department;

  const citySel = $('#in-city');
  if(citySel) citySel.value = p.city || 'Peshawar';
  refreshAreas();
  const areaSel = $('#in-area');
  if(areaSel) areaSel.value = p.area || '';

  $$('[data-lock]').forEach(b=>{
    const locked = !!state.locks[b.dataset.lock];
    b.querySelector('svg').innerHTML = `<use href="${locked?'#i-lock':'#i-unlock'}"/>`;
    b.style.color = locked ? 'var(--accent)' : '';
  });
}

function refreshAreas(){
  const city = $('#in-city').value;
  const sel = $('#in-area');
  const cur = sel.value;
  sel.innerHTML = '<option value="">-- none --</option>';
  (LOCATIONS[city]||[]).forEach(a=>{
    const o=document.createElement('option'); o.value=a; o.textContent=a; sel.appendChild(o);
  });
  if([...sel.options].some(o=>o.value===cur)) sel.value=cur;
}

/* ---------- POPULATE ---------- */
function populateInstitutions(filter=''){
  const sel = $('#in-institution');
  const cur = state.profile.institution;
  sel.innerHTML = '';
  INSTITUTIONS.concat(state.customInstitutions)
    .filter(i=>i.name.toLowerCase().includes(filter.toLowerCase()))
    .forEach(i=>{
      const o=document.createElement('option'); o.value=i.name; o.textContent=`${i.name} (${i.abbr})`; sel.appendChild(o);
    });
  if([...sel.options].some(o=>o.value===cur)) sel.value=cur;
}
function populateDepartments(){
  const sel = $('#in-department');
  sel.innerHTML = '';
  DEPARTMENTS.concat(state.customDepartments).forEach(d=>{
    const o=document.createElement('option'); o.value=d.name; o.textContent=d.name; sel.appendChild(o);
  });
  if([...sel.options].some(o=>o.value===state.profile.department)) sel.value=state.profile.department;
}
function populatePhones(){
  const sel = $('#in-phone');
  sel.innerHTML = '';
  PHONE_NUMBERS.forEach(n=>{
    const o=document.createElement('option'); o.value=n; o.textContent=n; sel.appendChild(o);
  });
  sel.value = state.profile.phone || PHONE_NUMBERS[0];
}
function populateCities(){
  const sel = $('#in-city');
  if(sel.options.length) return;
  Object.keys(LOCATIONS).forEach(c=>{
    const o=document.createElement('option'); o.value=c; o.textContent=c; sel.appendChild(o);
  });
}
function populateLogos(){
  const grid = $('#logo-grid');
  grid.innerHTML = '';
  LOGOS.forEach(l=>{
    const el=document.createElement('div');
    el.className='logo-swatch'+(state.profile.logo===l.id?' selected':'');
    el.innerHTML=l.svg;
    el.title=l.label;
    el.addEventListener('click',()=>{
      state.profile.logo=l.id; state.profile.logoCustom=null;
      populateLogos(); render(); save();
    });
    grid.appendChild(el);
  });
}
function populateThemes(){
  const grid = $('#theme-grid');
  grid.innerHTML = '';
  THEMES.forEach(t=>{
    const el=document.createElement('div');
    el.className='theme-swatch'+(state.design.theme===t.id?' selected':'');
    el.style.background = `linear-gradient(145deg, ${t.bg}, ${t.accent})`;
    el.innerHTML = `<span>${t.label}</span>`;
    el.addEventListener('click',()=>{
      state.design.theme=t.id; state.design.accent=t.accent; state.design.bg=t.bg;
      populateThemes(); syncForm(); render(); save();
    });
    grid.appendChild(el);
  });
}

/* ---------- LANGUAGE ---------- */
function applyLanguage(){
  const dict = I18N[state.lang];
  document.documentElement.lang = state.lang;
  document.documentElement.dir = state.lang==='ur'?'rtl':'ltr';
  $$('[data-i18n]').forEach(el=>{
    const k=el.dataset.i18n; if(dict[k]) el.textContent=dict[k];
  });
  $$('.chip[data-lang]').forEach(c=>c.classList.toggle('active',c.dataset.lang===state.lang));
}

/* ---------- FIELD SET ---------- */
function setField(key,val){
  state.profile[key]=val;

  if(key==='institution'){
    const f=INSTITUTIONS.concat(state.customInstitutions).find(i=>i.name===val);
    if(f){
      state.profile.institutionShort=f.abbr;
      state.profile.institutionType=f.type;
      if(LOCATIONS[f.city]) state.profile.city=f.city;
    }
    regenIdentifiers();
  }
  if(key==='department'){
    const f=DEPARTMENTS.concat(state.customDepartments).find(d=>d.name===val);
    if(f){
      state.profile.departmentShort=f.abbr;
      state.profile.degree=f.degree;
    }
    regenIdentifiers();
  }
  if(['institutionShort','departmentShort','year'].includes(key)){
    regenIdentifiers();
  }
  if(key==='name'){
    state.profile.fatherName = guardianFromName(val);
  }
  if(key==='emailNumber'){
    state.profile.email = makeEmail(state.profile);
  }

  render(); syncForm(); save();
}

/* ---------- SIGNATURE PAD ---------- */
let sigPad = null;
function initSignaturePad(){
  const canvas = $('#sig-canvas');
  if(!canvas || typeof SignaturePad === 'undefined') return;
  const ratio = Math.max(window.devicePixelRatio||1,1);
  canvas.width = canvas.offsetWidth * ratio;
  canvas.height = canvas.offsetHeight * ratio;
  canvas.getContext('2d').scale(ratio,ratio);
  sigPad = new SignaturePad(canvas, {
    backgroundColor:'rgba(0,0,0,0)',
    penColor:'#111111',
    minWidth:0.8,
    maxWidth:2.2
  });
}
function updateSigPreview(){
  const box = $('#sig-preview');
  if(state.profile.signature){
    box.innerHTML = `<img src="${state.profile.signature}" alt="signature">`;
  } else {
    box.innerHTML = `<span>No signature set</span>`;
  }
}

/* ---------- DOWNLOAD ---------- */
function downloadCard(surface){
  const el = surface==='back' ? $('#card-back') : $('#card-front');
  if(!window.html2canvas){ toast('Export library not loaded','err'); return; }
  html2canvas(el,{backgroundColor:null,scale:2,logging:false,useCORS:true}).then(canvas=>{
    const a=document.createElement('a');
    a.download=`student-id-${surface}.png`;
    a.href=canvas.toDataURL('image/png');
    a.click();
    toast('PNG exported');
  }).catch(err=>{ console.error(err); toast('Export failed','err'); });
}

/* ---------- LIBRARY ---------- */
function snapshot(){
  const p = Object.assign({}, state.profile);
  p._id = 'p_'+Date.now()+'_'+randInt(100,999);
  return p;
}
function addProfile(p){
  state.profiles.unshift(p);
  if(state.profiles.length>200) state.profiles.length=200;
  renderProfiles(); save();
}
function renderProfiles(){
  const list=$('#profiles-list');
  const q=($('#in-library-search').value||'').toLowerCase();
  list.innerHTML='';
  const filtered=state.profiles.filter(p=>{
    if(!q) return true;
    return [p.name,p.regNumber,p.studentId,p.institution,p.department].some(v=>String(v||'').toLowerCase().includes(q));
  });
  if(!filtered.length){
    list.innerHTML='<div style="color:var(--muted);font-size:12px;padding:14px;text-align:center">No profiles yet.</div>';
    return;
  }
  filtered.forEach(p=>{
    const item=document.createElement('div');
    item.className='profile-item';
    item.innerHTML=`
      <img class="p-avatar" src="${esc(p.photo||DEFAULT_PHOTO)}" alt="">
      <div class="p-info">
        <div class="p-name">${esc(p.name)}</div>
        <div class="p-meta">${esc(p.regNumber)} · ${esc(p.department)}</div>
      </div>
      <div class="p-actions">
        <button class="btn icon ghost small" data-load="${p._id}"><svg class="icon"><use href="#i-eye"/></svg></button>
        <button class="btn icon ghost small" data-del="${p._id}"><svg class="icon"><use href="#i-trash"/></svg></button>
      </div>`;
    list.appendChild(item);
  });
  list.querySelectorAll('[data-load]').forEach(b=>b.addEventListener('click',()=>{
    const p=state.profiles.find(x=>x._id===b.dataset.load);
    if(p){ state.profile=Object.assign({},p); syncForm(); render(); save(); toast('Profile loaded'); }
  }));
  list.querySelectorAll('[data-del]').forEach(b=>b.addEventListener('click',()=>{
    state.profiles=state.profiles.filter(x=>x._id!==b.dataset.del);
    renderProfiles(); save();
  }));
}
function generateMany(n){
  for(let i=0;i<n;i++){
    const saved=Object.assign({},state.profile);
    const locks=Object.assign({},state.locks);
    Object.keys(state.locks).forEach(k=>state.locks[k]=false);
    randomizeAll();
    addProfile(snapshot());
    state.profile=saved; state.locks=locks;
  }
  syncForm(); render(); save();
  toast(`${n} profile(s) added`);
}
function exportCSV(){
  if(!state.profiles.length){ toast('No profiles','err'); return; }
  const cols=['name','fatherName','gender','institution','institutionShort','department','departmentShort','degree','session','year','studentId','regNumber','rollNumber','admissionNumber','libraryNumber','examNumber','cardRef','email','phone','area'];
  const rows=state.profiles.map(p=>cols.map(c=>`"${String(p[c]??'').replace(/"/g,'""')}"`).join(','));
  triggerDownload(new Blob([cols.join(',')+'\n'+rows.join('\n')],{type:'text/csv'}),'student-profiles.csv');
}
function exportJSON(){
  triggerDownload(new Blob([JSON.stringify({state},null,2)],{type:'application/json'}),'id-studio-config.json');
}
function importJSON(file){
  const r=new FileReader();
  r.onload=e=>{
    try{
      const data=JSON.parse(e.target.result);
      state=Object.assign(defaultState(),data.state||data);
      state.profile=Object.assign(defaultState().profile,state.profile||{});
      state.design=Object.assign(defaultState().design,state.design||{});
      init(true);
      toast('Configuration imported');
    }catch(err){ toast('Invalid JSON','err'); }
  };
  r.readAsText(file);
}
function triggerDownload(blob,name){
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=name; a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),2000);
}

/* ---------- RANDOM ---------- */
function randomizeAll(){
  const p=state.profile;
  if(!state.locks.name){
    applyGenderAndName(p.gender, true);
  }
  const inst=rand(INSTITUTIONS);
  p.institution=inst.name; p.institutionShort=inst.abbr; p.institutionType=inst.type;
  if(LOCATIONS[inst.city]) p.city=inst.city;
  const dept=rand(DEPARTMENTS);
  p.department=dept.name; p.departmentShort=dept.abbr; p.degree=dept.degree;
  p.phone=rand(PHONE_NUMBERS);
  regenIdentifiers();
}
function generateComplete(){
  state.profile.gender=rand(['male','female']);
  randomizeAll();
  toast('Complete profile generated');
}

/* ---------- WIRE ---------- */
function wireNav(){
  $$('.nav-item').forEach(b=>b.addEventListener('click',()=>{
    $$('.nav-item').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    $$('.panel').forEach(p=>p.classList.remove('active'));
    const t=$(`[data-panel="${b.dataset.section}"]`);
    if(t) t.classList.add('active');
  }));
}
function wireSegments(){
  $$('.seg-btn[data-surface]').forEach(b=>b.addEventListener('click',()=>{
    $$('.seg-btn[data-surface]').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    state.surface=b.dataset.surface;
    applySurface(); save();
  }));
}
function wireForm(){
  const map={
    '#in-name':'name','#in-nameUr':'nameUr','#in-fatherName':'fatherName',
    '#in-instShort':'institutionShort','#in-instType':'institutionType',
    '#in-deptShort':'departmentShort','#in-degree':'degree','#in-session':'session',
    '#in-year':'year','#in-studentId':'studentId','#in-regNumber':'regNumber',
    '#in-rollNumber':'rollNumber','#in-admissionNumber':'admissionNumber',
    '#in-libraryNumber':'libraryNumber','#in-examNumber':'examNumber',
    '#in-campusRef':'campusRef','#in-deptRef':'deptRef','#in-cardRef':'cardRef',
    '#in-emailNumber':'emailNumber','#in-phone':'phone','#in-customLoc':'customLoc',
    '#in-qrPayload':'qrPayload','#in-notes':'notes','#in-issueDate':'issueDate',
    '#in-expiryDate':'expiryDate','#in-signatureLabel':'signatureLabel'
  };
  Object.keys(map).forEach(sel=>{
    const el=$(sel); if(!el) return;
    const ev=(el.tagName==='SELECT'||el.type==='date')?'change':'input';
    el.addEventListener(ev,()=>setField(map[sel],el.value));
  });

  $('#in-gender').addEventListener('change',e=>{
    applyGenderAndName(e.target.value,true);
    syncForm(); render(); save();
  });

  const designMap={
    '#in-accent':['accent','color'], '#in-cardBg':['bg','color'],
    '#in-radius':['radius','number'], '#in-scale':['scale','number'],
    '#in-cardTitle':['title','text']
  };
  Object.keys(designMap).forEach(sel=>{
    const [key,type]=designMap[sel];
    $(sel).addEventListener('input',e=>{
      state.design[key]=type==='number'?Number(e.target.value):e.target.value;
      render(); save();
    });
  });

  [['#tg-showEmail','showEmail'],['#tg-showPhone','showPhone'],['#tg-showLocation','showLocation'],
   ['#tg-showIssue','showIssue'],['#tg-showSignature','showSignature'],['#tg-showQrLogo','showQrLogo']]
   .forEach(([sel,key])=>{
     $(sel).addEventListener('change',e=>{ state.design[key]=e.target.checked; render(); save(); });
   });
}
function wireSelects(){
  $('#in-institution').addEventListener('change',e=>setField('institution',e.target.value));
  $('#in-department').addEventListener('change',e=>setField('department',e.target.value));
  $('#in-city').addEventListener('change',e=>{
    state.profile.city=e.target.value; refreshAreas(); state.profile.area=''; render(); save();
  });
  $('#in-area').addEventListener('change',e=>{ state.profile.area=e.target.value; render(); save(); });
  $('#in-inst-search').addEventListener('input',e=>populateInstitutions(e.target.value));

  $('#in-instCustom').addEventListener('change',e=>{
    const v=e.target.value.trim(); if(!v) return;
    const abbr=v.split(/\s+/).map(w=>w[0]).join('').toUpperCase().slice(0,6)||'INST';
    state.customInstitutions.push({name:v,abbr,type:'University',city:'Islamabad'});
    populateInstitutions();
    setField('institution',v);
    e.target.value='';
    toast('Custom institution saved');
  });
  $('#in-deptCustom').addEventListener('change',e=>{
    const v=e.target.value.trim(); if(!v) return;
    const abbr=v.split(/\s+/).map(w=>w[0]).join('').toUpperCase().slice(0,4)||'DPT';
    state.customDepartments.push({name:v,abbr,degree:'BS '+v});
    populateDepartments();
    setField('department',v);
    e.target.value='';
    toast('Custom department saved');
  });
}
function wireActions(){
  $('#btn-random-name').addEventListener('click',()=>{
    if(state.locks.name){ toast('Name is locked','err'); return; }
    applyGenderAndName(state.profile.gender,true);
    syncForm(); render(); save();
  });
  $('#btn-lock-name').addEventListener('click',()=>{
    state.locks.name=!state.locks.name; syncForm(); save();
  });
  $('#btn-photo-reset').addEventListener('click',()=>{
    state.profile.photo=DEFAULT_PHOTO; render(); save();
  });
  $('#in-photo').addEventListener('change',e=>{
    const f=e.target.files[0]; if(!f) return;
    const r=new FileReader();
    r.onload=ev=>{ state.profile.photo=ev.target.result; render(); save(); };
    r.readAsDataURL(f);
  });
  $('#in-logo').addEventListener('change',e=>{
    const f=e.target.files[0]; if(!f) return;
    const r=new FileReader();
    r.onload=ev=>{ state.profile.logoCustom=ev.target.result; render(); save(); };
    r.readAsDataURL(f);
  });
  $('#btn-logo-reset').addEventListener('click',()=>{
    state.profile.logoCustom=null; state.profile.logo='default';
    populateLogos(); render(); save();
  });
  $('#btn-random-institution').addEventListener('click',()=>{
    const i=rand(INSTITUTIONS); setField('institution',i.name);
  });
  $('#btn-reset-institution').addEventListener('click',()=>{
    const i=INSTITUTIONS[0];
    state.profile.institution=i.name; state.profile.institutionShort=i.abbr;
    state.profile.institutionType=i.type; state.profile.city=i.city;
    regenIdentifiers(); syncForm(); render(); save();
  });
  $('#btn-random-dept').addEventListener('click',()=>{
    const d=rand(DEPARTMENTS); setField('department',d.name);
  });
  $('#btn-random-phone').addEventListener('click',()=>{
    state.profile.phone=rand(PHONE_NUMBERS); syncForm(); render(); save();
  });
  $('#btn-regen-all').addEventListener('click',()=>{
    regenIdentifiers(); syncForm(); render(); save();
  });
  $$('[data-regen]').forEach(b=>b.addEventListener('click',()=>{
    const key=b.dataset.regen;
    if(key==='email'){ state.profile.emailNumber=pad(randInt(1,999),3); state.profile.email=makeEmail(state.profile); }
    else if(key==='regNumber'||key==='admissionNumber') state.profile[key]=makeIdentifier(state.profile,4);
    else state.profile[key]=makeIdentifier(state.profile,3);
    syncForm(); render(); save();
  }));
  $$('[data-lock]').forEach(b=>b.addEventListener('click',()=>{
    state.locks[b.dataset.lock]=!state.locks[b.dataset.lock];
    syncForm(); save();
  }));

  $('#btn-copy-email').addEventListener('click',()=>{
    navigator.clipboard.writeText(state.profile.email||'').then(()=>toast('Copied'));
  });

  $('#in-qrFile').addEventListener('change',e=>{
    const f=e.target.files[0]; if(!f) return;
    const r=new FileReader();
    r.onload=ev=>{
      state.profile.qrPayload=String(ev.target.result).trim().slice(0,1200);
      syncForm(); render(); save(); toast('QR content loaded');
    };
    r.readAsText(f);
  });
  $('#in-qrLogo').addEventListener('change',e=>{
    const f=e.target.files[0]; if(!f) return;
    const r=new FileReader();
    r.onload=ev=>{ state.profile.qrLogo=ev.target.result; render(); save(); };
    r.readAsDataURL(f);
  });
  $('#btn-qrLogo-reset').addEventListener('click',()=>{
    state.profile.qrLogo=null; render(); save();
  });

  $('#in-signature').addEventListener('change',async e=>{
    const f=e.target.files[0]; if(!f) return;
    const r=new FileReader();
    r.onload=async ev=>{
      let data=ev.target.result;
      if($('#tg-removeWhite').checked) data=await removeWhiteBg(data);
      state.profile.signature=data;
      updateSigPreview(); render(); save(); toast('Signature uploaded');
    };
    r.readAsDataURL(f);
  });
  $('#btn-sig-reset').addEventListener('click',()=>{
    state.profile.signature=null; updateSigPreview(); render(); save();
  });
  $('#btn-sig-clear').addEventListener('click',()=>{
    if(sigPad) sigPad.clear();
  });
  $('#btn-sig-save').addEventListener('click',()=>{
    if(!sigPad || sigPad.isEmpty()){ toast('Draw a signature first','err'); return; }
    state.profile.signature=sigPad.toDataURL('image/png');
    updateSigPreview(); render(); save(); toast('Signature applied');
  });

  $('#btn-save-config').addEventListener('click',()=>{ save(); toast('Configuration saved'); });
  $('#btn-reset-config').addEventListener('click',()=>{
    if(!confirm('Reset configuration to defaults?')) return;
    state=defaultState(); init(true); toast('Reset complete');
  });

  $('#btn-gen-profile').addEventListener('click',generateComplete);
  $('#btn-randomize-all').addEventListener('click',()=>{ randomizeAll(); syncForm(); render(); save(); });
  $('#btn-gen-many').addEventListener('click',()=>generateMany(parseInt($('#in-qty').value,10)||1));
  $('#in-library-search').addEventListener('input',renderProfiles);
  $('#btn-export-csv').addEventListener('click',exportCSV);
  $('#btn-export-json').addEventListener('click',exportJSON);
  $('#in-importJson').addEventListener('change',e=>{ const f=e.target.files[0]; if(f) importJSON(f); });

  $('#btn-download-both').addEventListener('click',()=>{
    downloadCard('front'); setTimeout(()=>downloadCard('back'),700);
  });
  $('#btn-print').addEventListener('click',()=>window.print());
  $$('[data-download]').forEach(b=>b.addEventListener('click',()=>downloadCard(b.dataset.download)));

  $$('.chip[data-lang]').forEach(c=>c.addEventListener('click',()=>{
    state.lang=c.dataset.lang; applyLanguage(); render(); save();
  }));
}

/* ---------- INIT ---------- */
function init(fresh=false){
  if(!fresh) load();
  populateInstitutions();
  populateDepartments();
  populatePhones();
  populateCities();
  populateLogos();
  populateThemes();
  applyLanguage();
  wireNav();
  wireSegments();
  wireForm();
  wireSelects();
  wireActions();
  initSignaturePad();
  updateSigPreview();

  const p=state.profile;
  if(!p.studentId || !p.regNumber || !p.rollNumber || !p.admissionNumber || !p.libraryNumber || !p.examNumber || !p.cardRef || !p.email){
    regenIdentifiers();
  }

  syncForm();
  render();
  renderProfiles();
  $$('.seg-btn[data-surface]').forEach(b=>b.classList.toggle('active',b.dataset.surface===state.surface));
}

document.addEventListener('DOMContentLoaded',()=>init());