import streamlit as st
import streamlit.components.v1 as components

# 1. Configure the Streamlit page
st.set_page_config(page_title="Our Anniversary", layout="wide", initial_sidebar_state="collapsed")

# 2. Hide Streamlit's default UI elements to make it look like a pure web app
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp {background-color: #121212;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. HTML, CSS, and JS (with images pointing to your raw GitHub links)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Our Anniversary 💖</title>
    
    <!-- Tailwind CSS for rapid styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Canvas Confetti for the blind box explosion -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <!-- Google Fonts for typography -->
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Share+Tech+Mono&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-dark: #121212;
            --bg-light: #fdf2f8;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: var(--bg-dark);
            transition: background-color 1s ease;
        }

        .view-section {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            flex-direction: column; justify-content: center; align-items: center;
        }

        .view-section.active {
            display: flex;
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .font-mono { font-family: 'Share Tech Mono', monospace; }
        
        .time-box {
            background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1rem;
            min-width: 90px;
            text-align: center;
        }

        @keyframes pulse-text {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        .animate-pulse-text { animation: pulse-text 2s infinite ease-in-out; }

        .gift-btn {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            background-color: white;
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 16rem;
        }
        .gift-btn:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        }

        .modal {
            display: none;
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            z-index: 100;
            justify-content: center; align-items: center;
        }
        .modal.active {
            display: flex;
            animation: fadeIn 0.4s ease-out;
        }

        .letter-paper-css {
            background-color: #f4ece1;
            background-image: repeating-linear-gradient(transparent, transparent 28px, rgba(0,0,0,0.06) 29px);
            box-shadow: 2px 2px 15px rgba(0,0,0,0.4), inset 0 0 50px rgba(150, 100, 50, 0.15);
            font-family: 'Caveat', cursive;
            color: #3e2a1d;
            width: 90%;
            max-width: 500px;
            padding: 40px 30px;
            border-radius: 4px;
            position: relative;
            transform: rotate(-1deg);
            max-height: 90vh;
            overflow-y: auto;
        }
        .letter-paper-css::before {
            content: '';
            position: absolute; top: 0; left: 40px; bottom: 0; width: 2px;
            background: rgba(255, 100, 100, 0.3);
        }

        .polaroid {
            background: white;
            padding: 10px 10px 40px 10px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            position: absolute;
            transform: rotate(var(--rot)) scale(1);
            transition: transform 0.4s cubic-bezier(0.5, 0.885, 0.32, 1.275);
            cursor: pointer;
            width: 200px;
        }
        .polaroid:hover {
            z-index: 999 !important; 
            transform: scale(1.6) rotate(0deg);
            box-shadow: 0 15px 30px rgba(0,0,0,0.6);
        }
        .polaroid img { width: 100%; height: 200px; object-fit: cover; background-color: #eee; }

        .mystery-box {
            width: 140px; height: 140px; cursor: pointer;
            transition: transform 0.2s, filter 0.2s;
            display: flex; justify-content: center; align-items: center;
        }
        .mystery-box img {
            width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 10px 8px rgba(0,0,0,0.2));
        }
        .mystery-box.disabled { opacity: 0.5; pointer-events: none; filter: grayscale(100%); }
        .mystery-box:not(.disabled):hover { transform: scale(1.15) translateY(-5px); filter: brightness(1.1); }
    </style>
</head>
<body>

    <!-- Screen 1: Countdown -->
    <div id="countdown-view" class="view-section active text-white">
        <h1 class="text-3xl md:text-5xl mb-8 font-semibold tracking-wider text-center px-4">Waiting for Our Special Day...</h1>
        <div class="flex gap-2 md:gap-6 font-mono text-4xl md:text-6xl">
            <div class="time-box">
                <span id="days">00</span>
                <div class="text-xs md:text-sm text-gray-400 mt-2 tracking-widest uppercase font-sans">Days</div>
            </div>
            <div class="time-box">
                <span id="hours">00</span>
                <div class="text-xs md:text-sm text-gray-400 mt-2 tracking-widest uppercase font-sans">Hours</div>
            </div>
            <div class="time-box">
                <span id="minutes">00</span>
                <div class="text-xs md:text-sm text-gray-400 mt-2 tracking-widest uppercase font-sans">Minutes</div>
            </div>
            <div class="time-box">
                <span id="seconds">00</span>
                <div class="text-xs md:text-sm text-gray-400 mt-2 tracking-widest uppercase font-sans">Seconds</div>
            </div>
        </div>
    </div>

    <!-- Screen 2: Click Anywhere Overlay -->
    <div id="click-anywhere-view" class="view-section bg-black cursor-pointer">
        <h2 class="text-4xl md:text-6xl text-pink-400 font-bold animate-pulse-text text-center px-4">
            It's Time! 💖<br><span class="text-2xl md:text-3xl font-normal text-white mt-4 block">Click anywhere to open your gifts!</span>
        </h2>
    </div>

    <!-- Screen 3: Gifts Selection -->
    <div id="gifts-view" class="view-section" style="background-color: var(--bg-light);">
        <h2 class="text-3xl md:text-5xl font-bold text-gray-800 mb-12 text-center px-4">Happy Anniversary! Pick a gift 🎁</h2>
        
        <div class="flex flex-col md:flex-row gap-8 items-center justify-center w-full px-4 max-w-6xl">
            
            <!-- Box 1: Love Letter (Raw GitHub URL) -->
            <div onclick="openLetter()" class="gift-btn">
                <div class="h-48 w-full rounded-lg overflow-hidden mb-4 border border-gray-100 flex items-center justify-center bg-gray-50">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/envelope.jpg" alt="Envelope" class="w-full h-full object-cover">
                </div>
                <h3 class="text-xl font-semibold text-gray-700">A Letter for You</h3>
            </div>

            <!-- Box 2: Memories -->
            <div onclick="openMemories()" class="gift-btn">
                <div class="h-48 w-full rounded-lg overflow-hidden mb-4 flex items-center justify-center bg-pink-100 text-7xl shadow-inner border border-pink-200">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/fav mem.jpg" alt="fav" class="w-full h-full object-cover">
                </div>
                <h3 class="text-xl font-semibold text-gray-700">Fav Memories</h3>
            </div>

            <!-- Box 3: Blind Boxes (Raw GitHub URL) -->
            <div onclick="openBlindBoxes()" class="gift-btn">
                <div class="h-48 w-full rounded-lg overflow-hidden mb-4 flex items-center justify-center bg-purple-50 p-4 shadow-inner border border-purple-100">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/blind_box.png" alt="Blind Box" class="w-full h-full object-contain hover:scale-110 transition-transform">
                </div>
                <h3 class="text-xl font-semibold text-gray-700">Blind Boxes</h3>
            </div>

        </div>
    </div>

    <!-- Modal: Love Letter -->
    <div id="modal-letter" class="modal" onclick="closeModal(event, 'modal-letter')">
        <div class="letter-paper-css" onclick="event.stopPropagation()">
            <button onclick="document.getElementById('modal-letter').classList.remove('active')" class="absolute top-2 right-4 text-4xl text-gray-800 hover:text-black font-sans">&times;</button>
            <div class="pl-8 pt-4">
                <h2 class="text-4xl mb-4">My Dearest,</h2>
                <p class="text-2xl leading-relaxed">
                    Happy Anniversary! ❤️ Time feels like it stops when I'm with you, yet the days fly by so fast. 
                    Thank you for being my rock, my safe place, and my favorite adventure. <br><br>
                    Here's to the beautiful memories we've made, the ones we are making today, and the millions 
                    more we will make in the future. You mean the world to me, and I love you more than words can ever truly express.
                </p>
                <p class="text-3xl mt-8 font-bold text-right pr-4">Love, Steffi</p>
            </div>
        </div>
    </div>

    <!-- Modal: Memories -->
    <div id="modal-memories" class="modal" onclick="closeModal(event, 'modal-memories')" style="background: rgba(15, 15, 15, 0.98);">
        <button onclick="closeMemoriesModal()" class="absolute top-6 right-8 text-5xl text-white hover:text-gray-300 z-[2000]">&times;</button>
        <iframe id="youtube-player" class="hidden" width="0" height="0" src="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        <div id="polaroid-container" class="relative w-full h-full overflow-hidden" onclick="event.stopPropagation()"></div>
    </div>

    <!-- Modal: Blind Boxes Selection (Raw GitHub URLs) -->
    <div id="modal-blind-boxes" class="modal" onclick="closeModal(event, 'modal-blind-boxes')">
        <div class="bg-white p-8 rounded-2xl max-w-5xl w-[90%] text-center relative shadow-2xl" onclick="event.stopPropagation()">
            <button onclick="document.getElementById('modal-blind-boxes').classList.remove('active')" class="absolute top-4 right-4 text-4xl text-gray-500 hover:text-black">&times;</button>
            <h2 class="text-4xl font-bold text-gray-800 mb-2">Pick ONE Mystery Box!</h2>
            <p class="text-gray-500 mb-10 text-xl font-medium">Choose carefully... what will you get? 👀</p>
            
            <div class="flex flex-wrap justify-center gap-4 md:gap-8" id="blind-box-container">
                <div class="mystery-box box-choice" onclick="selectBlindBox(1)">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp" alt="Box 1">
                </div>
                <div class="mystery-box box-choice" onclick="selectBlindBox(2)">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp" alt="Box 2">
                </div>
                <div class="mystery-box box-choice" onclick="selectBlindBox(3)">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp" alt="Box 3">
                </div>
                <div class="mystery-box box-choice" onclick="selectBlindBox(4)">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp" alt="Box 4">
                </div>
                <div class="mystery-box box-choice" onclick="selectBlindBox(5)">
                    <img src="https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pink-gift-box-with-gold-ribbon-on-transparent-background-png.webp" alt="Box 5">
                </div>
            </div>
        </div>
    </div>

    <!-- Modal: Blind Box Result -->
    <div id="modal-blind-result" class="modal">
        <div class="bg-white p-6 rounded-3xl max-w-sm w-[90%] text-center shadow-[0_0_40px_rgba(255,105,180,0.4)] relative border-4 border-pink-100">
            <h2 class="text-3xl font-extrabold text-pink-600 mb-4 uppercase tracking-widest" id="result-title">Title</h2>
            <div class="w-full bg-gray-50 rounded-xl mb-6 overflow-hidden flex items-center justify-center p-2 border-2 border-dashed border-pink-200">
                <img id="result-img" src="" alt="Result" class="w-full h-auto object-contain rounded-lg max-h-64">
            </div>
            <button onclick="document.getElementById('modal-blind-result').classList.remove('active')" class="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white px-8 py-3 rounded-full font-bold transition-all transform hover:scale-105 text-lg w-full shadow-lg">Claim It! 💖</button>
        </div>
    </div>

    <script>
        const targetDate = new Date("Oct 14, 2026 00:00:00").getTime();
        let timerInterval;
        let blindBoxClaimed = false;

        // Uses RAW GitHub URLs ensuring they load correctly on Streamlit Cloud
        // Notice the extensions match your GitHub screenshot exactly (.gif)
        const blindBoxData = {
            1: { img: 'https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/hug.gif', text: 'deep hug' },
            2: { img: 'https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/zonk.gif', text: 'ZONK' },
            3: { img: 'https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pinch.gif', text: 'PINCH' },
            4: { img: 'https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/pat%20pat.gif', text: 'pat pat' },
            5: { img: 'https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/s.gif', text: 'kisseu' }
        };

        function initApp() {
            updateTimer(); 
            timerInterval = setInterval(updateTimer, 1000);
            
            document.getElementById('click-anywhere-view').addEventListener('click', () => {
                document.getElementById('click-anywhere-view').classList.remove('active');
                document.getElementById('gifts-view').classList.add('active');
                document.body.style.backgroundColor = 'var(--bg-light)';
            });
        }

        function updateTimer() {
            const now = new Date().getTime();
            const distance = targetDate - now;

            if (distance <= 0) {
                clearInterval(timerInterval);
                document.getElementById('countdown-view').classList.remove('active');
                if(!document.getElementById('gifts-view').classList.contains('active')) {
                    document.getElementById('click-anywhere-view').classList.add('active');
                    document.body.style.backgroundColor = '#000000';
                }
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById('days').innerText = days.toString().padStart(2, '0');
            document.getElementById('hours').innerText = hours.toString().padStart(2, '0');
            document.getElementById('minutes').innerText = minutes.toString().padStart(2, '0');
            document.getElementById('seconds').innerText = seconds.toString().padStart(2, '0');
        }

        function openLetter() {
            document.getElementById('modal-letter').classList.add('active');
        }

        function openMemories() {
            const modal = document.getElementById('modal-memories');
            const container = document.getElementById('polaroid-container');
            const player = document.getElementById('youtube-player');
            
            modal.classList.add('active');
            player.src = 'https://www.youtube.com/embed/SctrVF37GAQ?autoplay=1';

            if (container.children.length === 0) {
                for (let i = 1; i <= 34; i++) {
                    const el = document.createElement('div');
                    el.className = 'polaroid';
                    
                    const left = Math.random() * 70 + 5;
                    const top = Math.random() * 65 + 5;
                    const rot = Math.random() * 80 - 40;

                    el.style.left = left + '%';
                    el.style.top = top + '%';
                    el.style.setProperty('--rot', rot + 'deg');
                    el.style.zIndex = i;
                    
                    el.onmouseenter = function() { this.style.zIndex = 1000; };
                    el.onmouseleave = function() { this.style.zIndex = i; };

                    const img = document.createElement('img');
                    img.src = `https://raw.githubusercontent.com/steffiwdjy/anniv2026/main/${i}.jpeg`;
                    img.alt = 'Memory ' + i;
                    
                    const caption = document.createElement('div');
                    caption.className = 'text-center mt-3 text-sm font-semibold text-gray-700 font-sans';
                    caption.innerText = 'Memory ' + i;

                    el.appendChild(img);
                    el.appendChild(caption);
                    container.appendChild(el);
                }
            }
        }

        function closeMemoriesModal() {
            document.getElementById('modal-memories').classList.remove('active');
            document.getElementById('youtube-player').src = '';
        }

        function openBlindBoxes() {
            document.getElementById('modal-blind-boxes').classList.add('active');
        }

        function selectBlindBox(boxNumber) {
            if (blindBoxClaimed) return;
            blindBoxClaimed = true; 

            const boxes = document.querySelectorAll('.box-choice');
            boxes.forEach(box => box.classList.add('disabled'));

            const duration = 2000;
            const end = Date.now() + duration;

            (function frame() {
                confetti({ particleCount: 7, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#ff69b4', '#ff1493', '#ffb6c1'] });
                confetti({ particleCount: 7, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#ff69b4', '#ff1493', '#ffb6c1'] });

                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            }());
            
            setTimeout(() => {
                document.getElementById('modal-blind-boxes').classList.remove('active');
                
                const data = blindBoxData[boxNumber];
                document.getElementById('result-title').innerText = data.text;
                document.getElementById('result-img').src = data.img;
                
                document.getElementById('modal-blind-result').classList.add('active');
            }, 1200); 
        }

        function closeModal(event, modalId) {
            if(event.target.id === modalId) {
                document.getElementById(modalId).classList.remove('active');
                if(modalId === 'modal-memories') {
                    closeMemoriesModal();
                }
            }
        }

        window.onload = initApp;
    </script>
</body>
</html>
"""

components.html(HTML_TEMPLATE, height=900, scrolling=False)
