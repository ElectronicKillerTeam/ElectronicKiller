
function getSocket() {
    var sid = $('#sid').text();
    var socket = new WebSocket('ws://127.0.0.1:10911/onlinesocket?sid=' + sid);

    socket.onopen = function () {
        console.log('WebSocket open');
    };
    socket.onclose = function () {
        console.log('WebSocket close');
    }
    socket.onmessage = function (e) {
        console.log(e.data);
        data = JSON.parse(myUnescape(e.data))
        switch (data.type) {
            case 'info':
                if (data.content == 'ready') {
                    GetMoreCard(4, 0);
                }
                break;
            case 'getcards':
                SetUserCardCount(data.userid, data.count);
                break;
        }
    }
    return socket;
}


$().ready(function () {
    window.socket = getSocket();
    //GetMoreCard(4);
})

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

//传入卡牌，将卡牌显示在页面自己的位置上
function ShowCard(cards) {
    var mypanel = $('#mypanel');
    var content = '<div class="card col-md-1"><div>{0}</div><div>{1}</div><div class="f14 mt10">{2}</div></div>';
    for (var i = 0; i < cards.length; i++) {
        mypanel.append($.format(content, cards[i].CardNum,cards[i].CardName,cards[i].Description));
    }
    var count = $('#mypanel .card').length;
    $('#selfusercard .cardcount').text(count);
}

$.format = function (source, params) {
    if (arguments.length == 1)
        return function () {
            var args = $.makeArray(arguments);
            args.unshift(source);
            return $.format.apply(this, args);
        };
    if (arguments.length > 2 && params.constructor != Array) {
        params = $.makeArray(arguments).slice(1);
    }
    if (params.constructor != Array) {
        params = [params];
    }
    $.each(params, function (i, n) {
        source = source.replace(new RegExp("\\{" + i + "\\}", "g"), n);
    });
    return source;
};

$('#getMoreCard').click(function () {
    var count = $('#mypanel .card').length;
    GetMoreCard(2, count);
});

//从服务器请求更多的卡牌
function GetMoreCard(count, hasCount) {
    $.ajax({
        url: '/getcards',
        type: 'GET',
        dataType: 'json',
        data: {
            'count': count,
            'hasCount': hasCount
        },
        success: function (data) {
            ShowCard(data);
        },
        error: function (e) {
            alert(e);
        }
    });
}

function SetUserCardCount(userid, count) {
    $('[name=' + userid + '] .cardcount').text(count);
}