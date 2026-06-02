# 本地图片高清放大工具

这是一个本地运行的图片放大和锐化小工具，适合处理 ChatGPT / AI 生成图、产品图、设计图、规格书图片和线稿图。程序不会上传图片，不调用付费 API。

## 功能

- 支持 JPG、JPEG、PNG、WEBP
- 支持单张图片和整个文件夹批量处理
- 支持 2x、4x 放大
- 快速模式：使用 Lanczos 插值、轻微降噪、对比度优化和锐化
- AI 高清模式：如果本机安装了 `realesrgan-ncnn-vulkan`，优先调用它；不可用时自动切换到快速模式
- 输出到 `output` 文件夹，文件名类似 `photo_upscale_4x.png`
- 保留原图，不覆盖原文件

## 安装 Python

### Mac

1. 打开 [Python 官网](https://www.python.org/downloads/)。
2. 下载 macOS 版本 Python 3.10 或更新版本。
3. 安装时保持默认选项即可。
4. 安装完成后，打开“终端”，输入：

```bash
python3 --version
```

能看到版本号就表示安装成功。

### Windows

1. 打开 [Python 官网](https://www.python.org/downloads/)。
2. 下载 Windows 版本 Python 3.10 或更新版本。
3. 安装第一步请勾选 `Add python.exe to PATH`。
4. 安装完成后，打开 PowerShell，输入：

```powershell
python --version
```

能看到版本号就表示安装成功。

## 安装依赖

在项目文件夹中打开终端或 PowerShell，执行：

Mac：

```bash
python3 -m pip install -r requirements.txt
```

Windows：

```powershell
python -m pip install -r requirements.txt
```

## 运行程序

Mac：

```bash
python3 main.py
```

Windows：

```powershell
python main.py
```

打开窗口后：

1. 把图片拖到网页中的上传区域，或者点击选择单张 / 多张图片。
2. 选择输出文件夹，默认是当前项目下的 `output`。
3. 选择 2x 或 4x。
4. 选择“快速模式”或“AI 高清模式”。
5. 点击 `CREATE` 确认开始处理。

新版使用本地网页界面，会在浏览器打开 `http://127.0.0.1:7860`。它仍然只在本地运行，不会上传图片到云端。

如果浏览器没有自动打开，可以手动复制这个地址到浏览器：

```bash
http://127.0.0.1:7860
```

## 批量处理 input 文件夹

你可以在项目文件夹中创建一个 `input` 文件夹，把要处理的图片放进去，然后运行程序并选择这个 `input` 文件夹。

也可以直接使用命令行批量处理：

Mac：

```bash
python3 main.py --input input --output output --scale 4 --mode fast
```

Windows：

```powershell
python main.py --input input --output output --scale 4 --mode fast
```

## AI 高清模式说明

本工具优先支持 `realesrgan-ncnn-vulkan`。它是本地运行的 Real-ESRGAN 方案，不需要付费 API。

如果电脑没有 GPU、没有安装 `realesrgan-ncnn-vulkan`、模型不可用或运行失败，程序会自动切换到快速模式，不会直接退出。

使用方式：

1. 下载适合你系统的 `realesrgan-ncnn-vulkan`。
2. 把可执行文件放到项目目录，或把它加入系统 PATH。
3. 也可以设置环境变量 `REALESRGAN_NCNN` 指向可执行文件路径。
4. 在程序中选择“AI 高清模式”。

## 常见问题

### 显存不足怎么办？

先改用 2x，或把大图裁成几块分别处理。也可以直接使用快速模式，速度更稳，对显卡没有要求。

### 图片太大处理很慢怎么办？

4x 会让像素数量变成原来的 16 倍。建议先用 2x 测试效果，确认没问题后再处理大图。

### AI 模型下载失败怎么办？

可以先使用快速模式。快速模式不需要模型，适合普通用户稳定使用。

### AI 高清模式没有生效怎么办？

通常是没有安装 `realesrgan-ncnn-vulkan`，或者程序找不到它。把可执行文件放到项目文件夹，或设置 `REALESRGAN_NCNN` 环境变量即可。

### 输出图片在哪里？

默认在项目的 `output` 文件夹中。文件名会自动加后缀，例如 `example_upscale_4x.png`。

### 会覆盖原图吗？

不会。程序只会读取原图，并在输出文件夹中保存新的 PNG 文件。

## 建议

- 产品图、设计图、线稿图：建议先试 2x 快速模式。
- AI 生成图：可以试 4x 快速模式，或者安装 Real-ESRGAN 后使用 AI 高清模式。
- 有文字的小图：不要反复多次放大，同一张图放大一次即可。
