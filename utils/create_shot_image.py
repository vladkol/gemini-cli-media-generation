# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from datetime import datetime, timezone
import mimetypes
import os
import sys
import typing

from google import genai
from google.genai import types

from dotenv import load_dotenv

USE_VAI_OVERRIDE = False

def save_binary_file(file_path, data):
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"\n\n==== 🌠 Image saved to to: {file_path} ====\n\n")

def load_image_file(file_path: str) -> types.Part:
    ext = file_path.lower().rsplit(".", 1)[-1]
    if ext not in ["jpg", "jpeg", "png"]:
        raise ValueError("Image file must be be JPEG or PNG")
    with open(file_path, "rb") as f:
        data = f.read()
    if ext == "png":
        mime_type = "image/png"
    else:
        mime_type = "image/jpeg"
    return types.Part.from_bytes(
        mime_type=mime_type,
        data=data,
    )

def generate(args: typing.Sequence[str]):
    parser = argparse.ArgumentParser(
        description="Gemini 2.5 Image Generator"
    )

    parser.add_argument(
        "--source-image",
        help="Source image.",
        type=str,
        required=False,
        default=None
    )
    parser.add_argument(
        "--prompt",
        help="Image Generation Prompt.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output-directory",
        help="Directory path to save the image to.",
        type=str,
        required=False,
        default="."
    )
    parser.add_argument(
        "--output-name-prefix",
        help="Result file name prefix",
        type=str,
        required=False,
        default="generated-image-"
    )
    parser.add_argument(
        "--model",
        help="Image Generation Model.",
        type=str,
        required=False,
        default=os.environ.get(
            "MM_MODEL_NAME",
            "gemini-2.5-flash-preview-image-08-25"
        )
    )

    options = parser.parse_args(args)

    client = genai.Client(
        vertexai=False,
        api_key=os.environ["GEMINI_API_KEY"]
    )
    model = options.model
    parts = [
        load_image_file(options.source_image)
    ] if options.source_image else []
    parts.append(
        types.Part.from_text(text=options.prompt)
    )
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
        candidate_count=1,
        temperature=0.5,
    )


    for chunk in client.models.generate_content_stream(
        model=model,
        contents=types.Content(parts=parts),
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if (
            chunk.candidates[0].content.parts[0].inline_data
            and chunk.candidates[0].content.parts[0].inline_data.data
        ):
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(
                inline_data.mime_type  # type: ignore
            )
            suffix = datetime.now(
                timezone.utc
            ).strftime("%Y%m%d-%H%M%S-%f")[:-3]
            file_name = f"{options.output_name_prefix}-{suffix}{file_extension}"
            file_path = os.path.join(
                options.output_directory,
                file_name
            )
            save_binary_file(file_path, data_buffer)
        else:
            print(chunk.text)

if __name__ == "__main__":
    load_dotenv()
    generate(sys.argv[1:])
