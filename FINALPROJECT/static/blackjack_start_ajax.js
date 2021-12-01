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
            console.log('success')
            let blackjack_cards = JSON.parse(this.response)
            console.log(blackjack_cards)
            playerScore.innerHTML = blackjack_cards[4][0]
            dealerScore.innerHTML = blackjack_cards[4][1]
            gameStateStorage.innerHTML = blackjack_cards
        }
    }
    xhr.send()
}

function playerStand() {
    const gameState = {
        name: 'Daisy',
        age: 35
    }

    const jsonString = JSON.stringify(gameState)
    console.log(jsonString)
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/blackjack-player-stand", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(jsonString)
}