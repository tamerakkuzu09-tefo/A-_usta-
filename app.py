import os
import gradio as gr

# Varsayıyorum ki handle_text_input, choose ve reset_chat fonksiyonları 
# dosyanın daha üst kısmında tanımlı (kodunu paylaşmadığın için onları değiştirmedim)

def reset_chat():
    return [], None, *update_buttons([]), gr.update(visible=True), ""

# -------------------------
# Arayüz
# -------------------------

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
        b1 = gr.Button(visible=False)
        b2 = gr.Button(visible=False)
        b3 = gr.Button(visible=False)

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

    b1.click(choose, inputs=[b1, chatbot], outputs=[chatbot, state, b1, b2, b3])
    b2.click(choose, inputs=[b2, chatbot], outputs=[chatbot, state, b1, b2, b3])
    b3.click(choose, inputs=[b3, chatbot], outputs=[chatbot, state, b1, b2, b3])

    reset.click(
        reset_chat,
        outputs=[chatbot, state, b1, b2, b3, input_row, text_input]
    )

# Railway için doğru launch ayarları
demo.queue().launch(           # queue eklemek chatbot için faydalı
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False,
    debug=False
)
