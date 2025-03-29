from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)

L = instaloader.Instaloader()

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "لینک اینستاگرام را وارد کنید"}), 400

    try:
        # استخراج shortcode از لینک
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        # انتخاب لینک مستقیم بر اساس نوع پست (عکس یا ویدئو)
        media_url = post.video_url if post.is_video else post.url
        return jsonify({"download_url": media_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
