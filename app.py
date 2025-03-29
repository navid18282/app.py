from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

# پوشه دانلودها
os.makedirs("downloads", exist_ok=True)

L = instaloader.Instaloader()

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "لینک اینستاگرام را وارد کنید"}), 400

    shortcode = url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    filename = f"downloads/{shortcode}.mp4" if post.is_video else f"downloads/{shortcode}.jpg"

    # دانلود فایل
    L.download_post(post, target="downloads")

    return jsonify({"download_url": f"https://yourserver.com/{filename}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
