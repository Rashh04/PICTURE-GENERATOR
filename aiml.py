from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HIGH-QUALITY IMAGE DATASET (SCENARIO BASED)
dataset = {
    "moon": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d",
    "night": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "dog": "https://images.unsplash.com/photo-1517423440428-a5a00ad493e8",
    "car": "https://images.unsplash.com/photo-1503376780353-7e6692767b70",
    "mountain": "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
    "beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    "city": "https://images.unsplash.com/photo-1494526585095-c41746248156",
    "sunset": "https://images.unsplash.com/photo-1501973801540-537f08ccae7b",
    "forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
    "space": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa"
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Studio Pro</title>

<style>
body{
    background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#1c1c3c);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    font-family: 'Segoe UI', sans-serif;
    color:white;
    text-align:center;
    padding:40px;
}

@keyframes gradientBG{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

.container{
    width:800px;
    margin:auto;
    padding:30px;
    border-radius:20px;
    backdrop-filter: blur(15px);
    background: rgba(255,255,255,0.08);
    box-shadow: 0 0 40px rgba(0,255,255,0.2);
}

h1{
    font-size:35px;
    background: linear-gradient(90deg,cyan,magenta);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

textarea{
    width:100%;
    height:120px;
    border-radius:12px;
    padding:15px;
    font-size:16px;
    background: rgba(255,255,255,0.1);
    color:white;
    border:none;
}

button{
    margin-top:20px;
    padding:15px 40px;
    border:none;
    border-radius:10px;
    font-size:18px;
    background: linear-gradient(45deg,cyan,blue);
    color:white;
    cursor:pointer;
}

img{
    margin-top:20px;
    max-width:100%;
    border-radius:15px;
    display:none;
    box-shadow:0 10px 30px rgba(0,0,0,0.5);
}

.download{
    display:none;
    margin-top:15px;
    background: green;
}
</style>

</head>

<body>

<div class="container">
<h1>⚡ AI Studio Pro</h1>
<p>Try: moon, dog, beach sunset, forest, space</p>

<textarea id="prompt">moon night sky</textarea>

<button onclick="generate()">Generate</button>

<br>
<img id="img">

<br>
<button class="download" id="downloadBtn" onclick="download()">Download</button>

</div>

<script>

let currentImage = "";

async function generate(){

    let prompt = document.getElementById("prompt").value;

    const res = await fetch("/generate",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({prompt:prompt})
    });

    const data = await res.json();

    currentImage = data.image;

    let img = document.getElementById("img");
    img.src = data.image + "?auto=format&fit=crop&w=800&q=80";
    img.style.display = "block";

    document.getElementById("downloadBtn").style.display = "inline-block";
}

function download(){
    let a = document.createElement("a");
    a.href = currentImage;
    a.download = "ai-image.jpg";
    a.click();
}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt").lower()
    words = prompt.split()

    # MULTI-KEYWORD MATCHING
    for word in words:
        if word in dataset:
            return jsonify({"image": dataset[word]})

    # DEFAULT BEAUTIFUL IMAGE
    return jsonify({
        "image": "https://images.unsplash.com/photo-1492724441997-5dc865305da7"
    })

if __name__ == "__main__":
    app.run(debug=True)