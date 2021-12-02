let dealerScore = document.getElementById("dealer-score-value")
let playerScore = document.getElementById("player-score-value")
let gameStateStorage = document.getElementById("game-state")

// this function is called when the start game button has been clicked
// it call the starter cards and displays the cards values on the HTML game board
function startGame() {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', "http://127.0.0.1:5000/blackjack-start-ajax", true)
    xhr.onload = function() {
        if (xhr.status == 200) {
            let gameState = JSON.parse(this.response)
            console.log(gameState)
            if (gameState['is_blackjack_true']) {
                playerScore.innerHTML = "Blackjack, Player Wins"
            } else {
                playerScore.innerHTML = gameState['value_of_starting_hands'][0]
                dealerScore.innerHTML = gameState['value_of_starting_hands'][1]
                gameStateStorage.innerHTML = JSON.stringify(gameState)
            }
        }
    }
    xhr.send()
}

function playerStand() {
    let gameState = gameStateStorage.innerHTML
//    let jsonGameState = JSON.stringify(gameState)
    console.log(gameState)
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/blackjack-player-stand", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
}