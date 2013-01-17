function preview_post() {
    var form = document.getElementById('post_form');
    form.action = '/post/preview/';

    submit_post();
}

function edit_post(post_id)    {
    var form = document.getElementById('post_form');
    form.action = '/posts/' + post_id + '/edit/';

    submit_post();
}

function submit_post()  {
    var form = document.getElementById('post_form');
    var content = document.getElementById('post_content');

    if(content.value == '')
        return;

    form.submit();
}
