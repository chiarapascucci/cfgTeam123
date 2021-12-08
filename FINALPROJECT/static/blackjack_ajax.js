let dealerScore = document.getElementById("dealer-score-value")
let playerScore = document.getElementById("player-score-value")
let hitBtn = document.getElementById("hit")
let standBtn = document.getElementById("stand")
let winner = document.getElementById("display-winner")
let gameStateStorage = document.getElementById("game-state")

// this function is called when the start game button has been clicked
// it calls the starter cards and displays the cards values on the HTML game board
function startGame() {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', "http://127.0.0.1:5000/blackjack-start", true)
    xhr.onload = function() {
        if (xhr.status == 200) {
            let gameState = JSON.parse(this.response)
            if (gameState['is_blackjack_true']) {
                winner.innerHTML = "Blackjack, Player Wins"
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = ""
            } else {
                hitBtn.disabled = false
                standBtn.disabled = false
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                winner.innerHTML = ""
                gameStateStorage.innerHTML = JSON.stringify(gameState)
            }
        }
    }
    xhr.send()
}

// this function is called when the stand button has been clicked
// it displays the winner of the game
function playerStand() {
    let gameState = gameStateStorage.innerHTML
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/blackjack-player-stand", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
    xhr.onload = function() {
        if (xhr.status == 200) {
            let gameState = JSON.parse(this.response)
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                winner.innerHTML = gameState['winner']
                hitBtn.disabled = true
                standBtn.disabled = true
            }
        }
    }

//this function is called when the hit button has been clicked
// it displays if player has gone bust or can play again
function playerHit() {
    let gameState = gameStateStorage.innerHTML
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/blackjack-player-hit", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
    xhr.onload = function() {
            let gameState = JSON.parse(this.response)
            if (gameState['winner'] == false) {
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                winner.innerHTML = "Player Bust, Dealer Wins"
                hitBtn.disabled = true
                standBtn.disabled = true
            } else {
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                gameStateStorage.innerHTML = JSON.stringify(gameState)
            }
        }
    }
