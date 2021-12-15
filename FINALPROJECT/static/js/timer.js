$(document).ready(function(){

    // this function get executes every time a page loads
    // it checks to see if there a required break len in the session data
    // if so it means that the user has started a session
    if(sessionStorage.getItem("req_len")){
        //declaring interval var
        const my_interval = setInterval(function () {

            // gettting the value of the req len in the current session
            let req_len = sessionStorage.getItem("req_len")
            let interval = parseInt(req_len, 10)
            // substracting a second (set to equal the second paramenter to set interval)
            let time_left = interval - 1000;

            // updating session storage
            sessionStorage.setItem("req_len", time_left.toString())

            //checking if time has run out
            if (time_left <= 0) {
                let session_id = sessionStorage.getItem("session_id");
                let user_id = sessionStorage.getItem("user_id");
                sessionStorage.clear();
                alert("time is up");
                clearInterval(my_interval);
                time_up(session_id, user_id);

            }
        }, 1000);
    }

    // when a timer length is selected button should be enabled
    $("#timer-select-len").change(function (){
        let btn_attr = $("#set-timer-btn").attr("disabled");
        if (btn_attr==="disabled"){
            $("#set-timer-btn").prop("disabled", false)
        }

    });

    // when the start timer button is pressed timer starts
    $("#set-timer-btn").click(function(){
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

        // forming ajax request to server
        // this request instructs the server to hit the database amd create a new entry in the sessions table
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
            // upon successful completion of the request
            // user and session id are stored in sessionstorage
            // and user is redirected to browsegames page
            success : function(data){
                let session_id = data.result[0][0];
                let user_id = data.result[0][1];

                // setting session object to information needed
                // all data is saved as strings (unfortunately)
                sessionStorage.setItem("req_len", ms_timeout.toString());
                sessionStorage.setItem("user_id", user_id);
                sessionStorage.setItem("session_id", session_id);

                let redirect_url = data.redirect_url
                window.location.replace(redirect_url)

            }
        });

    });
});

// this function gets called when the timer expires
function time_up(session_id, user_id){
    let now = new Date();
    // it captures the current date and time
    let now_time = now.getHours()+":"+now.getMinutes()+":"+now.getSeconds();
    let now_date = now.getFullYear()+'-'+(now.getMonth()+1)+"-"+now.getDate();
    let end_time = now_date + ' ' + now_time;
    // having collected the required data it instructs the server to hit the database
    // to update the relevant sessions entry with an end time
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
            success: function(data){
                // upon completion the user is logged out
                let redirect_url = data.redirect_url;
                window.location.replace(redirect_url);
            }

    });

}
