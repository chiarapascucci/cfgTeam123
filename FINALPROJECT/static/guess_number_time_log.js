let gameStateStorage = document.getElementById("game-state")

window.addEventListener('load', (e) => {
    logGuessNumberStartGame()
    console.log('Tic Tac is fully loaded');
})


window.addEventListener('beforeunload', (e) => {
    e.returnValue = 'Are you sure you want to leave?'
    logGuessNumberEndGame()
    console.log("Tic Tac FIRED")
})

// logs player start game and creates new database record
function logGuessNumberStartGame() {
    console.log('start game function')
    let xhr = new XMLHttpRequest()
    xhr.open('GET', "http://127.0.0.1:5000/guess-num-game-record", true)
    xhr.onload = function() {
        if (xhr.status == 200) {
            let gameState = JSON.parse(this.response)
            gameStateStorage.innerHTML = JSON.stringify(gameState)
            }
        }
    xhr.send()
    }


// logs player end the game and updates end time in database
function logGuessNumberEndGame() {
    let gameState = gameStateStorage.innerHTML
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/guess-num-end", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
}

$(document).ready(function(){
    let btn = $('#take-guess')
    btn.click(function(){
        let input_val = $('#guess').val()
        if (!input_val || input_val <=0){
            console.log(btn.val())
            alert("please enter a valid number to play");
        }
        else {
            take_guess();
        }

    });

});