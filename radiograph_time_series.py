
import openai
import base64

def compare_radiographs(labeled_images):
    vision_prompts = []
    for img_file, label in labeled_images:
        b64_img = base64.b64encode(img_file.getvalue()).decode("utf-8")
        vision_prompts.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64_img}"
            },
            "label": label
        })

    messages = [{"role": "user", "content": [
        {"type": "text", "text": "You're a dental radiologist AI. Compare these radiographs chronologically and describe:"},
        {"type": "text", "text": "• Changes in bone levels, lesions, or restorations"},
        {"type": "text", "text": "• Signs of healing or disease progression"},
        {"type": "text", "text": "• Relevant treatment suggestions or warnings"},
        *vision_prompts
    ]}]

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=1000
    )

    return response.choices[0].message["content"]
