import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def process_path(input_path, output_dir, scale=4, mode="fast", progress_callback=None):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if scale not in (2, 4):
        raise ValueError("放大倍率只支持 2x 或 4x。")

    files = collect_images(input_path)
    if not files:
        raise ValueError("没有找到可处理的图片。支持 JPG、JPEG、PNG、WEBP。")

    results = []
    for index, image_path in enumerate(files, start=1):
        output_path = make_output_path(image_path, output_dir, scale)
        message = f"正在处理：{image_path.name}"
        if progress_callback:
            progress_callback(index - 1, len(files), message)

        used_mode = upscale_image(image_path, output_path, scale=scale, mode=mode)
        results.append(str(output_path))

        if progress_callback:
            progress_callback(index, len(files), f"完成：{output_path.name}（{used_mode}）")

    return results


def collect_images(input_path):
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() in SUPPORTED_EXTENSIONS else []

    images = []
    for path in sorted(input_path.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(path)
    return images


def make_output_path(image_path, output_dir, scale):
    stem = image_path.stem
    output_path = output_dir / f"{stem}_upscale_{scale}x.png"
    counter = 2
    while output_path.exists():
        output_path = output_dir / f"{stem}_upscale_{scale}x_{counter}.png"
        counter += 1
    return output_path


def upscale_image(input_path, output_path, scale=4, mode="fast"):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if mode == "ai":
        ok = try_realesrgan_ncnn(input_path, output_path, scale)
        if ok:
            postprocess_fast(output_path, output_path, scale, already_upscaled=True)
            return "AI 高清模式"

    postprocess_fast(input_path, output_path, scale, already_upscaled=False)
    return "快速模式"


def try_realesrgan_ncnn(input_path, output_path, scale):
    executable = find_realesrgan_executable()
    if not executable:
        return False

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        temp_output = temp_dir / output_path.name
        command = [
            executable,
            "-i",
            str(input_path),
            "-o",
            str(temp_output),
            "-s",
            str(scale),
            "-n",
            "realesrgan-x4plus",
            "-f",
            "png",
        ]

        try:
            completed = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60 * 30,
            )
        except (OSError, subprocess.SubprocessError):
            return False

        if completed.returncode != 0 or not temp_output.exists():
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(temp_output), str(output_path))
        return True


def find_realesrgan_executable():
    env_path = os.environ.get("REALESRGAN_NCNN")
    candidates = []
    if env_path:
        candidates.append(env_path)

    names = [
        "realesrgan-ncnn-vulkan",
        "realesrgan-ncnn-vulkan.exe",
        "realesrgan-ncnn-vulkan.app",
    ]
    for name in names:
        found = shutil.which(name)
        if found:
            candidates.append(found)

    local_dirs = [
        Path.cwd(),
        Path.cwd() / "realesrgan-ncnn-vulkan",
        Path.cwd() / "models",
        Path(__file__).resolve().parent,
    ]
    for directory in local_dirs:
        for name in names:
            candidates.append(str(directory / name))

    for candidate in candidates:
        path = Path(candidate).expanduser()
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
    return None


def postprocess_fast(input_path, output_path, scale, already_upscaled=False):
    image = Image.open(input_path)
    image = ImageOps.exif_transpose(image)

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

    if not already_upscaled:
        new_size = (image.width * scale, image.height * scale)
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    image = denoise_image(image)
    image = optimize_contrast(image)
    image = sharpen_image(image, scale)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=True)


def denoise_image(image):
    has_alpha = image.mode == "RGBA"
    alpha = image.getchannel("A") if has_alpha else None
    rgb = image.convert("RGB")
    array = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)

    denoised = cv2.fastNlMeansDenoisingColored(
        array,
        None,
        h=3,
        hColor=3,
        templateWindowSize=7,
        searchWindowSize=21,
    )
    rgb_image = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
    if has_alpha:
        rgb_image.putalpha(alpha)
    return rgb_image


def optimize_contrast(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.04)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.02)
    return image


def sharpen_image(image, scale):
    radius = 1.0 if scale == 2 else 1.2
    percent = 120 if scale == 2 else 135
    threshold = 4
    image = image.filter(
        ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
    )
    return image
