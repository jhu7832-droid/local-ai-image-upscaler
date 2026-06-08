# 本地图片高清放大工具

当前版本：`v0.1.2`

这是一个本地运行的图片放大和锐化小工具，适合处理 ChatGPT / AI 生成图、产品图、设计图、规格书图片和线稿图。程序不会上传图片，不调用付费 API。

## 版本更新规则

以后每次更新网站、修改说明或改写代码，最终版本号都会增加 `0.0.1`。

示例：

```text
v0.1.0 → v0.1.1 → v0.1.2 → v0.1.3
```

当最后一位到 `9` 后，下一次进入新的小版本：

```text
v0.1.9 → v0.2.0
```

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

## 下载与更新项目

普通用户推荐使用 ZIP 压缩包方式下载，不需要会 Git 命令。

### 下载最新版 ZIP

1. 打开项目网站或 GitHub 页面。
2. 点击 `下载源码 ZIP`。
3. 下载完成后，双击解压压缩包。
4. 打开解压后的项目文件夹。
5. 按下面的 Mac 或 Windows 运行方式启动程序。

ZIP 下载地址：

```text
https://github.com/jhu7832-droid/local-ai-image-upscaler/archive/refs/heads/main.zip
```

### 以后如何更新？

如果我更新了网站或程序，普通用户只需要重新下载最新版 ZIP，然后重新解压即可。

注意：更新前建议先把旧文件夹里的 `output` 文件夹保存好，因为里面可能有你已经处理好的图片。

### GitHub 克隆方式

如果你会使用 GitHub Desktop 或 Git 命令，也可以用克隆方式：

```bash
git clone https://github.com/jhu7832-droid/local-ai-image-upscaler.git
cd local-ai-image-upscaler
```

以后更新时，在项目文件夹里执行：

```bash
git pull
```

## Mac 运行方式

1. 安装 Python 3.10 或更新版本。
2. 打开“终端”。
3. 进入项目文件夹。
4. 安装依赖。
5. 启动程序。

如果你是通过 Git 下载项目：

```bash
git clone https://github.com/jhu7832-droid/local-ai-image-upscaler.git
cd local-ai-image-upscaler
python3 -m pip install -r requirements.txt
python3 main.py
```

如果你已经在项目文件夹里：

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

运行后会自动打开本地网页：

```bash
http://127.0.0.1:7860
```

然后拖入图片，选择 2x / 4x 和处理模式，点击 `CREATE`。

## Windows 运行方式

1. 安装 Python 3.10 或更新版本。
2. 安装 Python 时必须勾选 `Add python.exe to PATH`。
3. 打开 PowerShell。
4. 进入项目文件夹。
5. 安装依赖。
6. 启动程序。

如果你是通过 Git 下载项目：

```powershell
git clone https://github.com/jhu7832-droid/local-ai-image-upscaler.git
cd local-ai-image-upscaler
python -m pip install -r requirements.txt
python main.py
```

如果你已经在项目文件夹里：

```powershell
python -m pip install -r requirements.txt
python main.py
```

运行后会自动打开本地网页：

```powershell
http://127.0.0.1:7860
```

然后拖入图片，选择 2x / 4x 和处理模式，点击 `CREATE`。

如果 PowerShell 提示找不到 `python`，可以尝试：

```powershell
py -m pip install -r requirements.txt
py main.py
```

## iPhone / iPad 使用方式

iPhone / iPad 可以访问项目网站和 GitHub 页面查看说明，但不能像 Mac / Windows 一样直接运行这个 Python 本地处理工具。

推荐流程：

1. 在 iPhone / iPad 上准备要处理的图片。
2. 用 AirDrop、iCloud、微信文件传输、数据线等方式，把图片传到 Mac 或 Windows 电脑。
3. 在电脑上运行本工具。
4. 把图片拖到本地网页界面里。
5. 选择 2x / 4x 和处理模式。
6. 点击 `CREATE`。
7. 在电脑的 `output` 文件夹中找到高清图。
8. 把高清图传回 iPhone / iPad。

这样仍然保持“图片在自己设备上处理”，不会上传到项目网站。

## 打开工具后的操作

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

### Windows 可以用吗？

可以。Pillow、OpenCV、NumPy、FastAPI 和 Uvicorn 都支持 Windows。最常见的问题是安装 Python 时没有勾选 `Add python.exe to PATH`。

### iPhone 可以直接处理图片吗？

目前不建议。这个项目是 Python 本地桌面工具，最佳使用方式是在 Mac 或 Windows 电脑上处理图片。

## 网站信息反馈

Netlify 网站底部已经加入“信息反馈”表单，用户可以填写邮箱和问题描述。

反馈会进入 Netlify Forms 后台。要让站长邮箱收到通知，请在 Netlify 后台设置一次：

1. 打开 Netlify 项目 `local-ai-image-upscaler`。
2. 进入 `Project configuration`。
3. 打开 `Notifications`。
4. 添加 `Email notification`。
5. 收件邮箱填写你自己的接收邮箱。
6. 保存后，用户提交反馈时就会发送邮件通知。

即使没有开启邮件通知，也可以在 Netlify 的 `Forms` 页面查看用户提交内容。

### 会覆盖原图吗？

不会。程序只会读取原图，并在输出文件夹中保存新的 PNG 文件。

## 建议

- 产品图、设计图、线稿图：建议先试 2x 快速模式。
- AI 生成图：可以试 4x 快速模式，或者安装 Real-ESRGAN 后使用 AI 高清模式。
- 有文字的小图：不要反复多次放大，同一张图放大一次即可。
