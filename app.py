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
        "buttons": ["220 Volt", "380 Volt", ""]
    },
    "380 Volt": {
        "text": "Bu motor neyle çalışıyor?",
        "buttons": ["Kontaktör", "Sürücü", "Softstarter"]
    },
    "220 Volt": {
        "text": "220 volt motorlarda kondansatör arızası sık görülür.",
        "buttons": ["", "", ""]
    },
    "Kontaktör": {
        "text": "Termik atmış mı?",
        "buttons": ["Evet", "Hayır", ""]
    },
    "Sürücü": {
        "text": "Sürücü ekranında hata var mı?",
        "buttons": ["Var", "Yok", ""]
    },
    "Softstarter": {
        "text": "Softstarter hata ışığı yanıyor mu?",
        "buttons": ["Evet", "Hayır", ""]
    },
    "Evet": {
        "text": "Termiği resetleyip tekrar deneyin.",
        "buttons": ["", "", ""]
    },
    "Hayır": {
        "text": "Motor klemensinde 3 faz var mı?",
        "buttons": ["Var", "Yok", ""]
    },
    "Var": {
        "text": "Motor sıkışmış olabilir.",
        "buttons": ["", "", ""]
    },
    "Yok": {
        "text": "Sigorta veya kabloyu kontrol edin.",
        "buttons": ["", "", ""]
    }
}

def make_button_html(node_key):
    if node_key is None:
        return gr.update(value="", visible=False)
    btns = dialog_tree[node_key]["buttons"]
    active = [b for b in btns if b]
    if not active:
        return gr.update(value="", visible=False)
    
    html = '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;">'
    for btn in active:
        html += f'''<button onclick="
            document.getElementById('hidden_input').value='{btn}';
            document.getElementById('hidden_btn').click();
        " style="padding:10px 20px;font-size:16px;border:2px solid #666;border-radius:8px;background:#f0f0f0;cursor:pointer;">{btn}</button>'''
    html += '</div>'
    return gr.update(value=html, visible=True)

def add_msg(history, user_text, bot_text):
    history = history or []
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": bot_text})
    return history

def handle_text_input(user_text, history):
    if not user_text or not user_text.strip():
        return history, None, make_button_html(None), gr.update(visible=True)
    user_text_lower = user_text.strip().lower()
    matched = any(trigger in user_text_lower for trigger in TRIGGERS)
    if matched:
        history = add_msg([], user_text.strip(), dialog_tree["start"]["text"])
        return history, "start", make_button_html("start"), gr.update(visible=False)
    else:
        history = add_msg(history or [], user_text.strip(), "⚠️ Lütfen arızayı daha açık belirtin. Örnek: 'Motor çalışmıyor'")
        return history, None, make_button_html(None), gr.update(visible=True)

def handle_choice(choice_text, history, state):
    if not choice_text or not choice_text.strip():
        return history, state, make_button_html(state), ""
    choice = choice_text.strip()
    if state is None:
        return history, state, make_button_html(None), ""
    node_data = dialog_tree.get(state)
    if not node_data or choice not in node_data["buttons"]:
        return history, state, make_button_html(state), ""
    next_node = dialog_tree.get(choice)
    if not next_node:
        return history, state, make_button_html(None), ""
    history = add_msg(history or [], choice, next_node["text"])
    return history, choice, make_button_html(choice), ""

def reset_chat():
    return [], None, make_button_html(None), gr.update(visible=True), ""

with gr.Blocks(title="AI Elektrik Bakım Ustası") as demo:
    gr.Markdown("# 🔧 AI Elektrik Bakım Ustası")
    gr.Markdown("Arızayı aşağıya yazın, size adım adım yardımcı olalım.")

    chatbot = gr.Chatbot(height=450, type="messages")
    state = gr.State()

    btn_area = gr.HTML(value="", visible=False)

    # Gizli input ve buton - HTML butonlarından tetiklenir
    with gr.Row(visible=False):
        hidden_input = gr.Textbox(elem_id="hidden_input")
        hidden_btn = gr.Button("hidden", elem_id="hidden_btn")

    with gr.Row() as input_row:
        text_input = gr.Textbox(
            placeholder="Örnek: Motor çalışmıyor...",
            label="Arızayı Yazın",
            scale=4
        )
        send_btn = gr.Button("Gönder", scale=1, variant="primary")

    reset = gr.Button("🔄 Sıfırla", variant="secondary")

    send_btn.click(handle_text_input,
        inputs=[text_input, chatbot],
        outputs=[chatbot, state, btn_area, input_row])

    text_input.submit(handle_text_input,
        inputs=[text_input, chatbot],
        outputs=[chatbot, state, btn_area, input_row])

    hidden_btn.click(handle_choice,
        inputs=[hidden_input, chatbot, state],
        outputs=[chatbot, state, btn_area, hidden_input])

    reset.click(reset_chat,
        outputs=[chatbot, state, btn_area, input_row, text_input])

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
