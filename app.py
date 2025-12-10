import gradio as gr
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image
import time

# -------------------------
# Helper: Plot Array to PIL Image
# -------------------------
def plot_array(arr, highlight=None):
    fig, ax = plt.subplots(figsize=(6,3), dpi=120)
    x = np.arange(len(arr))
    bars = ax.bar(x, arr, color="skyblue", edgecolor="black")

    if highlight is not None:
        i, j = highlight
        if 0 <= i < len(arr):
            bars[i].set_color("orange")
        if 0 <= j < len(arr):
            bars[j].set_color("red")

    ax.set_title("Bubble Sort Progress")
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_xticks(x)
    ax.set_ylim(0, max(arr)+2 if arr else 1)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# -------------------------
# Bubble Sort Logic
# -------------------------
def is_sorted(arr):
    return all(arr[k] <= arr[k+1] for k in range(len(arr)-1))

def generate_list(n=6):
    arr = random.sample(range(1, 20), n)
    state = {"array": arr, "pass": 0, "i": 0, "done": False, "steps": 0, "history": []}
    img = plot_array(arr, highlight=(0,1) if len(arr)>1 else None)
    feedback = f"New list generated: {arr}"
    state["history"].append(f"Step 0: {feedback}")
    return state, feedback, arr, img, f"Steps: 0", "\n".join(state["history"])

def bubble_step(state, user_swap):
    arr = state["array"]
    p, i = state["pass"], state["i"]

    if state["done"]:
        img = plot_array(arr)
        return state, "Sorting is already complete!", arr, img, f"Steps: {state['steps']}", "\n".join(state["history"])

    j = i+1
    needed_swap = arr[i] > arr[j]

    # Apply user's choice with detailed feedback
    if user_swap == "Swap":
        if needed_swap:
            arr[i], arr[j] = arr[j], arr[i]
            feedback = f"Correct! {arr[j]} was greater than {arr[i]}, so swapping fixed the order."
            advance = True
        else:
            feedback = f"Incorrect. {arr[i]} and {arr[j]} are already in the right order.\nTry again: swapping here would break the ascending order."
            advance = False
    else:  # "Don't Swap"
        if not needed_swap:
            feedback = f"Correct! {arr[i]} ≤ {arr[j]}, so no swap was needed."
            advance = True
        else:
            feedback = f"Incorrect. {arr[i]} is greater than {arr[j]}, so leaving them would keep the array unsorted.\nTry again: not swapping here would break the ascending order."
            advance = False

    # Only advance if the choice was correct
    if advance:
        i += 1
        if i >= len(arr) - p - 1:
            p += 1
            i = 0

    # Check completion
    if is_sorted(arr):
        state["done"] = True
        feedback += "\nSorting complete! 🎉"

    state["array"], state["pass"], state["i"] = arr, p, i
    state["steps"] += 1
    state["history"].append(f"Step {state['steps']}: {feedback} → {arr}")

    img = plot_array(arr, highlight=None if state["done"] else (i, i+1))
    return state, feedback, arr, img, f"Steps: {state['steps']}", "\n".join(state["history"])

# -------------------------
# Auto Sort Generator
# -------------------------
def auto_sort(state):
    arr = state["array"]
    n = len(arr)
    for p in range(n-1):
        for i in range(n-p-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                feedback = f"Swapped {arr[i]} and {arr[i+1]}"
            else:
                feedback = f"No swap needed for {arr[i]} and {arr[i+1]}"
            state["steps"] += 1
            state["history"].append(f"Step {state['steps']}: {feedback} → {arr}")
            img = plot_array(arr, highlight=(i, i+1))
            yield state, feedback, arr.copy(), img, f"Steps: {state['steps']}", "\n".join(state["history"])
            time.sleep(0.25) # Slightly increased delay for better visibility
    state["done"] = True
    feedback = "Auto sort complete! 🎉"
    state["history"].append(f"Step {state['steps']}: {feedback}")
    img = plot_array(arr)
    yield state, feedback, arr, img, f"Steps: {state['steps']}", "\n".join(state["history"])

# -------------------------
# Gradio UI
# -------------------------
with gr.Blocks() as demo:
    gr.Markdown("# Bubble Sort Game\nLearn Bubble Sort by making the right swap decisions!")

    state = gr.State()

    # Large buttons for Generate and Auto Sort
    with gr.Row():
        generate_btn = gr.Button("Generate New List", scale=1)
        auto_btn = gr.Button("Auto Sort", scale=1)


    array_display = gr.JSON(label="Current Array")
    visual_display = gr.Image(label="Array Visualization", type="pil")
    feedback_box = gr.Textbox(label="Feedback", interactive=False, lines=2)
    step_tracker = gr.Textbox(label="Step Tracker", interactive=False)
    history_box = gr.Textbox(label="History Log", interactive=False, lines=12)

    # Large buttons for Swap / Don't Swap
    with gr.Row():
        swap_btn = gr.Button("Swap", scale=1)
        dont_swap_btn = gr.Button("Don't Swap", scale=1)

    # Wire buttons
    generate_btn.click(
        fn=generate_list,
        outputs=[state, feedback_box, array_display, visual_display,step_tracker, history_box]
    )

    swap_btn.click(
        fn=bubble_step,
        inputs=[state, gr.Textbox(value="Swap", visible=False)],
        outputs=[state, feedback_box, array_display, visual_display, step_tracker, history_box]
    )

    dont_swap_btn.click(
        fn=bubble_step,
        inputs=[state, gr.Textbox(value="Don't Swap", visible=False)],
        outputs=[state, feedback_box, array_display, visual_display, step_tracker, history_box]
    )

    auto_btn.click(
        fn=auto_sort,
        inputs=[state],
        outputs=[state, feedback_box, array_display, visual_display, step_tracker, history_box]
    )

# -------------------------
# Launch immediately
# -------------------------
demo.launch()
