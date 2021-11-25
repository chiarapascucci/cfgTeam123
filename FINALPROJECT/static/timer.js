$(document).ready(function(){

    $("#timer-select-len").change(function (){
        let btn_attr = $("#set-timer-btn").attr("disabled");
        console.log(btn_attr)
        if (btn_attr==="disabled"){
            console.log("change prop of button")
            $("#set-timer-btn").prop("disabled", false)
        }

    });

    $("#set-timer-btn").click(function(){
        console.log("in start timer js func");
        let selected_len = $("#timer-select-len").find(":selected").val();
        console.log(selected_len);
        let len_as_int = parseInt(selected_len, 10);
        console.log(len_as_int);
        let ms_timeout = len_as_int * 60000;
        console.log(ms_timeout);
        let now = new Date();
        let now_time = now.getHours()+":"+now.getMinutes()+":"+now.getSeconds();
        let now_date = now.getFullYear()+'-'+(now.getMonth()+1)+"-"+now.getDate();
        let entry_date = now_date + ' ' + now_time;
        console.log(entry_date);
        session_id = null;
        user_id = null;
        data_str = '{'
        $.ajax({
            type : 'POST',
            url : "http://127.0.0.1:5000/log-session-start",
            dataType : 'json',
            contentType : 'application/json',
            data : JSON.stringify({
                'user_id' : 2,
                'start_time' : entry_date,
                'requested_duration' : ms_timeout
            }),
            success : function(data){
                console.log("successful ajax request, data received: ")
                console.log(data)
                session_id = data[0][0];
                user_id = data[0][1];
                console.log("setting the timer for " ); console.log(ms_timeout);
                set_timer(session_id, user_id, ms_timeout);

            }
        });

    });
});

function set_timer(session_id, user_id, ms_timeout){
    setTimeout(function(){alert("time is up"); time_up(session_id, user_id)}, ms_timeout);
}

function time_up(session_id, user_id){

    let now = new Date();
    let now_time = now.getHours()+":"+now.getMinutes()+":"+now.getSeconds();
    let now_date = now.getFullYear()+'-'+(now.getMonth()+1)+"-"+now.getDate();
    let end_time = now_date + ' ' + now_time;
    $.ajax({
            type : 'POST',
            url : "http://127.0.0.1:5000/log-session-end",
            dataType : 'json',
            contentType : 'application/json',
            data : JSON.stringify({
                'user_id' : user_id,
                'end_time' : end_time,
                'session_id' : session_id
            }),

    });

}
