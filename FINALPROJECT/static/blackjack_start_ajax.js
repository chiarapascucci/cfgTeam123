let dealerScore = document.getElementById("dealer-score-value")
let playerScore = document.getElementById("player-score-value")
let winner = document.getElementById("display-winner")
let gameStateStorage = document.getElementById("game-state")

// this function is called when the start game button has been clicked
// it call the starter cards and displays the cards values on the HTML game board
function startGame() {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', "http://127.0.0.1:5000/blackjack-start", true)
    xhr.onload = function() {
        if (xhr.status == 200) {
            let gameState = JSON.parse(this.response)
            console.log(gameState)
            if (gameState['is_blackjack_true']) {
                winner.innerHTML = "Blackjack, Player Wins"
            } else {
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                winner.innerHTML = ""
                gameStateStorage.innerHTML = JSON.stringify(gameState)
            }
        }
    }
    xhr.send()
}

function playerStand() {
    let gameState = gameStateStorage.innerHTML
    console.log(gameState)
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/blackjack-player-stand", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
    xhr.onload = function() {
        if (xhr.status == 200) {
            let winner = JSON.parse(this.response)
            playerScore.innerHTML = winner
            dealerScore.innerHTML = ""
            }
        }
    }

function playerHit() {
    let gameState = gameStateStorage.innerHTML
    console.log(gameState)
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/blackjack-player-hit", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
    xhr.onload = function() {
            let gameState = JSON.parse(this.response)
            console.log(gameState)
            if (gameState['winner'] == false) {
                console.log('if loop')
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                winner.innerHTML = "Player Bust, Dealer Wins"
            } else {
                console.log('else loop')
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                gameStateStorage.innerHTML = JSON.stringify(gameState)
            }
        }
    }
