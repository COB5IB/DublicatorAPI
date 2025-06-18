from flask import Flask, request, Response
import requests
import logging
import os

# === LOG AYARLARI ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{log_dir}/duplicator.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Ortam değişkenlerinden hedef URL'ler ve port bilgisi alınır
TARGET_URLS = os.environ.get("TARGET_URLS", "http://10.49.77.153:9401,http://10.49.77.153:9402").split(",")
PORT = int(os.environ.get("DUPLICATOR_PORT", 9301))


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def duplicate_and_forward(path):
    method = request.method
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    data = request.get_data()
    full_path = f"/{path}"

    # 🟡 GELEN İSTEĞİ LOGA YAZ
    logging.info("📥 Yeni istek alındı:")
    logging.info(f"🔸 Yöntem: {method}")
    logging.info(f"🔸 Path: /{path}")
    logging.info(f"🔸 Headers: {dict(request.headers)}")
    try:
        logging.info(f"🔸 Body: {data.decode(errors='ignore')}")
    except Exception as e:
        logging.warning(f"🔸 Body okunamadı: {e}")

    results = []
    for target in TARGET_URLS:
        url = f"{target}{full_path}"
        try:
            resp = requests.request(method, url, headers=headers, data=data)
            results.append((url, resp.status_code))
            logging.info(f"✅ {method} -> {url} [Status: {resp.status_code}]")
        except Exception as e:
            results.append((url, str(e)))
            logging.error(f"❌ {method} -> {url} [Error: {str(e)}]")

    return Response(f"Duplicated to: {results}", status=200)


if __name__ == "__main__":
    logging.info(f"🚀 Duplicator başlatılıyor... Port: {PORT}")
    logging.info(f"🎯 Hedef URL'ler: {TARGET_URLS}")
    app.run(host="0.0.0.0", port=PORT)
