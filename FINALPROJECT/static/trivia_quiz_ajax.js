
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
                    success: function(data)
                        question.text(data['question'])
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