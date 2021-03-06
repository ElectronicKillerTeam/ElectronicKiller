﻿function GameClass() {
    var me = this;
    var online_users = {};

    me.EnterHouse = function (userid,username) {
        if ($('#' + userid).length > 0)
            return
        $('#chatList').append('<div>' + username + '进入房间。</div>');
        var emptyPosiList = $('.no-user');
        if (emptyPosiList.length > 0) {
            var posi = emptyPosiList.first();
            posi.removeClass('no-user');
            posi.attr('id', userid);
            posi.append('<div>' + username + '</div>');
        }
    }
    me.ExitHouse = function (userid,username) {
        var posi = $('#' + userid)
        posi.removeAttr('id');
        posi.addClass('no-user');
        posi.empty();
        $('#chatList').append('<div>' + username + '已退出房间。</div>');
    }
    me.GetHouseUsers = function () {
        var cards = $('.user-card');
        var result = '';
        for (var i = 0; i < cards.length; i++) {
            var card = cards[i];
            var id = card.getAttribute('id');
            if (id != null) {
                result += id + ','
            }
        }
        return result;
    }
}

