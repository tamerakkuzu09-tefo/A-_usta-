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
        "buttons": ["Kontaktör", "Sürücü", "Softstarter"]
    },
    "220 Volt": {
        "text": "220 volt motorlarda kondansatör arızası sık görülür.",
        "buttons": []
    },
    "Kontaktör": {
        "text": "Termik atmış mı?",
        "buttons": ["Evet", "Hayır"]
    },
    "Sürücü": {
        "text": "Sürücü ekranında hata var mı?",
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
        "text": "Motor sıkışmış olabilir.",
        "buttons": []
    },
    "Yok": {
        "text": "Sigorta veya kabloyu kontrol edin.",
        "buttons": []
    }
}

def update_buttons(buttons):
    updates = []
    for i in range(3):
        if i < len(buttons):
            updates.append(gr.update(value=buttons[i], visible=True))
        else:
            updates.append(gr.update(value="-", visible=False))
    return updates

def handle_text_input(user_text, history):
    if not user_text or not user_text.strip():
        return history, None, *update_buttons([]), gr.update(visible=True)

    user_text_lower = user_text.strip().lower()
    history = history or []
    matched = any(trigger in user_text_lower for trigger in TRIGGERS)

    if matched:
        history = [(user_text.strip(), dialog_tree["start"]["text"])]
        buttons = dialog_tree["start"]["buttons"]
        return history, "start", *update_buttons(buttons), gr.update(visible=False)
    else:
        history = history + [(user_text.strip(), "⚠️ Lütfen arızayı daha açık belirtin. Örnek: 'Motor çalışmıyor'")]
        return history, None, *update_buttons([]), gr.update(visible=True)

def btn1_click(history, state):
    if state is None:
        return history, state, *update_buttons([])
    node_data = dialog_tree.get(state)
    if not node_data or len(node_data["buttons"]) < 1:
        return history, state, *update_buttons([])
    choice = node_data["buttons"][0]
    return _process_choice(choice, history)

def btn2_click(history, state):
    if state is None:
        return history, state, *update_buttons([])
    node_data = dialog_tree.get(state)
    if not node_data or len(node_data["buttons"]) < 2:
        return history, state, *update_buttons([])
    choice = node_data["buttons"][1]
    return _process_choice(choice, history)

def btn3_click(history, state):
    if state is None:
        return history, state, *update_buttons([])
    node_data = dialog_tree.get(state)
    if not node_data or len(node_data["buttons"]) < 3:
        return history, state, *update_buttons([])
    choice = node_data["buttons"][2]
    return _process_choice(choice, history)

def _process_choice(choice, history):
    history = history or []
    node = dialog_tree.get(choice)
    if not node:
        return history, None, *update_buttons([])
    history = history + [(choice, node["text"])]
    buttons = node["buttons"]
    return history, choice, *update_buttons(buttons)

def reset_chat():
    return [], None, *update_buttons([]), gr.update(visible=True), ""

with gr.Blocks(title="AI Elektrik Bakım Ustası") as demo:

    gr.Markdown("# 🔧 AI Elektrik Bakım Ustası")
    gr.Markdown("Arızayı aşağıya yazın, size adım adım yardımcı olalım.")

    chatbot = gr.Chatbot(height=450)
    state = gr.State()

    with gr.Row() as input_row:
        text_input = gr.Textbox(
            placeholder="Örnek: Motor çalışmıyor...",
            label="Arızayı Yazın",
            scale=4
        )
        send_btn = gr.Button("Gönder", scale=1, variant="primary")

    with gr.Row():
        b1 = gr.Button("...", visible=False)
        b2 = gr.Button("...", visible=False)
        b3 = gr.Button("...", visible=False)

    reset = gr.Button("🔄 Sıfırla", variant="secondary")

    send_btn.click(
        handle_text_input,
        inputs=[text_input, chatbot],
        outputs=[chatbot, state, b1, b2, b3, input_row]
    )

    text_input.submit(
        handle_text_input,
        inputs=[text_input, chatbot],
        outputs=[chatbot, state, b1, b2, b3, input_row]
    )

    b1.click(btn1_click, inputs=[chatbot, state], outputs=[chatbot, state, b1, b2, b3])
    b2.click(btn2_click, inputs=[chatbot, state], outputs=[chatbot, state, b1, b2, b3])
    b3.click(btn3_click, inputs=[chatbot, state], outputs=[chatbot, state, b1, b2, b3])

    reset.click(
        reset_chat,
        outputs=[chatbot, state, b1, b2, b3, input_row, text_input]
    )

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
