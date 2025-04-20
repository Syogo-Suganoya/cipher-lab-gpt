import os
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image

GEMINI_KEY = os.environ.get("GEMINI_KEY")


def query(prompt):
    try:
        client = genai.Client(api_key=GEMINI_KEY)
        response = client.models.generate_content(
            # model="gemini-2.0-flash",
            model="gemini-2.0-flash-lite",
            # model="gemini-2.0-pro-exp-02-05",
            contents=prompt,
        )
    except Exception as e:
        print(f"Gemini APIエラー: {e}")
        return None

    output_text = response.text
    return output_text.strip()


def image_genrate(contents, directory):
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = f"{contents}\n- スタイル: 手書きイラスト"

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation", contents=prompt, config=types.GenerateContentConfig(response_modalities=["Text", "Image"])
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(os.path.join(directory, "image.jpeg"))


def image_genrate_imagen3(contents, directory):
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = f"{contents}\n- スタイル: 手書きイラスト"

    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        ),
    )
    if response.generated_images:
        generated_image = response.generated_images
        image = Image.open(BytesIO(generated_image.image.image_bytes))
        image.save(os.path.join(directory, "image.jpeg"))
