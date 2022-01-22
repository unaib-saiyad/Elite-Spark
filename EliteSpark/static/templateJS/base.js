
var wsStart = 'ws://';
var host = window.location.host;
var user_id = $("input[name='user-id']").val();

var notify_url = wsStart + host + '/notification/' + user_id;

const notificationSocket = new WebSocket(notify_url);

function NotificationSend(){
    notificationSocket.send(JSON.stringify({
        'process': 'unopened_notifications_count',
        'user-id': user_id,
    }));
}


notificationSocket.onopen = function () {
    NotificationSend();
};

notificationSocket.onerror = function(e){
    console.error("error", e)
}

notificationSocket.onmessage = function(e) {
    data = JSON.parse(e.data);
    console.log(data);
    $('#all-notification-counter').html(data['count']);
    $('#friend-notification-counter').html(data['friend_notice_count']);
}

$(function () {
    //Add text editor
    $('#compose-textarea').summernote()
});

$("input[name=search]").on('keyup', function () {
    let query = $(this).val();
    if (query.length === 0) {
        $('#main-content-section').css('display', 'block');
        $('#search-query-content').css('display', 'none');
    } else {
        $('#main-content-section').css('display', 'none');
        $('#search-query-content').css('display', 'block');
        let url = window.location.origin + '/user/api/search/query/';
        $.ajax({
            async: true,
            method: "GET",
            url: url,
            data: {
                'query': query,
            },
            success: function (response) {
                if (response.length != 0) {
                    $('#search-content').empty();
                } else {
                    $('#search-content').html("No such results!...");
                }
                response.forEach(student => {
                    let tag = "";
                    let roll_number = "";
                    let standard = "";
                    if (student.tag) {
                        tag = student.tag;
                    }
                    if (student.roll_number) {
                        roll_number = student.roll_number;
                    }
                    if (student.standard) {
                        standard = student.standard;
                    }
                    $('#search-content').append(`
                        <div class="col-md-4">
                            <!-- Widget: user widget style 1 -->
                            <div class="card card-widget widget-user">
                                <!-- Add the bg color to the header using any of the bg-* classes -->
                                <div class="widget-user-header text-white"
                                    style="background: url('`+ window.location.origin +`/static/dist/img/photo1.png') center center;">
                                    <a href="`+ window.location.origin +`/user/profile/` + student.user +
                        `"
                                     class="widget-user-username text-right" style="text-decoration: none; color: white;">` +
                                        student.user + `</a>
                                    <h5 class="widget-user-desc text-right">` + tag + `</h5>
                                </div>
                                <div class="widget-user-image">
                                    <img class="img-circle" src="` + student.profile + `" alt="User Avatar">
                                </div>
                                <div class="card-footer">
                                    <div class="row">
                                        <div class="col-sm-4 border-right">
                                            <div class="description-block">
                                                <h5 class="description-header">` + standard + `</h5>
                                                <span class="description-text">STANDARD</span>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 border-right">
                                            <div class="description-block">
                                                <h5 class="description-header">` + student.friends_count + `</h5>
                                                <span class="description-text">FRIENDS</span>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4">
                                            <div class="description-block">
                                                <h5 class="description-header">` + roll_number + `</h5>
                                                <span class="description-text">ROLL NUMBER</span>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                            </div>
                            <!-- /.widget-user -->
                        </div>
                        <!-- /.col -->
                    `);
                });
            }
        });
    }
});

// Friend request
function friendRequest(username) {
    $('#friend-request-content').css('display', 'block');
    $('#main-content-section').css('display', 'none');
    $('#friend-request-list').empty();
    let url = window.location.origin + '/user/api/friend-request/receiver';
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            'receiver': username,
        },
        success: function (response) {
            response.forEach(element => {
                if (element.status === true) {
                    $('#friend-request-list').append(`
                    <li>
                        <img src="`+ element.sender_profile +`" alt="User Image">
                        <a class="users-list-name" href="`+ window.location.origin +`/user/profile/`+ element.sender +`">
                            `+ element.sender +`
                        </a>
                        <span class="users-list-date">`+ element.timestamp +`</span>
                    </li>
                    `);
                }
                else{
                    console.log("Reloading...");
                    location.reload();
                }
            });
        }
    });
}

// Add friend request
function addFriend(username){
    let url = window.location.origin + '/user/friend-request/' + username;
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            'receiver': username,
        },
        success: function (response) {
            if(response['Status'] === true){
                $('#friends-button').html('Requested');
            }
            else{
                $('#friends-button').html('Add Friend');
            }
        }
    });
}

function friendToMain() {
    $('#friend-request-content').css('display', 'none');
    $('#main-content-section').css('display', 'block');
}

function StudentData(username) {
    let url = window.location.origin + "/user/api/student/data";
    var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
    let user_id = $("input[name='user-id']").val();
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            'username': username,
        },
        success: function (response) {
            $('.user-profile-image').attr('src', response[0].profile);
            $('#user-prn').html(response[0].prn);
            $('#user-friends').html(response[0].friends_count);
            $('#user-fullname').html(response[0].full_name);
            if (response[0].roll_number != null) {
                $('.user-rollnumber').html(response[0].roll_number);
                $('#input-rollnumber').val(response[0].roll_number);
            }
            if (response[0].standard != null) {
                $('.user-standard').html(response[0].standard);
                $('#user-standard-' + response[0].standard).attr("selected", "selected");
            }
            if (response[0].tag != null) {
                $('#input-user-tag').val(response[0].tag);
                let tag = response[0].tag;
                if (response[0].tag.length > 20) {
                    tag = response[0].tag.slice(0, 19) + '...';
                }
                $('.user-tag').html(tag);
            }
            if (response[0].standard != null) {
                $('#user-privacy-' + response[0].account_scope).attr("selected", "selected");
            }
            if(response[0].friends.includes(parseInt(user_id))){
                $('#add-friends-btn').html(`
                <button onclick="removeFriend('` + username + `')" id="remove-friends-button"
                    class="btn btn-primary btn-block">Remove Friend</button>
            `);
            }
        }
    });
}