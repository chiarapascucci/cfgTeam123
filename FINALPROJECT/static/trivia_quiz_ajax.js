function htmlDecode(input) {
  var doc = new DOMParser().parseFromString(input, "text/html");
  return doc.documentElement.textContent;
}

function answer_clicked(answer, game_id){
    console.log(answer + game_id)
    $.ajax({
        type : 'GET',
        url : "http://127.0.0.1:5000/trivia-quiz/" + game_id + "/check-answer/" + answer,
        dataType : 'json',
        contentType : 'application/json',
        success: function(data){
            console.log("ajax success: data received")
            console.log(data)
            $('#correct').text(data)
            question = $('#question')
            answers = $('#answers')
            $.ajax({
                type : 'GET',
                url : "http://127.0.0.1:5000/trivia-quiz/" + game_id + "/next-question",
                dataType : 'json',
                contentType : 'application/json',
                success: function(data){
                        question.text(htmlDecode(data['question']))
                        cor_ans = data['correct_answer']
                        console.log(cor_ans)
                        inc_ans = data['incorrect_answers']
                        console.log(inc_ans)
                        all_ans = inc_ans.concat(cor_ans)
                        console.log(all_ans)
                        buttons_html = ''
                        for (i = 0; i < all_ans.length; i++) {
                            ans_text = all_ans[i]
                            buttons_html += '<button onclick="answer_clicked(\''+ans_text+'\','+game_id+')">' + ans_text + '</button>'
                        }
                        answers.html(buttons_html)
                    }
            });
        }
    });
}
//
//let gameStateStorage = document.getElementById("game-state")
//
//window.addEventListener('load', (e) => {
//    logTriviaStartGame()
//    console.log('Trivia is fully loaded');
//})
//
//
//window.addEventListener('beforeunload', (e) => {
//    e.returnValue = 'Are you sure you want to leave?'
//    logTriviaEndGame()
//    console.log("Trivia FIRED")
//})
//
//// logs player start game and creates new database record
//function logTriviaStartGame() {
//    console.log('start game function')
//    let xhr = new XMLHttpRequest()
//    xhr.open('GET', "http://127.0.0.1:5000/trivia-game-record", true)
//    xhr.onload = function() {
//        if (xhr.status == 200) {
//            let gameState = JSON.parse(this.response)
//            gameStateStorage.innerHTML = JSON.stringify(gameState)
//            }
//        }
//    xhr.send()
//    }
//
//
//// logs player end the game and updates end time in database
//function logTriviaEndGame() {
//    let gameState = gameStateStorage.innerHTML
//    let xhr = new XMLHttpRequest()
//    xhr.open('POST', "http://127.0.0.1:5000/trivia-end", true)
//    xhr.setRequestHeader("Content-Type", "application/json")
//    xhr.send(gameState)
//}
