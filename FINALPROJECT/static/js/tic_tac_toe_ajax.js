let gameStateStorage = document.getElementById("game-state")

// logs player end the game and updates end time in database
window.addEventListener('beforeunload', (e) => {
    let gameState = gameStateStorage.innerHTML
    let xhr = new XMLHttpRequest()
    xhr.open('POST', "http://127.0.0.1:5000/tic-tac-end", true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(gameState)
})


function cell_clicked(cel_num){
    let cell_id = "#c"+cel_num;
    let cell_selected = $(cell_id)

    let cell_sel_atr = cell_selected.attr("disabled");
    if (! cell_sel_atr){
        cell_selected.text('x');
        cell_selected.attr('disabled', true);
        play_comp_turn();
    }
}

function play_comp_turn(){
    const x_cells = [];
    const o_cells = [];
    let x_str = "";
    let o_str = "";
    for (let i =1; i<=9; i++){
        let id_str = "#c"+i.toString();
        let cell = $(id_str)
        let cell_dis_atr = cell.attr("disabled");
        if(cell_dis_atr){
            let val = cell.text();
            if (val === 'x'){
                x_cells.push(i);
                x_str = x_str +i.toString()
            } else if (val === 'o'){
                o_cells.push(i);
                o_str = o_str+i.toString()
            }
        }
    }


    $.ajax({
        type : 'POST',
        url : "http://127.0.0.1:5000/tic-tac-ajax",
        dataType : 'json',
        contentType : 'application/json',
        data : JSON.stringify({
            'x': x_str,
            'o' : o_str,
        }),
        success: function(data){
            let msg = $('#end-msg')
            let cell_id = "#c"+data['comp_move'];
            let cell = $(cell_id);
            if (data['game_end']){
                cell.text('o');
                cell.attr('disabled', true);
                msg.text("it's a tie!");
                setTimeout(function (){clear_table()}, 1500)
            }
            else if (data['comp_win']){
                cell.text('o');
                cell.attr('disabled', true);
                msg.text("I win!");
                setTimeout(function (){clear_table()}, 1500)
            }
            else if (data['hum_win']){
                msg.text("You win!");
                setTimeout(function (){clear_table()}, 1500)
            }
            else {
                let comp_move = data['comp_move'];
                let cell_id = "#c"+comp_move.toString();
                let cell = $(cell_id);
                cell.text('o');
                cell.attr('disabled', true);
            }
        }
    });
}

function clear_table(){
    for (let i =1; i<=9; i++){
        let id_str = "#c"+i.toString();
        let cell = $(id_str)
        cell.attr("disabled", false);
        cell.text("");
        let msg = $('#end-msg')
        msg.text("let's go again")

    }
}