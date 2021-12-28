$(document).ready(function() {
    $('.like-form').submit(function(e) {
        e.preventDefault();
        const video_id = $('.like-btn').val()
        const token = $('input[name=csrfmiddlewaretoken]').val()
        var user = $('.user').val()
        const url = $(this).attr('action')
        $.ajax({
            method: "POST",
            url: url,
            headers: { 'X-CSRFToken': token },
            data: {
                'video_id': video_id
            },
            success: function(response) {
                var divid = $(this.parentNode.parentNode).id;
                $.scrollTo($(divid), 500);

            }
        })
    })



})