$(document).ready(function(){

    // this function get executes every time a page loads
    // it checks to see if there a required break len in the session data
    // if so it means that the user has started a session
    if(sessionStorage.getItem("req_len")){
        //declaring interval var
        const my_interval = setInterval(function () {
            console.log("in first func")

            // gettting the value of the req len in the current session
            let req_len = sessionStorage.getItem("req_len")
            let interval = parseInt(req_len, 10)
            console.log(interval)
            console.log(typeof interval)
            // substracting a second (set to equal the second paramenter to set interval)
            let time_left = interval - 1000;

            // updating session storage
            sessionStorage.setItem("req_len", time_left.toString())
            console.log("time left")
            console.log(time_left)

            //checking if time has run out
            if (time_left <= 0) {
                let session_id = sessionStorage.getItem("session_id");
                let user_id = sessionStorage.getItem("user_id");
                alert("time is up");
                time_up(session_id, user_id);

                clearInterval(my_interval);
            }
        }, 1000);
    }

    // when a timer length is selected button should be enabled
    $("#timer-select-len").change(function (){
        let btn_attr = $("#set-timer-btn").attr("disabled");
        console.log(btn_attr)
        if (btn_attr==="disabled"){
            $("#set-timer-btn").prop("disabled", false)
        }

    });

    // when the start timer button is pressed timer starts
    $("#set-timer-btn").click(function(){
        console.log("in start timer js func");
        // getting value of requested length from user selection
        let selected_len = $("#timer-select-len").find(":selected").val();
        // converting it to an int
        let len_as_int = parseInt(selected_len, 10);

        // getting the value in ms
        let ms_timeout = len_as_int * 60000;

        // getting the current timedate object
        let now = new Date();
        let now_time = now.getHours()+":"+now.getMinutes()+":"+now.getSeconds();
        let now_date = now.getFullYear()+'-'+(now.getMonth()+1)+"-"+now.getDate();
        //forming a string with current timedate in correct format
        let entry_date = now_date + ' ' + now_time;

        let user_id = parseInt($('#session-info').attr('data'));
        console.log(user_id)

        // forming ajax request to server
        $.ajax({
            type : 'POST',
            url : "http://127.0.0.1:5000/log-session-start",
            dataType : 'json',
            contentType : 'application/json',
            data : JSON.stringify({
                'user_id' : user_id,
                'start_time' : entry_date,
                'requested_duration' : ms_timeout
            }),
            success : function(data){
                console.log("successful ajax request, data received: ")
                console.log(data)
                let session_id = data.result[0][0];
                let user_id = data.result[0][1];
                console.log("session id and user id fetched from ajax req: ")
                console.log(session_id)
                console.log(user_id)
                // setting session object to information needed
                // all data is saved as strings (unfortunately)
                sessionStorage.setItem("req_len", ms_timeout.toString());
                sessionStorage.setItem("user_id", user_id);
                sessionStorage.setItem("session_id", session_id);
                console.log(sessionStorage.getItem('user_id'))
                let redirect_url = data.redirect_url
                window.location.replace(redirect_url)



            }
        });

    });
});


function time_up(session_id, user_id){
    console.log("in time up js func")
    console.log("session id and user id are")
    console.log(session_id, user_id)
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
