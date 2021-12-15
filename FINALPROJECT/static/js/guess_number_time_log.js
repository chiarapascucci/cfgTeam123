let gameStateStorage = document.getElementById("game-state")

// logs player end the game and updates end time in database
window.addEventListener('beforeunload', (e) => {
    let gameState = gameStateStorage.innerHTML
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/guess-num-end", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
})
