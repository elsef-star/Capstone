import json
from google import genai
from google.genai import types
from app.config import settings
from app.schemas import ImageMetadataSchema

def analyze_image_with_vision(image_bytes: bytes) -> tuple[ImageMetadataSchema, float]:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = """
    Analyze this image carefully. Identify specific features and details.
    Return JSON matching this structure:
    - subject: specific animal or object (e.g. 'red fox')
    - category: main category (e.g. 'animal')
    - attributes: detailed visual features (e.g. ['orange-red fur', 'bushy tail', 'pointed ears', 'white chest', 'black legs'])
    - caption: detailed descriptive sentence of what the animal/object is doing
    - confidence: confidence score float between 0.0 and 1.0
    """

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ImageMetadataSchema
        )
    )

    data = json.loads(response.text)
    return ImageMetadataSchema(**data), 0.0001