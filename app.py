import gradio as gr

TRIGGERS = [
    "motor çalışmıyor",
    "motor arızalı",
    "calismiyor",
    "çalışmıyor",
    "motor start almıyor"
]

dialog_tree = {
    "start": {
        "text": "Bu motor kaç voltta çalışıyor?",
        "buttons": ["220 Volt", "380 Volt"]
    },
    "380 Volt": {
        "text": "Bu motor neyle çalışıyor?",
        "buttons": ["Kontaktör", "Invertör", "Softstarter"]
    },
    "220 Volt": {
        "text": "220 volt motorlarda kondansatör arızası sık görülür. Kondansatörü kontrol edin.",
        "buttons": []
    },
    "Kontaktör": {
        "text": "Termik atmış mı?",
        "buttons": ["Evet", "Hayır"]
    },
    "Invertör": {
        "text": "Invertör ekranında hata kodu var mı?",
        "buttons": ["Var", "Yok"]
    },
    "Softstarter": {
        "text": "Softstarter hata ışığı yanıyor mu?",
        "buttons": ["Evet", "Hayır"]
    },
    "Evet": {
        "text": "Termiği resetleyip tekrar deneyin.",
        "buttons": []
    },
    "Hayır": {
        "text": "Motor klemensinde 3 faz var mı?",
        "buttons": ["Var", "Yok"]
    },
    "Var": {
        "text": "Motor sıkışmış olabilir. Yükü kontrol edin.",
        "buttons": []
    },
    "Yok": {
        "text": "Sigorta veya kabloyu kontrol edin.",
        "buttons": []
    }
}

def make_options_text(buttons):
    if not buttons:
        return ""
    lines = []
    for b in buttons:
        lines.append(f"👉 **{b}** yazmak için kutucuğa **{b}** yazın")
    return "\n\n" + "\n".join(lines)

def add_msg(history, user_text, bot_text):
    history = history or []
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": bot_text})
    return history

def find_matching_button(text, buttons):
    text_lower = text.strip().lower()
    for b in buttons:
        if b.lower() in text_lower or text_lower in b.lower():
            return b
    return None

def chat(user_text, history, state):
    if not user_text or not user_text.strip():
        return history, state, ""

    user_text_stripped = user_text.strip()
    user_lower = user_text_stripped.lower()
    history = history or []

    # Eğer state yoksa — tetikleyici kelime ara
    if state is None:
        matched = any(trigger in user_lower for trigger in TRIGGERS)
        if matched:
            node = dialog_tree["start"]
            bot_text = node["text"] + make_options_text(node["buttons"])
            history = add_msg([], user_text_stripped, bot_text)
            return history, "start", ""
        else:
            history = add_msg(history, user_text_stripped,
                "⚠️ Lütfen arızayı daha açık belirtin.\nÖrnek: **Motor çalışmıyor**")
            return history, None, ""

    # State varsa — mevcut node'un butonlarıyla eşleştir
    node_data = dialog_tree.get(state, {})
    buttons = node_data.get("buttons", [])

    match = find_matching_button(user_text_stripped, buttons)

    if match:
        next_node = dialog_tree.get(match, {})
        bot_text = next_node.get("text", "")
        next_buttons = next_node.get("buttons", [])
        if next_buttons:
            bot_text += make_options_text(next_buttons)
        history = add_msg(history, user_text_stripped, bot_text)
        return history, match, ""
    else:
        options = make_options_text(buttons)
        history = add_msg(history, user_text_stripped,
            f"❓ Anlamadım. Lütfen aşağıdaki seçeneklerden birini yazın:{options}")
        return history, state, ""

def reset_chat():
    return [], None, ""

with gr.Blocks(title="AI Elektrik Bakım Ustası") as demo:
    gr.Markdown("# 🔧 AI Elektrik Bakım Ustası")
    gr.Markdown("Arızayı aşağıya yazın, size adım adım yardımcı olalım.")

    chatbot = gr.Chatbot(height=500, type="messages")
    state = gr.State()

    with gr.Row():
        text_input = gr.Textbox(
            placeholder="Örnek: Motor çalışmıyor...",
            label="",
            scale=4,
            autofocus=True
        )
        send_btn = gr.Button("Gönder", scale=1, variant="primary")

    reset = gr.Button("🔄 Sıfırla", variant="secondary")

    send_btn.click(chat,
        inputs=[text_input, chatbot, state],
        outputs=[chatbot, state, text_input])

    text_input.submit(chat,
        inputs=[text_input, chatbot, state],
        outputs=[chatbot, state, text_input])

    reset.click(reset_chat,
        outputs=[chatbot, state, text_input])

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
