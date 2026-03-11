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
    text: "Öncelikle kesinlikle güvenlik kurallarına uy, dikkatli ve tedbirli ol. Panoda motorun bağlı olduğu kontaktör ve termik devresini gözle kontrol et. Yanık herhangi bir parça veya kablo var mı, yanık kokusu geliyor mu? Eğer böyle bir durum varsa gerekli değişimleri ve düzeltmeleri yap.",
    buttons: ["Yanık var", "Yanık yok"]
  },
  "Yanık var": {
    text: "Yanık olan parça veya kabloyu değiştirin. Değişimden sonra tekrar deneyin.",
    buttons: []
  },
  "Yanık yok": {
    text: "Termiği resetle ve start butonuna bas, bak bakalım termik tekrar atıyor mu?",
    buttons: ["Atmıyor", "Bir süre sonra atıyor", "Hemen atıyor"]
  },
  "Atmıyor": {
    text: "Motor çalışmaya başladı. Sorununuz çözülmüş görünüyor. Takipte kalın.",
    buttons: []
  },
  "Bir süre sonra atıyor": {
    text: "Motor ısınma sorunu yaşıyor olabilir. Motorun üzerindeki fanı ve havalandırma deliklerini kontrol edin. Aşırı yük var mı kontrol edin.",
    buttons: []
  },
  "Hemen atıyor": {
    text: "Bu durumda olası bir kısa devre ihtimali var. Bu kısa devre motor tarafında mı pano tarafında mı onu anlayalım. Şimdi şunu yap: Motor kablosunun panoya girip bağlandığı noktadan (klemens ya da direkt kontaktör veya termiğe bağlanmış olabilir) kabloları sıralamasına dikkat ederek sök, yani motor kablosunu panodan ayır. Termiği tekrar resetle ve start butonuna bas. Tekrar gözlemle, termik atıyor mu? Atıyorsa start butonuna basar basmaz mı atıyor yoksa yine bir süre sonra mı atıyor?",
    buttons: ["Atmıyor2", "Bir süre sonra atıyor2", "Hemen atıyor2"]
  },
  "Atmıyor2": {
    text: "Şimdi önce panoda voltaj ölçümleri yapalım. Termik resetli ve start butonuna basılmış, motoru çalıştıran kontaktör çekili iken motor kablolarını çıkardığın yerden voltaj ölçümü yap. Fazlar arasında yaklaşık 375 ile 405 volt arası bir değer ölçmen lazım. Çıkan sonuç verdiğim değerler arasında ise stop butonuna bas, termiği kapat ve motor kablolarını çıkardığın yere çıkardığın sıralama ile bağla.",
    buttons: ["Voltaj değerleri normal", "Voltaj değerleri normal değil"]
  },
  "Bir süre sonra atıyor2": {
    text: "Kablo veya bağlantı noktalarında kaçak akım olabilir. Kabloları ve bağlantı noktalarını dikkatlice kontrol edin.",
    buttons: []
  },
  "Hemen atıyor2": {
    text: "Pano tarafında kısa devre var. Kontaktör, termik ve bağlantı noktalarını kontrol edin.",
    buttons: []
  },
  "Voltaj değerleri normal": {
    text: "Kabloları çıkardığın yere bağlarken sıralamaya dikkat ettiğini varsayıyorum. Şimdi motorun yanına git ve motora bak, anormal bir durum var mı? Yakından kokla, eğer yanıksa yanık kokusunu hissedebilirsin. Sonra yapabiliyorsan motor el ile dönüyor mu kontrol et.",
    buttons: ["Motor elle dönüyor", "Motor elle dönmüyor"]
  },
  "Voltaj değerleri normal değil": {
    text: "Pano besleme hattında sorun var. Sigortaları, kablo bağlantılarını ve şebeke gelişini kontrol edin.",
    buttons: []
  },
  "Motor elle dönüyor": {
    text: "Şimdi klemens kapağını aç ve yine kablo sıralamasına dikkat ederek kabloları çıkarıp motordan ayır.

Burası çok önemli, şimdi söyleyeceğim şeyleri yaparken çok dikkatli olmalısın. Kabloları motordan ayırdıktan sonra kablo boşta ve herhangi bir ucunun sana, herhangi bir yere veya birbirine temas etmediğinden emin ol. Termiği resetle ve start butonuna bas, sonra motorun yanında motordan çıkardığın kabloları çok dikkatli bir şekilde ölç. Yine fazlar arasında 375 ile 405 volt arasında değerler görmen lazım.",
    buttons: ["Voltaj değerleri normal2", "Voltaj değerleri normal değil2"]
  },
  "Motor elle dönmüyor": {
    text: "Motor mekanik olarak kilitlenmiş olabilir. Motor yataklarını veya bağlı olduğu yükü kontrol edin. Motor içi arıza da olabilir, servis gerekebilir.",
    buttons: []
  },
  "Voltaj değerleri normal2": {
    text: "Şimdi öncelikle ölçü aleti ile motorun sağlamlık kontrolünü yap. Ölçü aletini buzzer konumuna al. Önce motor klemensindeki üç ya da altı uç ile gövde arasında ölçüm yap, sonra da fazlar arasında yap ölçümü.

Yanık bir motorda genellikle uçlardan bir veya birkaçında gövde ile kısa devre olur ya da fazlar arasında bir faz değer göstermez veya fazlardan bir tanesi diğer ikisine göre çok farklı bir değer gösterir; bu motorun yanık olduğu anlamına gelir. Etiket bilgisine dikkat ederek motoru değiştir.

Sağlam bir motorda fazlar arasındaki direnç değerleri birbirine yakın ve uçlar ile gövde arasında herhangi bir kısa devre olmaz.",
    buttons: []
  },
  "Voltaj değerleri normal değil2": {
    text: "Kablo hattında sorun var. Motordan panoya giden kabloyu kontrol edin, kopukluk veya kaçak olabilir.",
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
