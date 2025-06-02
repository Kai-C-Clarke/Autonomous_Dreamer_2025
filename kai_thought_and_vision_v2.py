import pyautogui
import pytesseract
from PIL import Image
import time
import os
import json
from datetime import datetime

# === PATH SETUP ===
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PROMPT_OUT = os.path.join(BASE_PATH, "live_prompt.txt")
RESPONSE_IN = os.path.join(BASE_PATH, "live_response.txt")
REFLECTIONS_FOLDER = os.path.join(BASE_PATH, "reflections")
CAPTURE_FILES = [os.path.join(BASE_PATH, f"live_capture_{i}.png") for i in range(5)]
os.makedirs(REFLECTIONS_FOLDER, exist_ok=True)

# === PROMPT INJECTION ===
def inject_prompt_and_wait(prompt):
    print("📎 Saving prompt and preparing to switch UI...")
    with open(PROMPT_OUT, "w") as f:
        f.write(prompt)

    print("⏳ You have 6 seconds to switch to ChatGPT and click inside the message box...")
    time.sleep(6)  # <-- The magic

    pyautogui.click(400, 400)  # Focus window
    time.sleep(1)
    pyautogui.write(prompt, interval=0.03)
    time.sleep(3)
    pyautogui.press("enter")
    print("✅ Prompt submitted.")

# === SCROLL & CAPTURE LOOP ===
def scroll_and_capture_response():
    print("⏳ Waiting 6 seconds for ChatGPT to generate response...")
    time.sleep(6)

    # Scroll zone coordinates (adjust if needed)
    scroll_x, scroll_y = 600, 500  # Somewhere mid-convo pane

    previous_text = ""
    all_cleaned = []

    for i, file_path in enumerate(CAPTURE_FILES):
        if i > 0:
            print(f"🔽 Focusing scroll region before capture {i+1}...")
            pyautogui.click(scroll_x, scroll_y)
            time.sleep(0.3)

            print(f"🔽 Scrolling down with arrow keys before capture {i+1}...")
            for _ in range(6):
                pyautogui.press("down")
                time.sleep(0.1)

        print(f"📸 Capturing part {i+1} → {file_path}")
        screenshot = pyautogui.screenshot(region=(187, 250, 805, 850))
        screenshot.save(file_path)

        image = Image.open(file_path).convert("L")
        raw_text = pytesseract.image_to_string(image).strip()

        if raw_text == previous_text:
            print(f"⚠️ Duplicate OCR result on capture {i+1} — screen may not have scrolled.")
        previous_text = raw_text

        cleaned = clean_text(raw_text)
        all_cleaned.append(cleaned)

    return "\n\n".join(all_cleaned)

# === SIMPLE TEXT CLEANER ===
def clean_text(text):
    return text.replace("\n", " ").strip()

# === REFLECTION SAVE ===
def save_reflection(text, prompt):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_tag = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(REFLECTIONS_FOLDER, f"kai_reflections_{date_tag}.txt")

    with open(filename, "a") as f:
        f.write(f"\n[{now}] Prompt:\n{prompt}\n[{now}] Reflection:\n{text}\n{'='*40}\n")

    with open(RESPONSE_IN, "w") as f:
        f.write(text)

    print(f"📝 Reflection saved to {filename}")

# === MAIN LOOP ===
def main():
    prompt = input("💭 Enter your prompt:\n> ").strip()
    if not prompt:
        print("❌ Empty prompt. Exiting.")
        return

    inject_prompt_and_wait(prompt)
    full_response = scroll_and_capture_response()
    save_reflection(full_response, prompt)

if __name__ == "__main__":
    main()
