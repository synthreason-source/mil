import gradio as gr
import random

def roll_dice():
    # Generate a random integer between 1 and 99 (inclusive)
    roll = random.randint(1, 999)
    
    # Check if the roll hits the 1-in-99 target (e.g., the number 1)
    if roll == 1:
        # Pass a dictionary to the Gradio Label for visual confidence bars
        label = {"Success 🎉": 1.0, "Failure ❌": 0.0}
        message = f"Jackpot! You rolled a {roll}."
    else:
        label = {"Failure ❌": 1.0, "Success 🎉": 0.0}
        message = f"You rolled a {roll}. Better luck next time."
        
    return message, label

# Build the Gradio UI
with gr.Blocks(theme=gr.themes.Monochrome()) as app:
    gr.Markdown("## 1-in-999 Dice Roller")
    gr.Markdown("Click the button to roll a 99-sided die. You only attack your enemy if you roll a 1.")
    
    with gr.Row():
        roll_btn = gr.Button("Roll Dice", variant="primary")
        
    with gr.Row():
        result_msg = gr.Textbox(label="Raw Roll Result", interactive=False)
        result_label = gr.Label(label="Outcome Status")
        
    # Link the button click to the roll_dice function
    roll_btn.click(fn=roll_dice, inputs=[], outputs=[result_msg, result_label])

if __name__ == "__main__":
    app.launch()
