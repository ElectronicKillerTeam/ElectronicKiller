
var game = new GameClass();
window.socket = null;
function myUnescape(value) {
    var result = '';
    var i = 0;
    for (i = 0; i < value.length;) {
        if (i < value.length - 2 && value[i] == '\\' && value[i + 1] == '\\' && value[i + 2] == 'u') {
            result += '%u';
            i += 2;
        } else if (i < value.length - 1 && value[i] == '\\' && value[i + 1] == 'u') {
            result = result + '%u';
            i += 1;
        }
        else
            result = result + value[i];
        i++;
    }
    console.log(result);
    return unescape(result)
}
function getSocket() {
    var sid = $('#sid').text();
    var socket = new WebSocket('ws://127.0.0.1:10911/chat?sid=' + sid);

    socket.onopen = function () {
        console.log('WebSocket open');
    };
    socket.onclose = function () {
        console.log('exit');
    }
    socket.onmessage = function (e) {
        data = JSON.parse(myUnescape(e.data))
        if (data.type == 'message') {
            $('#chatList').append('<div>' + data.user.username + ':' + data.message + '</div>');
            $('#chatInput').val('');
        } else if (data.type == 'command') {
            if (data.command == 'close') {
                $('#chatList').append('<div>您已在另一处登陆，本网页已下线。</div>');
            } else if (data.command == 'start') {
                window.location.href = '/online';
            }
        } else if (data.type == 'info') {
            switch (data.info) {
                case 'login': game.EnterHouse(data.user);
                    break;
                case 'exit': game.ExitHouse(data.user);
                    break;
            }
        }
    }
    return socket;
}

$('#chatForm').submit(function () {
    if (window.socket == null)
        return false;
    var content = $('#chatInput').val();
    if (content.length == 0)
        return false;
    window.socket.send(escape(content));
    return false;
});

$().ready(function () {
    window.socket = getSocket()

    var user_data = $('#user_data').text();
    if (user_data != '') {
        var items = $.parseJSON(user_data);
        $.each(items, function (i, user) {
            game.EnterHouse(user);
        });
    }
})

$('#startGameForm').submit(function () {
    //var form = $('#startGameForm');
    //var users = game.GetHouseUsers();
    //$('#startGameForm input[name="users"]').val(users);
    window.socket.send(escape('startgame'));
    return false;
})