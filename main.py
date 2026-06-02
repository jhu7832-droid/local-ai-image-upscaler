import argparse
import html
import mimetypes
import shutil
import tempfile
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from upscaler import process_path


APP_TITLE = "本地图片高清放大工具"

PAGE = r"""
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>本地图片高清放大工具</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
      color: #20313c;
      background:
        radial-gradient(circle at 18% 16%, rgba(56,168,232,.22), transparent 28%),
        radial-gradient(circle at 82% 12%, rgba(147,197,253,.28), transparent 24%),
        linear-gradient(135deg, #eaf4f8 0%, #f7fbfd 55%, #edf6fb 100%);
    }
    main { max-width: 1120px; margin: 0 auto; padding: 42px 24px; }
    .app {
      border: 1px solid rgba(120,160,184,.34);
      border-radius: 24px;
      padding: 30px;
      background: rgba(255,255,255,.62);
      box-shadow: 0 24px 74px rgba(44,90,119,.16);
      backdrop-filter: blur(18px);
    }
    h1 { margin: 0; font-size: 34px; }
    .sub { color: #607582; margin: 10px 0 24px; }
    .grid { display: grid; grid-template-columns: 1.7fr .8fr; gap: 22px; }
    .drop {
      border: 2px dashed rgba(56,168,232,.55);
      border-radius: 20px;
      min-height: 210px;
      background: rgba(255,255,255,.72);
      display: grid;
      place-items: center;
      text-align: center;
      padding: 22px;
      transition: transform .15s ease, border-color .15s ease, background .15s ease;
      cursor: pointer;
    }
    .drop.dragover {
      transform: translateY(-2px);
      border-color: #38a8e8;
      background: rgba(236,248,255,.92);
    }
    .drop strong { display:block; font-size: 23px; margin-bottom: 8px; }
    .drop span { color: #607582; }
    input[type="file"] { display: none; }
    label, .label { display: block; font-weight: 700; margin: 0 0 8px; }
    input[type="text"] {
      width: 100%;
      border: 1px solid rgba(135,169,188,.45);
      border-radius: 12px;
      padding: 12px 14px;
      outline: none;
      background: rgba(255,255,255,.78);
      color: #20313c;
    }
    .panel {
      border-radius: 18px;
      padding: 18px;
      background: rgba(255,255,255,.66);
      border: 1px solid rgba(135,169,188,.32);
    }
    .row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }
    .choice input { display: none; }
    .choice span {
      display: inline-block;
      border-radius: 999px;
      padding: 10px 15px;
      border: 1px solid rgba(135,169,188,.45);
      background: rgba(255,255,255,.7);
      cursor: pointer;
    }
    .choice input:checked + span {
      border-color: #38a8e8;
      background: #e2f5fc;
      color: #176d9f;
      font-weight: 800;
    }
    #create {
      width: 220px;
      min-height: 58px;
      border: 0;
      border-radius: 999px;
      color: white;
      font-size: 20px;
      font-weight: 900;
      letter-spacing: 1px;
      background: linear-gradient(135deg, #38a8e8, #237db1);
      box-shadow: 0 12px 28px rgba(56,168,232,.34), inset 0 1px 0 rgba(255,255,255,.35);
      animation: createPulse 1.65s ease-in-out infinite;
      transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
      cursor: pointer;
    }
    #create:hover { filter: brightness(1.06); transform: translateY(-2px); }
    #create:active {
      transform: translateY(4px) scale(.97);
      box-shadow: 0 5px 12px rgba(56,168,232,.24), inset 0 3px 8px rgba(0,0,0,.18);
      animation: none;
    }
    @keyframes createPulse {
      0%,100% { box-shadow: 0 12px 28px rgba(56,168,232,.30), 0 0 0 0 rgba(56,168,232,.22); }
      50% { box-shadow: 0 16px 34px rgba(56,168,232,.42), 0 0 0 9px rgba(56,168,232,.08); }
    }
    pre {
      white-space: pre-wrap;
      min-height: 92px;
      padding: 14px;
      border-radius: 14px;
      background: rgba(255,255,255,.68);
      border: 1px solid rgba(135,169,188,.25);
    }
    .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
    .gallery img {
      width: 100%;
      border-radius: 16px;
      background: white;
      border: 1px solid rgba(135,169,188,.32);
      box-shadow: 0 10px 26px rgba(44,90,119,.10);
    }
    @media (max-width: 850px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <section class="app">
      <h1>本地图片高清放大工具</h1>
      <p class="sub">拖入图片后不会立刻处理，确认参数并点击 CREATE 才会开始。全程本地运行，不上传云端。</p>

      <div class="grid">
        <div>
          <div id="drop" class="drop">
            <div>
              <strong>把图片拖到这里，或点击上传</strong>
              <span id="fileText">支持 JPG / JPEG / PNG / WEBP，可一次选择多张</span>
            </div>
          </div>
          <input id="files" type="file" accept=".jpg,.jpeg,.png,.webp" multiple />
          <div style="height:16px"></div>
          <label>批量处理文件夹路径，可选</label>
          <input id="inputFolder" type="text" placeholder="例如 input 或 /Users/你的名字/Pictures/input" />
          <div style="height:14px"></div>
          <label>输出文件夹</label>
          <input id="outputFolder" type="text" value="__OUTPUT__" />
        </div>

        <div class="panel">
          <div class="label">放大倍率</div>
          <div class="row">
            <label class="choice"><input name="scale" type="radio" value="2" /><span>2x</span></label>
            <label class="choice"><input name="scale" type="radio" value="4" checked /><span>4x</span></label>
          </div>

          <div class="label">处理模式</div>
          <div class="row">
            <label class="choice"><input name="mode" type="radio" value="fast" checked /><span>快速模式</span></label>
            <label class="choice"><input name="mode" type="radio" value="ai" /><span>AI 高清模式</span></label>
          </div>

          <button id="create">CREATE</button>
        </div>
      </div>

      <h3>处理进度 / 完成提示</h3>
      <pre id="status">等待上传图片。</pre>
      <div id="gallery" class="gallery"></div>
    </section>
  </main>

  <script>
    const drop = document.getElementById("drop");
    const filesInput = document.getElementById("files");
    const fileText = document.getElementById("fileText");
    const statusBox = document.getElementById("status");
    const gallery = document.getElementById("gallery");
    const create = document.getElementById("create");

    drop.addEventListener("click", () => filesInput.click());
    drop.addEventListener("dragover", (event) => {
      event.preventDefault();
      drop.classList.add("dragover");
    });
    drop.addEventListener("dragleave", () => drop.classList.remove("dragover"));
    drop.addEventListener("drop", (event) => {
      event.preventDefault();
      drop.classList.remove("dragover");
      filesInput.files = event.dataTransfer.files;
      updateFileText();
    });
    filesInput.addEventListener("change", updateFileText);

    function updateFileText() {
      const count = filesInput.files.length;
      fileText.textContent = count ? `已上传 ${count} 张图片，确认后点击 CREATE` : "支持 JPG / JPEG / PNG / WEBP，可一次选择多张";
    }

    create.addEventListener("click", async () => {
      const form = new FormData();
      for (const file of filesInput.files) form.append("files", file);
      form.append("input_folder", document.getElementById("inputFolder").value);
      form.append("output_folder", document.getElementById("outputFolder").value);
      form.append("scale", document.querySelector("input[name=scale]:checked").value);
      form.append("mode", document.querySelector("input[name=mode]:checked").value);

      statusBox.textContent = "正在处理，请稍候...";
      create.disabled = true;
      gallery.innerHTML = "";
      try {
        const response = await fetch("/process", { method: "POST", body: form });
        const data = await response.json();
        statusBox.textContent = data.status;
        gallery.innerHTML = data.results.map((item) =>
          `<a href="${item.url}" target="_blank"><img src="${item.url}" alt="${item.name}" /></a>`
        ).join("");
      } catch (error) {
        statusBox.textContent = "处理失败：" + error;
      } finally {
        create.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


def create_app():
    app = FastAPI()

    @app.get("/", response_class=HTMLResponse)
    def index():
        output = html.escape(str(Path.cwd() / "output"))
        return PAGE.replace("__OUTPUT__", output)

    @app.get("/file")
    def serve_file(path: str):
        target = Path(path)
        if not target.exists() or not target.is_file():
            return JSONResponse({"error": "file not found"}, status_code=404)
        media_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        return FileResponse(target, media_type=media_type, filename=target.name)

    @app.post("/process")
    async def process(
        input_folder: str = Form(""),
        output_folder: str = Form("output"),
        scale: int = Form(4),
        mode: str = Form("fast"),
        files: list[UploadFile] = File(default=[]),
    ):
        output_dir = Path(output_folder.strip() or "output").expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        logs = []
        results = []

        def progress(done, total, message):
            logs.append(f"[{done}/{total}] {message}")

        try:
            if input_folder.strip():
                results.extend(
                    process_path(Path(input_folder.strip()).expanduser(), output_dir, scale=scale, mode=mode, progress_callback=progress)
                )

            if files:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_dir = Path(temp_dir)
                    for upload in files:
                        original_name = Path(upload.filename or "image.png").name
                        temp_path = temp_dir / original_name
                        if temp_path.exists():
                            temp_path = temp_dir / f"{time.time_ns()}_{original_name}"
                        with temp_path.open("wb") as handle:
                            shutil.copyfileobj(upload.file, handle)
                        results.extend(process_path(temp_path, output_dir, scale=scale, mode=mode, progress_callback=progress))

            if not results:
                return {"status": "请先上传图片，或填写 input 文件夹路径。", "results": []}
        except Exception as exc:
            return {"status": f"处理失败：{exc}", "results": []}

        payload = [
            {
                "name": Path(path).name,
                "url": "/file?path=" + urllib.parse.quote(str(Path(path).resolve())),
            }
            for path in results
        ]
        status = f"完成，共输出 {len(results)} 张图片。保存位置：{output_dir.resolve()}"
        if logs:
            status += "\n\n" + "\n".join(logs[-12:])
        return {"status": status, "results": payload}

    return app


def parse_args():
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument("--input", "-i", help="输入图片或文件夹路径")
    parser.add_argument("--output", "-o", default="output", help="输出文件夹")
    parser.add_argument("--scale", "-s", type=int, choices=[2, 4], default=4, help="放大倍率")
    parser.add_argument("--mode", "-m", choices=["fast", "ai"], default="fast", help="处理模式")
    parser.add_argument("--cli", action="store_true", help="使用命令行模式，不启动界面")
    parser.add_argument("--server-port", type=int, default=7860, help="本地界面端口")
    return parser.parse_args()


def run_cli(args):
    if not args.input:
        raise SystemExit("命令行模式需要提供 --input。")

    def on_progress(done, total, message):
        print(f"[{done}/{total}] {message}")

    results = process_path(Path(args.input), Path(args.output), scale=args.scale, mode=args.mode, progress_callback=on_progress)
    print(f"处理完成，共输出 {len(results)} 张图片：")
    for item in results:
        print(item)


def open_browser(port):
    time.sleep(1)
    webbrowser.open(f"http://127.0.0.1:{port}")


def run_gui(args):
    threading.Thread(target=open_browser, args=(args.server_port,), daemon=True).start()
    uvicorn.run(create_app(), host="127.0.0.1", port=args.server_port, log_level="info")


if __name__ == "__main__":
    args = parse_args()
    if args.cli or args.input:
        run_cli(args)
    else:
        run_gui(args)
