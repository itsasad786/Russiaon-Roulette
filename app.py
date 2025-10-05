# app.py
from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# HTML template for the game
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 Russian Roulette - Web Version</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 30px;
        }
        .number-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        .number-btn {
            background: linear-gradient(145deg, #f0f0f0, #cacaca);
            border: none;
            border-radius: 15px;
            padding: 20px;
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
            cursor: pointer;
            transition: all 0.3s ease;
            min-height: 60px;
        }
        .number-btn:hover {
            transform: translateY(-3px);
            background: linear-gradient(145deg, #e0e0e0, #b8b8b8);
        }
        .number-btn.selected {
            background: linear-gradient(145deg, #ff6b6b, #ee5a52);
            color: white;
        }
        .guess-btn {
            background: linear-gradient(135deg, #ff4444, #cc3333);
            border: none;
            color: white;
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            margin: 20px 0;
        }
        .guess-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 15px;
            font-size: 1.2rem;
            font-weight: bold;
        }
        .result.win {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
        }
        .result.lose {
            background: linear-gradient(135deg, #f44336, #d32f2f);
            color: white;
        }
        .stats {
            margin-top: 20px;
            color: #666;
        }
        @media (max-width: 768px) {
            .number-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            .container {
                padding: 20px;
                margin: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Russian Roulette</h1>
        <p class="subtitle">Choose a number between 1 and 10</p>
        
        <div class="number-grid">
            {% for i in range(1, 11) %}
            <button class="number-btn" onclick="selectNumber({{ i }})">{{ i }}</button>
            {% endfor %}
        </div>
        
        <button class="guess-btn" id="guessBtn" onclick="makeGuess()" disabled>PULL THE TRIGGER</button>
        
        <div id="result"></div>
        <div class="stats" id="stats">Games: 0 | Wins: 0 | Losses: 0</div>
    </div>

    <script>
        let selectedNumber = null;
        let targetNumber = {{ target_number }};
        let gamesPlayed = 0;
        let wins = 0;
        let losses = 0;

        function selectNumber(number) {
            selectedNumber = number;
            document.getElementById('guessBtn').disabled = false;
            
            // Update button styles
            document.querySelectorAll('.number-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            event.target.classList.add('selected');
        }

        function makeGuess() {
            if (!selectedNumber) return;
            
            gamesPlayed++;
            const resultDiv = document.getElementById('result');
            
            if (selectedNumber === targetNumber) {
                wins++;
                resultDiv.innerHTML = `
                    <div class="result win">
                        🎉 CONGRATULATIONS! You survived! 🎉<br>
                        The number was ${targetNumber}
                    </div>
                `;
            } else {
                losses++;
                resultDiv.innerHTML = `
                    <div class="result lose">
                        💀 WRONG GUESS! System crash initiated... 💀<br>
                        The correct number was ${targetNumber}<br>
                        <small>Just kidding! Your system is fine. 😄</small>
                    </div>
                `;
            }
            
            updateStats();
            document.getElementById('guessBtn').disabled = true;
            
            // Reset after 3 seconds
            setTimeout(() => {
                location.reload();
            }, 3000);
        }

        function updateStats() {
            document.getElementById('stats').textContent = 
                `Games: ${gamesPlayed} | Wins: ${wins} | Losses: ${losses}`;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    # Generate a random target number for each game
    target_number = random.randint(1, 10)
    return render_template_string(HTML_TEMPLATE, target_number=target_number)

@app.route("/api/play", methods=["POST"])
def play_game():
    """API endpoint for playing the game"""
    data = request.get_json()
    selected_number = data.get('number')
    target_number = random.randint(1, 10)
    
    if selected_number == target_number:
        return jsonify({
            "result": "win",
            "message": "Congratulations! You survived!",
            "target_number": target_number
        })
    else:
        return jsonify({
            "result": "lose", 
            "message": "Wrong guess! System crash initiated...",
            "target_number": target_number
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)