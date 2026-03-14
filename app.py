<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ElektroAI</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0a0e1a; --surface: #111827; --surface2: #1a2235;
  --border: #1e2d45; --accent: #f59e0b; --accent2: #3b82f6;
  --danger: #ef4444; --success: #10b981; --text: #e2e8f0;
  --text-muted: #64748b; --bot-bg: #151f30; --user-bg: #1e3a5f;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Syne', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
body::before { content: ''; position: fixed; inset: 0; background-image: linear-gradient(rgba(245,158,11,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(245,158,11,0.03) 1px, transparent 1px); background-size: 40px 40px; pointer-events: none; z-index: 0; }
header { position: relative; z-index: 10; background: var(--surface); border-bottom: 1px solid var(--border); padding: 14px 20px; display: flex; align-items: center; gap: 14px; }
.header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, var(--accent), #d97706); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; box-shadow: 0 0 20px rgba(245,158,11,0.3); }
.header-text h1 { font-size: 18px; font-weight: 800; letter-spacing: -0.5px; color: white; }
.header-text p { font-size: 12px; color: var(--text-muted); font-family: 'Space Mono', monospace; margin-top: 2px; }
.status-dot { margin-left: auto; display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--success); font-family: 'Space Mono', monospace; }
.status-dot::before { content: ''; width: 7px; height: 7px; background: var(--success); border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16,185,129,0.4); } 50% { opacity: 0.8; box-shadow: 0 0 0 5px rgba(16,185,129,0); } }
#chat { flex: 1; overflow-y: auto; padding: 20px 16px; display: flex; flex-direction: column; gap: 14px; position: relative; z-index: 1; scroll-behavior: smooth; max-height: calc(100vh - 200px); }
#chat::-webkit-scrollbar { width: 4px; }
#chat::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
.msg-wrapper { display: flex; gap: 10px; animation: slideIn 0.25s ease; }
.msg-wrapper.user { flex-direction: row-reverse; }
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.avatar { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; margin-top: 2px; }
.avatar.bot { background: linear-gradient(135deg, var(--accent), #d97706); color: #000; }
.avatar.user { background: var(--user-bg); border: 1px solid var(--accent2); color: var(--accent2); }
.msg { max-width: 78%; padding: 12px 16px; border-radius: 16px; font-size: 14px; line-height: 1.65; word-wrap: break-word; white-space: pre-wrap; }
.msg.bot { background: var(--bot-bg); border: 1px solid var(--border); border-bottom-left-radius: 4px; color: var(--text); }
.msg.user { background: var(--user-bg); border: 1px solid rgba(59,130,246,0.3); border-bottom-right-radius: 4px; color: #bfdbfe; }
.ai-badge { display: inline-block; font-size: 10px; font-family: 'Space Mono', monospace; color: var(--accent); background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2); border-radius: 4px; padding: 2px 6px; margin-bottom: 8px; }
#buttons { padding: 10px 16px; display: flex; flex-wrap: wrap; gap: 8px; background: var(--surface); border-top: 1px solid var(--border); position: relative; z-index: 10; min-height: 10px; }
.btn { padding: 10px 18px; font-size: 13px; font-weight: 600; font-family: 'Syne', sans-serif; border: 1px solid var(--accent); border-radius: 8px; background: rgba(245,158,11,0.08); color: var(--accent); cursor: pointer; flex: 1; min-width: 110px; text-align: center; transition: all 0.15s; }
.btn:hover { background: rgba(245,158,11,0.18); transform: translateY(-1px); }
.btn:active { background: var(--accent); color: #000; transform: translateY(0); }
#input-area { display: flex; padding: 12px 16px; gap: 10px; background: var(--surface); border-top: 1px solid var(--border); position: relative; z-index: 10; }
#text-input { flex: 1; padding: 12px 16px; border: 1px solid var(--border); border-radius: 10px; font-size: 14px; font-family: 'Syne', sans-serif; background: var(--bg); color: var(--text); outline: none; transition: border-color 0.2s; }
#text-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(245,158,11,0.1); }
#text-input::placeholder { color: var(--text-muted); }
#send-btn { padding: 12px 20px; background: var(--accent); color: #000; border: none; border-radius: 10px; font-size: 14px; font-weight: 700; font-family: 'Syne', sans-serif; cursor: pointer; transition: all 0.15s; white-space: nowrap; }
#send-btn:hover { background: #fbbf24; box-shadow: 0 0 16px rgba(245,158,11,0.4); }
#send-btn:disabled { background: var(--border); color: var(--text-muted); cursor: not-allowed; box-shadow: none; }
#mode-bar { padding: 6px 16px; background: var(--surface2); border-top: 1px solid var(--border); font-size: 11px; font-family: 'Space Mono', monospace; color: var(--text-muted); display: flex; align-items: center; gap: 6px; position: relative; z-index: 10; }
#reset-btn { width: 100%; padding: 9px; background: transparent; border: none; border-top: 1px solid var(--border); font-size: 12px; font-family: 'Space Mono', monospace; cursor: pointer; color: var(--text-muted); transition: color 0.2s; position: relative; z-index: 10; }
#reset-btn:hover { color: var(--danger); }
.typing { display: flex; gap: 5px; padding: 14px 16px; align-items: center; }
.typing span { width: 7px; height: 7px; background: var(--accent); border-radius: 50%; animation: bounce 1.2s infinite; opacity: 0.6; }
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 80%, 100% { transform: translateY(0); opacity: 0.4; } 40% { transform: translateY(-6px); opacity: 1; } }
</style>
</head>
<body>
<header>
  <div class="header-icon">&#9889;</div>
  <div class="header-text">
    <h1>ElektroAI</h1>
    <p>Akilli Elektrik Bakim Asistani</p>
  </div>
  <button onclick="resetChat()" style="margin-left:auto;padding:8px 14px;background:#ef4444;color:white;border:none;border-radius:8px;font-size:12px;font-weight:700;cursor:pointer;font-family:'Syne',sans-serif;white-space:nowrap;">&#8634; Yeni Sohbet</button>
</header>
<div id="chat"></div>
<div id="buttons"></div>
<div id="input-area">
  <input id="text-input" type="text" placeholder="Arizayi yazin... (or: motor calısmiyor)" />
  <button id="send-btn" onclick="sendText()">Gonder</button>
</div>
<div id="mode-bar">Mod: <span id="mode-label" style="color:#64748b">Bekleniyor</span></div>


<script>
var TRIGGERS = ['motor','ariza','calismiyor','calısmiyor','problem','sorun','start','kontaktor','sigorta','termik','faz','voltaj','akim','invertor','pano','kablo'];

var TREE = {
  'start': { text: 'Bu motor kac voltta calisiyor?', buttons: ['220 Volt', '380 Volt'] },
  '220 Volt': { text: '220 volt motorlari calistirmanin dogru yolu kontaktor-termik ile calistirmaktir.\n\nOnce motora elektrik gelip gelmedigini kontrol et. Gelmiyorsa sigorta, kontaktor, termik, fis, priz ve kabloyu kontrol et. Motor klemensinden 210-240 volt olmasi lazim.\n\nMotorda titreme, ses, zorlanma varsa kondansator arizali olabilir. Kondansatoru olc, sağlam degilse degistir.\n\nZorlanma kondansatordan degil mekanik sikismadan da olabilir. Motoru yukten ayir, bosta calistir. Calisirsa sorun yuktur.\n\nMotor hala calismiyorsa sargılari olc. Uclar ile govde arası kisa devre veya sargı deger gostermiyorsa motor yanikdir.', buttons: [] },
  '380 Volt': { text: 'Bu motor neyle calisiyor?', buttons: ['Kontaktor', 'Invertor', 'Softstarter'] },
  'Kontaktor': { text: 'Termik atmis mi?', buttons: ['Evet', 'Hayir'] },
  'Invertor': { text: 'Invertor ekraninda hata kodu var mi?', buttons: ['Var', 'Yok'] },
  'Softstarter': { text: 'Softstarter hata isigi yaniyor mu?', buttons: ['Evet', 'Hayir'] },
  'Evet': { text: 'Once guvenlik kurallarina uy! Panodaki kontaktor ve termik devresini gozle kontrol et. Yanik parca veya kablo var mi? Yanik kokusu geliyor mu?', buttons: ['Yanik var', 'Yanik yok'] },
  'Yanik var': { text: 'Yanik olan parca veya kabloyu degistirin. Degisimden sonra tekrar deneyin.', buttons: [] },
  'Yanik yok': { text: 'Termigi resetle ve start butonuna bas. Termik tekrar atiyor mu?', buttons: ['Atmiyor', 'Bir sure sonra atiyor', 'Hemen atiyor'] },
  'Atmiyor': { text: 'Sorun degisken yukle ilgili olabilir. Anlik zorlanmada akim artip termik atmis olabilir. Motoru calistir ve akimlarini kontrol et.', buttons: [] },
  'Bir sure sonra atiyor': { text: 'Motor fazla akim cekiyor. Ya yuk motora uygun degil ya da mekanik zorlanma var. Motoru ve yuku mekaniksel olarak kontrol et.', buttons: [] },
  'Hemen atiyor': { text: 'Kisa devre ihtimali var. Motor mi pano mu anlayalim.\n\nMotor kablosunu panodan soK (klemens veya kontaktor/termige bagli olabilir). Termigi resetle, start butonuna bas. Termik atiyor mu?', buttons: ['Atmiyor2', 'Bir sure sonra atiyor2', 'Hemen atiyor2'] },
  'Atmiyor2': { text: 'Simdi pano voltaj olcumleri yapalim. Kontaktor cekili iken kablo cikis noktasindan voltaj olc. Fazlar arasi 375-405 volt olmasi lazim.', buttons: ['Voltaj normal', 'Voltaj normal degil'] },
  'Bir sure sonra atiyor2': { text: 'Kablo veya baglanti noktalarinda kacak akim olabilir. Kabloyu ve baglantilari kontrol edin.', buttons: [] },
  'Hemen atiyor2': { text: 'Pano tarafinda kisa devre var. Kontaktor, termik ve baglantilari kontrol edin.', buttons: [] },
  'Voltaj normal': { text: 'Motorun yanina git. Anormal durum var mi? Yakından kokla. Motor el ile doniyor mu?', buttons: ['Motor elle doniyor', 'Motor elle donmuyor'] },
  'Voltaj normal degil': { text: 'Pano besleme hattinda sorun var. Sigortalari, kablo bağlantilarini ve sebeke gelisini kontrol edin.', buttons: [] },
  'Motor elle doniyor': { text: 'Klemens kapagini ac, kabloları cıkar. Kablolar bosta iken termigi resetle, start butonuna bas. Kablo uclarinda voltaj olc. 375-405 volt olmali.', buttons: ['Voltaj normal2', 'Voltaj normal degil2'] },
  'Motor elle donmuyor': { text: 'Motora bagli yuku ayir (kayis, zincir, reduktor, pompa, fan vb.) ve tekrar elle donup donmedigini kontrol et.', buttons: ['Yuk ayrildi motor doniyor', 'Yuk ayrildi motor donmuyor'] },
  'Yuk ayrildi motor doniyor': { text: 'Yuk ayrılınca motor doniyor ise yukle ilgili mekaniksel sorun var. Termik atma ve calismama sebebi budur.', buttons: [] },
  'Yuk ayrildi motor donmuyor': { text: 'Motorda mekaniksel sikisma var. Muhtemelen rulman kilitlemistir. Motoru yedegi ile degistir ya da bakim yap.', buttons: [] },
  'Voltaj normal2': { text: 'Olcu aletini buzzer konumuna al. Once klemens uclari ile govde arasi olc, sonra fazlar arasi olc.\n\nYanik motorda uclardan birinde govde kisa devresi olur ya da bir faz deger gostermez. Bu motorun yanik oldugu anlamina gelir. Etiket bilgisine dikkat ederek degistir.\n\nSaglam motorda faz direnc degerleri birbirine yakin ve govde kisa devresi olmaz.', buttons: [] },
  'Voltaj normal degil2': { text: 'Kablo hattinda sorun var. Motordan panoya giden kabloyu kontrol edin.', buttons: [] },
  'Hayir': { text: 'Motoru calistiran kontaktor cekiyor mu?', buttons: ['Evet cekiyor', 'Hayir cekmıyor'] },
  'Hayir cekmıyor': { text: 'Kontaktorun bobin uclarina (A1 ve A2) enerji geliyor mu? Kontaktorun calisma voltajini bilmen lazim, genelde uzerinde yazar (220V AC, 110V AC, 24V DC gibi).\n\nOlcu aletini once AC moduna al. Deger gormezsen DC ye gec. Enerji gelmiyorsa kontaktoru enerjileyen elemani kontrol et (start butonu, sensor, sivic, PLC vb.)', buttons: [] },
  'Evet cekiyor': { text: 'Kontaktorun giris ve cikis uclarindaki 3 faz voltaji olc. 370-410 volt arasi olmali.\n\nGiris normal ama cikista eksiklik/yokluk varsa kontaktor arizalidir. (Faz eksikligi motor termik attırir.)\n\nGiriste de voltaj yoksa kontaktore enerji gelmiyor demektir.', buttons: [] },
  'Var': { text: 'Invertor ekranindaki hata kodunu yazin, yardimci olayim.', buttons: [] },
  'Yok': { text: 'Hata kodu yoksa sunlari kontrol edin:\n1. Cikis uclarinda (U, V, W) voltaj var mi?\n2. Giris voltaji normal mi? (375-405V)\n3. Enable/Run sinyali geliyor mu?\n4. Referans frekans sifir mi?', buttons: [] }
};

var state = null;
var useAI = false;
var conversationHistory = [];
var chat, modeLabel;

function initDOM() {
  chat = document.getElementById('chat');
  modeLabel = document.getElementById('mode-label');
}

function addMsg(text, isUser, isAI) {
  var wrapper = document.createElement('div');
  wrapper.className = 'msg-wrapper ' + (isUser ? 'user' : 'bot');
  var avatar = document.createElement('div');
  avatar.className = 'avatar ' + (isUser ? 'user' : 'bot');
  avatar.textContent = isUser ? 'SN' : 'AI';
  var msgDiv = document.createElement('div');
  msgDiv.className = 'msg ' + (isUser ? 'user' : 'bot');
  if (isAI && !isUser) {
    var badge = document.createElement('div');
    badge.className = 'ai-badge';
    badge.textContent = '* AI MODU';
    msgDiv.appendChild(badge);
  }
  var textDiv = document.createElement('div');
  textDiv.style.whiteSpace = 'pre-wrap';
  textDiv.textContent = text;
  msgDiv.appendChild(textDiv);
  wrapper.appendChild(avatar);
  wrapper.appendChild(msgDiv);
  chat.appendChild(wrapper);
  chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
  var wrapper = document.createElement('div');
  wrapper.className = 'msg-wrapper bot';
  wrapper.id = 'typing-indicator';
  var avatar = document.createElement('div');
  avatar.className = 'avatar bot';
  avatar.textContent = 'AI';
  var t = document.createElement('div');
  t.className = 'msg bot typing';
  t.innerHTML = '<span></span><span></span><span></span>';
  wrapper.appendChild(avatar);
  wrapper.appendChild(t);
  chat.appendChild(wrapper);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  var t = document.getElementById('typing-indicator');
  if (t) t.remove();
}

function showButtons(btns) {
  var area = document.getElementById('buttons');
  area.innerHTML = '';
  for (var i = 0; i < btns.length; i++) {
    (function(b) {
      var el = document.createElement('button');
      el.className = 'btn';
      el.textContent = b;
      el.onclick = function() { choose(b); };
      area.appendChild(el);
    })(btns[i]);
  }
}

function setMode(mode) {
  modeLabel.textContent = mode;
  modeLabel.style.color = mode === 'AI Modu' ? '#f59e0b' : mode === 'Rehberli Mod' ? '#3b82f6' : '#64748b';
}

function setSendDisabled(v) {
  document.getElementById('send-btn').disabled = v;
  document.getElementById('text-input').disabled = v;
}

function choose(choice) {
  addMsg(choice, true, false);
  var node = TREE[choice];
  if (!node) return;
  addMsg(node.text, false, false);
  state = choice;
  setMode('Rehberli Mod');
  if (node.buttons && node.buttons.length > 0) {
    showButtons(node.buttons);
  } else {
    showButtons([]);
    setTimeout(function() {
      addMsg('Yukaridaki adimlari uyguladiniz mi? Baska soru varsa serbest yazabilirsiniz, AI yardimci olacak.', false, false);
      useAI = true;
      setMode('AI Modu');
    }, 600);
  }
}

async function askAI(msg) {
  setSendDisabled(true);
  showTyping();
  conversationHistory.push({ role: 'user', content: msg });
  var sys = 'Sen ElektroAI adinda uzman bir elektrik bakim asistanisin. 30 yillik elektrik bakim deneyimine sahip bir ustanin bilgisiyle donatildin. Uzmanlik alanlarin: endustriyel elektrik motor arizalari (220V-380V), kontaktor, termik role, invertor, softstarter, pano arizalari, sigorta, kablo, PLC ve otomasyon sistemleri, insaat elektrik. Yanit verirken once guvenlik uyarisi ver, adim adim ariza tespit yontemi anlat, olcum degerlerini belirt.';
  try {
    var res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: 'claude-sonnet-4-20250514', max_tokens: 1000, system: sys, messages: conversationHistory })
    });
    var data = await res.json();
    removeTyping();
    if (data.content && data.content[0]) {
      var reply = data.content[0].text;
      conversationHistory.push({ role: 'assistant', content: reply });
      addMsg(reply, false, true);
    } else {
      addMsg('Hata olustu. Tekrar deneyin.', false, false);
    }
  } catch(e) {
    removeTyping();
    addMsg('Baglanti hatasi. Internet baglantinizi kontrol edin.', false, false);
  }
  setSendDisabled(false);
  document.getElementById('text-input').focus();
}

