function profileInput() {
    $("#profile-input").click();
}
$('#profile-input').change(function () {
    var image = this.files[0];
    console.log(image);
    const url = window.URL.createObjectURL(image);
    console.log(url);
    $('#input-change-profile').attr('src', url);
});
username = window.location.pathname.slice(14, );
StudentData(username);

getRequestData(username);

// Get friend request data
function getRequestData(username) {
    let url = window.location.origin + '/user/get-friend-request/' + username;
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            'receiver': username,
        },
        success: function (response) {
            if (response['Status'] === true) {
                $('#friends-button').html('Requested');
            } else {
                getRequestedData(username);
            }
        }
    });
}

// Remove friend
function removeFriend(username) {
    let url = window.location.origin + '/user/remove-friend/';
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            'removee': username,
        },
        success: function (response) {
            if (response['Status'] === true) {
                $('#add-friends-btn').html(`
                    <button onclick="addFriend('` + username + `')" id="friends-button"
                            class="btn btn-primary btn-block">Add Friend</button>
                `);
            }
        }
    });
}

// Get friend request data
function getRequestedData(username) {
    let url = window.location.origin + '/user/get-requested-data/' + username;
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            'sender': username,
        },
        success: function (response) {
            if (response['Status'] === true) {
                $('#add-friends-btn').html(`
                <button onclick="actionOnFriendRequest('` + username + `', 'accept')" id="accept-friends-button"
                        class="btn btn-primary btn-block">Accept request</button>
                <button onclick="actionOnFriendRequest('` + username + `', 'reject')" id="reject-friends-button"
                    class="btn btn-danger btn-block">Reject request</button>
                `);
            }
            NotificationSend();
        }
    });
}

// Action on friend request
function actionOnFriendRequest(username, action) {
    let url = window.location.origin + '/user/accept-reject-request/' + username;
    $.ajax({
        async: true,
        method: "GET",
        url: url,
        data: {
            'sender': username,
            'action': action,
        },
        success: function (response) {
            if (response['Status'] === true) {
                if (action == 'accept') {
                    $('#add-friends-btn').html(`
                    <button onclick="removeFriend('` + username + `')" id="remove-friends-button"
                        class="btn btn-primary btn-block">Remove Friend</button>
                `);
                } else {
                    $('#add-friends-btn').html(`
                    <button onclick="addFriend('` + username + `')" id="friends-button"
                            class="btn btn-primary btn-block">Add Friend</button>
                `);
                }
            }
            NotificationSend();
        }
    });
}