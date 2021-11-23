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
        setTimeout(function (){alert("time is up");}, ms_timeout)

    });




});