function sendText() {
  var input = document.getElementById('text-input');
  var text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMsg(text, true, false);
  var lower = text.toLowerCase();

  if (useAI) { askAI(text); return; }

  if (state === null) {
    var matched = TRIGGERS.some(function(t) { return lower.indexOf(t) !== -1; });
    if (matched) {
      addMsg(TREE['start'].text, false, false);
      state = 'start';
      setMode('Rehberli Mod');
      showButtons(TREE['start'].buttons);
    } else {
      useAI = true; setMode('AI Modu'); askAI(text);
    }
  } else {
    var node = TREE[state];
    if (node && node.buttons && node.buttons.length > 0) {
      var match = null;
      for (var i = 0; i < node.buttons.length; i++) {
        if (lower.indexOf(node.buttons[i].toLowerCase()) !== -1) { match = node.buttons[i]; break; }
      }
      if (match) { choose(match); }
      else { useAI = true; setMode('AI Modu'); askAI(text); }
    } else {
      useAI = true; setMode('AI Modu'); askAI(text);
    }
  }
}

function resetChat() {
  chat.innerHTML = '';
  document.getElementById('buttons').innerHTML = '';
  state = null; useAI = false; conversationHistory = [];
  setMode('Bekleniyor');
  addMsg('Merhaba! Ben ElektroAI.\n\nArizayi yazarak baslayin veya soru sorun.\nOrnek: "Motor calısmiyor", "Sigorta atiyor", "Faz eksikligi var"', false, false);
}

document.addEventListener('DOMContentLoaded', function() {
  initDOM();
  document.getElementById('text-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) sendText();
  });
  resetChat();
});
</script>
</body>
</html>
