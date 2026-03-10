import gradio as gr
import os
os.environ["GRADIO_DEFAULT_LANG"] = "en"

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
        "buttons": ["Kontaktor", "Invertor", "Softstarter"]
    },
    "220 Volt": {
        "text": "220 volt motorlarda kondansatör arızası sık görülür.",
        "buttons": []
    },
    "Kontaktor": {
        "text": "Termik atmış mı?",
        "buttons": ["Evet", "Hayir"]
    },
    "Invertor": {
        "text": "Invertor ekranında hata var mı?",
        "buttons": ["Var", "Yok"]
    },
    "Softstarter": {
        "text": "Softstarter hata ışığı yanıyor mu?",
        "buttons": ["Evet", "Hayir"]
    },
    "Evet": {
        "text": "Termiği resetleyip tekrar deneyin.",
        "buttons": []
    },
    "Hayir": {
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

def add_msg(history, user_text, bot_text):
    history = history or []
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": bot_text})
    return history

def handle_text_input(user_text, history):
    if not user_text or not user_text.strip():
        return history, None, gr.update(choices=[""], visible=False, value=None), gr.update(visible=True)
    user_text_lower = user_text.strip().lower()
    matched = any(trigger in user_text_lower for trigger in TRIGGERS)
    if matched:
        history = add_msg([], user_text.strip(), dialog_tree["start"]["text"])
        choices = dialog_tree["start"]["buttons"]
        return history, "start", gr.update(choices=choices, visible=True, value=None), gr.update(visible=False)
    else:
        history = add_msg(history or [], user_text.strip(), "⚠️ Lütfen arızayı daha açık belirtin. Örnek: 'Motor çalışmıyor'")
        return history, None, gr.update(choices=[""], visible=False, value=None), gr.update(visible=True)

def handle_choice(choice, history, state):
    if not choice or state is None:
        return history, state, gr.update(choices=[""], visible=False, value=None)
    node_data = dialog_tree.get(state)
    if not node_data or choice not in node_data["buttons"]:
        return history, state, gr.update(choices=[""], visible=False, value=None)
    next_node = dialog_tree.get(choice)
    if not next_node:
        return history, state, gr.update(choices=[""], visible=False, value=None)
    history = add_msg(history or [], choice, next_node["text"])
    choices = next_node["buttons"]
    if choices:
        return history, choice, gr.update(choices=choices, visible=True, value=None)
    else:
        return history, choice, gr.update(choices=[""], visible=False, value=None)

def reset_chat():
    return [], None, gr.update(choices=[""], visible=False, value=None), gr.update(visible=True), ""

with gr.Blocks(title="AI Elektrik Bakim Ustasi") as demo:
    gr.Markdown("# 🔧 AI Elektrik Bakım Ustası")
    gr.Markdown("Arızayı aşağıya yazın, size adım adım yardımcı olalım.")

    chatbot = gr.Chatbot(height=450, type="messages")
    state = gr.State()

    choice_radio = gr.Radio(
        choices=[""],
        label="Seciminizi yapin:",
        visible=False,
        value=None
    )

    with gr.Row() as input_row:
        text_input = gr.Textbox(
            placeholder="Ornek: Motor calismiyor...",
            label="Arizayi Yazin",
            scale=4
        )
        send_btn = gr.Button("Gonder", scale=1, variant="primary")

    reset = gr.Button("Sifirla", variant="secondary")

    send_btn.click(handle_text_input,
        inputs=[text_input, chatbot],
        outputs=[chatbot, state, choice_radio, input_row])

    text_input.submit(handle_text_input,
        inputs=[text_input, chatbot],
        outputs=[chatbot, state, choice_radio, input_row])

    choice_radio.select(handle_choice,
        inputs=[choice_radio, chatbot, state],
        outputs=[chatbot, state, choice_radio])

    reset.click(reset_chat,
        outputs=[chatbot, state, choice_radio, input_row, text_input])

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
