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

// will need to refactor this to follow DRY principles better
function take_guess(){
    let comp_num = $('#comp-num').val();
    let hum_num = $('#guess').val();
    let guess_num = $('#guess-count').val();

    $.ajax({
        url : "http://127.0.0.1:5000/number-ajax",
        dataType: 'json',
        type : 'POST',
        contentType : 'application/json',
        data : JSON.stringify({
            'comp_num': comp_num,
            'human_num': hum_num,
            'no_of_guesses' : guess_num
        }),
        success : function(data){
            let p_msg = $('#display-msg');
            if (data['game_end']){
                p_msg.text(data['msg']);
                reset_game();
            }
            else if (data['human_win']){
                p_msg.text(data['msg']);
                reset_game();
            }
            else {
                p_msg.text(data['msg']);
                $('#guess-count').val(data['guess_no']);
                $('#guess').val('');
            }
        }

    });

}

function reset_game(){
    setTimeout(function(){
        $('#comp-num').val(Math.floor(Math.random() * 201));
        $('#guess').val('');
        $('#guess-count').val(0);
        $('#display-msg').text("let's play again");
    }, 1500)
}
