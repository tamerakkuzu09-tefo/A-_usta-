from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 7860))

HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Elektrik Bakım Ustası</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #f0f2f5; min-height: 100vh; display: flex; flex-direction: column; }
  header { background: #1a1a2e; color: white; padding: 16px 20px; text-align: center; }
  header h1 { font-size: 20px; }
  header p { font-size: 13px; color: #aaa; margin-top: 4px; }
  #chat { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; justify-content: flex-end; gap: 12px; max-height: calc(100vh - 180px); }
  .msg { max-width: 80%; padding: 12px 16px; border-radius: 16px; font-size: 15px; line-height: 1.5; word-wrap: break-word; }
  .bot { background: white; color: #222; border-bottom-left-radius: 4px; align-self: flex-start; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  .user { background: #0084ff; color: white; border-bottom-right-radius: 4px; align-self: flex-end; }
  #buttons { padding: 10px 16px; display: flex; flex-wrap: wrap; gap: 10px; background: #f0f2f5; }
  .btn { padding: 12px 20px; font-size: 15px; font-weight: bold; border: 2px solid #0084ff; border-radius: 24px; background: white; color: #0084ff; cursor: pointer; flex: 1; min-width: 120px; text-align: center; transition: all 0.2s; }
  .btn:active { background: #0084ff; color: white; }
  #input-area { display: flex; padding: 10px 16px; gap: 8px; background: white; border-top: 1px solid #ddd; }
  #text-input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 24px; font-size: 15px; outline: none; }
  #send-btn { padding: 12px 20px; background: #0084ff; color: white; border: none; border-radius: 24px; font-size: 15px; cursor: pointer; font-weight: bold; }
  #reset-btn { width: 100%; padding: 10px; background: #eee; border: none; font-size: 14px; cursor: pointer; color: #666; }
</style>
</head>
<body>
<header>
  <h1>🔧 AI Elektrik Bakım Ustası</h1>
  <p>Arızayı yazın veya seçeneklere tıklayın</p>
</header>

<div id="chat"></div>
<div id="buttons"></div>
<div id="input-area">
  <input id="text-input" type="text" placeholder="Örnek: Motor çalışmıyor..." />
  <button id="send-btn" onclick="sendText()">Gönder</button>
</div>
<button id="reset-btn" onclick="resetChat()">🔄 Sıfırla</button>

<script>
const TRIGGERS = [
  "motor çalışmıyor", "motor arızalı", "calismiyor",
  "çalışmıyor", "motor start almıyor"
];

const TREE = {
  "start": {
    text: "Bu motor kaç voltta çalışıyor?",
    buttons: ["220 Volt", "380 Volt"]
  },
  "220 Volt": {
    text: "220V motorlarda kondansatör arızası sık görülür. Kondansatörü kontrol edin.",
    buttons: []
  },
  "380 Volt": {
    text: "Bu motor neyle çalışıyor?",
    buttons: ["Kontaktör", "Invertör", "Softstarter"]
  },
  "Kontaktör": {
    text: "Termik atmış mı?",
    buttons: ["Evet", "Hayır"]
  },
  "Invertör": {
    text: "Invertör ekranında hata kodu var mı?",
    buttons: ["Var", "Yok"]
  },
  "Softstarter": {
    text: "Softstarter hata ışığı yanıyor mu?",
    buttons: ["Evet", "Hayır"]
  },
  "Evet": {
    text: "Termiği resetleyip tekrar deneyin.",
    buttons: []
  },
  "Hayır": {
    text: "Motor klemensinde 3 faz var mı?",
    buttons: ["Var", "Yok"]
  },
  "Var": {
    text: "Motor sıkışmış olabilir. Yükü kontrol edin.",
    buttons: []
  },
  "Yok": {
    text: "Sigorta veya kabloyu kontrol edin.",
    buttons: []
  }
};

let state = null;
let chat = document.getElementById("chat");

function addMsg(text, isUser) {
  let div = document.createElement("div");
  div.className = "msg " + (isUser ? "user" : "bot");
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function showButtons(buttons) {
  let area = document.getElementById("buttons");
  area.innerHTML = "";
  buttons.forEach(b => {
    let btn = document.createElement("button");
    btn.className = "btn";
    btn.textContent = b;
    btn.onclick = () => choose(b);
    area.appendChild(btn);
  });
}

function choose(choice) {
  addMsg(choice, true);
  let node = TREE[choice];
  if (!node) return;
  addMsg(node.text, false);
  state = choice;
  showButtons(node.buttons);
}

function sendText() {
  let input = document.getElementById("text-input");
  let text = input.value.trim();
  if (!text) return;
  input.value = "";
  addMsg(text, true);

  if (state === null) {
    let lower = text.toLowerCase();
    let matched = TRIGGERS.some(t => lower.includes(t));
    if (matched) {
      let node = TREE["start"];
      addMsg(node.text, false);
      state = "start";
      showButtons(node.buttons);
    } else {
      addMsg("⚠️ Lütfen arızayı daha açık belirtin. Örnek: Motor çalışmıyor", false);
    }
  } else {
    let node = TREE[state];
    let match = node.buttons.find(b => b.toLowerCase().includes(text.toLowerCase()) || text.toLowerCase().includes(b.toLowerCase()));
    if (match) {
      choose(match);
    } else {
      addMsg("❓ Anlamadım. Lütfen aşağıdaki seçeneklerden birini seçin.", false);
      showButtons(node.buttons);
    }
  }
}

function resetChat() {
  chat.innerHTML = "";
  document.getElementById("buttons").innerHTML = "";
  state = null;
  addMsg("Merhaba! Arızayı yazarak başlayın. Örnek: Motor çalışmıyor", false);
}

document.getElementById("text-input").addEventListener("keypress", e => {
  if (e.key === "Enter") sendText();
});

resetChat();
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
    def log_message(self, format, *args):
        pass

print(f"Sunucu başlatılıyor: port {PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
