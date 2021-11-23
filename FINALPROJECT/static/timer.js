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
        let entry_date = now_date + ' ' + now_time
        console.log(entry_date)
        data_str = '{'
        $.ajax({
            type : 'POST',
            url : "http://127.0.0.1:5000/log-session-start",
            dataType : 'json',
            contentType : 'application/json',
            data : JSON.stringify({
                'user_id' : 1,
                'start_time' : entry_date,
                'requested_duration' : ms_timeout
            }),

        })
        console.log("ajax part sent")
        setTimeout(function (){alert("time is up");}, ms_timeout)

    });




});

