function htmlDecode(input) {
  var doc = new DOMParser().parseFromString(input, "text/html");
  return doc.documentElement.textContent;
}

function answer_clicked(answer, game_id){
    console.log(answer + game_id)
    $.ajax({
        type : 'POST',
        url : "http://127.0.0.1:5000/trivia-quiz/" + game_id + "/check-answer",
        dataType : 'json',
        data: '{"user_answer": "' + answer + '"}',
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
                    next_question = data['next_question']
                    question_num = data['question_num']
                    if (next_question == null){
                        question.text('Score: ' + data['score'])
                        answers.html('')
                        $('#correct').text('')
                    } else {
                        question.text('Question ' + question_num + ': ' + htmlDecode(next_question['question']))
                        all_ans = next_question['answers']
                        console.log(all_ans)
                        buttons_html = ''
                        for (i = 0; i < all_ans.length; i++) {
                            ans_text = all_ans[i]
                            buttons_html += '<button class= "trivia-button" onclick="answer_clicked(`'+ans_text+'`,'+game_id+')">' + ans_text + '</button>'
                        }
                        answers.html(buttons_html)
                    }

                }

            });
        }
    });
}