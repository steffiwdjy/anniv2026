import streamlit as st
import streamlit.components.v1 as components

# Configure the Streamlit page to be wide and hide the default sidebar/menu
st.set_page_config(page_title="Happy Anniversary", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit's default headers and footers to make it look like a pure web app
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp {background-color: #111;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# The exact HTML, CSS, and JS from your web app
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        body {
            margin: 0; padding: 0; background-color: #111; color: white;
            font-family: 'Courier New', Courier, monospace; display: flex;
            justify-content: center; align-items: center; height: 95vh;
            overflow: hidden; flex-direction: column; text-align: center;
        }
        #countdown-screen { display: flex; flex-direction: column; align-items: center; transition: opacity 1s; }
        .time-box {
            display: inline-block; background: #222; border-radius: 10px;
            padding: 20px; margin: 10px; font-size: 3rem; font-weight: bold;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .label { display: block; font-size: 1rem; color: #f39c12; margin-top: 5px; }
        #main-screen { display: none; flex-direction: column; align-items: center; }
        .boxes-container { display: flex; gap: 30px; margin-top: 30px; }
        .gift-box {
            width: 150px; height: 150px; background: #333; border-radius: 15px;
            display: flex; justify-content: center; align-items: center; cursor: pointer;
            transition: transform 0.3s; font-size: 1.2rem; font-weight: bold;
            text-transform: uppercase; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }
        .gift-box:hover { transform: scale(1.1); background: #444; }
        .modal {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9); justify-content: center; align-items: center; z-index: 1000;
        }
        .close-btn { position: absolute; top: 20px; right: 30px; font-size: 2rem; cursor: pointer; color: white; z-index: 1001; }
        #envelope { width: 300px; cursor: pointer; transition: opacity 0.5s; }
        #classic-letter {
            display: none; background: #f4e4bc; color: #3e2723; padding: 40px; width: 80%;
            max-width: 500px; font-family: 'Georgia', serif; font-style: italic;
            border-radius: 5px; box-shadow: 0 0 20px rgba(0,0,0,0.8); line-height: 1.6;
        }
        #photo-container { position: relative; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }
        .polaroid {
            position: absolute; width: 150px; padding: 10px 10px 40px 10px; background: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6); transition: all 0.3s; cursor: pointer;
        }
        .polaroid img { width: 100%; height: 130px; object-fit: cover; }
        .polaroid:hover { z-index: 500 !important; transform: scale(1.5) rotate(0deg) !important; }
        #blind-box-container { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
        .blind-box { width: 120px; cursor: pointer; transition: transform 0.2s; }
        .blind-box:hover { transform: scale(1.1); }
        .blind-box img { width: 100%; }
        #blind-result { display: none; flex-direction: column; align-items: center; }
        #blind-result img { max-width: 300px; border-radius: 10px; }
        #blind-result h2 { margin-top: 20px; font-size: 2.5rem; color: #ff6b81; }
    </style>
</head>
<body>
    <div id="player" style="display:none;"></div>
    <script src="https://www.youtube.com/iframe_api"></script>

    <div id="countdown-screen">
        <h1 id="countdown-title">Waiting for Our Special Day...</h1>
        <div>
            <div class="time-box"><span id="days">00</span><span class="label">DAYS</span></div>
            <div class="time-box"><span id="hours">00</span><span class="label">HOURS</span></div>
            <div class="time-box"><span id="minutes">00</span><span class="label">MINUTES</span></div>
            <div class="time-box"><span id="seconds">00</span><span class="label">SECONDS</span></div>
        </div>
        <div id="click-anywhere" style="display:none; margin-top:30px; cursor:pointer; font-size:1.5rem; color:#f39c12;">
            (Click Anywhere)
        </div>
    </div>

    <div id="main-screen">
        <h1>Happy Anniversary! Pick a gift 🎁</h1>
        <div class="boxes-container">
            <div class="gift-box" onclick="openModal('modal-1')">Box 1</div>
            <div class="gift-box" onclick="openModal('modal-2')">Box 2</div>
            <div class="gift-box" onclick="openModal('modal-3')">Box 3</div>
        </div>
    </div>

    <div id="modal-1" class="modal">
        <div class="close-btn" onclick="closeModal('modal-1')">&times;</div>
        <img id="envelope" src="/app/static/image_9c4a77.jpg" onclick="openLetter()" alt="Envelope">
        <div id="classic-letter">
            My Dearest,<br><br>
            Happy Anniversary! Thank you for every single moment we've shared. You mean the world to me.<br><br>
            Forever yours,<br>
            Steffi
        </div>
    </div>

    <div id="modal-2" class="modal">
        <div class="close-btn" onclick="closeModal('modal-2'); stopMusic();">&times;</div>
        <div id="photo-container"></div>
    </div>

    <div id="modal-3" class="modal">
        <div class="close-btn" onclick="closeModal('modal-3')">&times;</div>
        <div id="blind-box-container">
            <div class="blind-box" onclick="chooseBlindBox('deep hug', '/app/static/hug.jpg')">
                <img src="/app/static/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp">
            </div>
            <div class="blind-box" onclick="chooseBlindBox('ZONK', '/app/static/zonk.jpg')">
                <img src="/app/static/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp">
            </div>
            <div class="blind-box" onclick="chooseBlindBox('PINCH', '/app/static/pinch.jpg')">
                <img src="/app/static/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp">
            </div>
            <div class="blind-box" onclick="chooseBlindBox('pat pat', '/app/static/pat pat.gif')">
                <img src="/app/static/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp">
            </div>
            <div class="blind-box" onclick="chooseBlindBox('kisseu', '/app/static/s.jpg')">
                <img src="/app/static/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp">
            </div>
        </div>
        <div id="blind-result">
            <img id="result-img" src="">
            <h2 id="result-text"></h2>
        </div>
    </div>

    <script>
        const targetDate = new Date("Oct 14, 2026 00:00:00").getTime();
        
        const countdownInterval = setInterval(() => {
            const now = new Date().getTime();
            const distance = targetDate - now;

            if (distance < 0) {
                clearInterval(countdownInterval);
                document.getElementById('countdown-title').innerText = "It's Time!";
                document.getElementById('days').innerText = "00";
                document.getElementById('hours').innerText = "00";
                document.getElementById('minutes').innerText = "00";
                document.getElementById('seconds').innerText = "00";
                
                const clickText = document.getElementById('click-anywhere');
                clickText.style.display = "block";
                
                document.body.onclick = function() {
                    document.getElementById('countdown-screen').style.display = "none";
                    document.getElementById('main-screen').style.display = "flex";
                    document.body.onclick = null; 
                };
            } else {
                document.getElementById('days').innerText = Math.floor(distance / (1000 * 60 * 60 * 24)).toString().padStart(2, '0');
                document.getElementById('hours').innerText = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
                document.getElementById('minutes').innerText = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
                document.getElementById('seconds').innerText = Math.floor((distance % (1000 * 60)) / 1000).toString().padStart(2, '0');
            }
        }, 1000);

        function openModal(id) {
            document.getElementById(id).style.display = 'flex';
            if(id === 'modal-2') triggerMemories();
        }
        function closeModal(id) {
            document.getElementById(id).style.display = 'none';
        }
        function openLetter() {
            document.getElementById('envelope').style.display = 'none';
            document.getElementById('classic-letter').style.display = 'block';
        }

        let ytPlayer;
        function onYouTubeIframeAPIReady() {
            ytPlayer = new YT.Player('player', {
                height: '0', width: '0',
                videoId: 'SctrVF37GAQ', 
                playerVars: { 'autoplay': 0, 'controls': 0 }
            });
        }
        function triggerMemories() {
            if(ytPlayer && ytPlayer.playVideo) ytPlayer.playVideo();
            const container = document.getElementById('photo-container');
            container.innerHTML = ""; 
            
            for(let i=1; i<=15; i++) {
                let div = document.createElement('div');
                div.className = 'polaroid';
                div.innerHTML = `<img src="/app/static/photo${i}.jpg" onerror="this.src='https://via.placeholder.com/150?text=Photo+${i}'">`;
                
                let rotation = (Math.random() * 60) - 30; 
                let x = (Math.random() * 60) - 30; 
                let y = (Math.random() * 60) - 30; 
                let z = Math.floor(Math.random() * 10);
                
                div.style.transform = `translate(${x}vw, ${y}vh) rotate(${rotation}deg)`;
                div.style.zIndex = z;
                container.appendChild(div);
            }
        }
        function stopMusic() {
            if(ytPlayer && ytPlayer.pauseVideo) ytPlayer.pauseVideo();
        }

        let blindBoxChosen = false;
        function chooseBlindBox(text, imgSrc) {
            if(blindBoxChosen) return; 
            blindBoxChosen = true;
            confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });

            setTimeout(() => {
                document.getElementById('blind-box-container').style.display = 'none';
                document.getElementById('result-img').src = imgSrc;
                document.getElementById('result-text').innerText = text;
                document.getElementById('blind-result').style.display = 'flex';
            }, 500);
        }
    </script>
</body>
</html>
"""

# Render the HTML directly inside Streamlit
components.html(HTML_TEMPLATE, height=850, scrolling=False)
