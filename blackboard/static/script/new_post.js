function initializeAjaxUpload()   {
  upload = new AjaxUpload('browse_filesystem', {
            action: upload_handler,
            name: 'file',
            data:   {
                csrf_token: document.getElementById('csrf_token').value
            },
            autoSubmit: false,
            onChange: function(file,extension){ write_filename(file,extension); },
            onSubmit: function(){ upload_started(); },
            onComplete: function(file,response){ upload_finished(file, response); }
          });
}

function write_filename(file,extension) {
    document.getElementById('file_name').value = file;
}

function upload_started()    {
    // disable upload fields
    document.getElementById('file_name').disabled = true;
    document.getElementById('browse_filesystem').disabled = true;
    document.getElementById('start_upload').disabled = true;
    // hide allowed file extensions
    document.getElementById('file_extensions').style.display = 'none';
    // show progress bar
    document.getElementById('progress_bar').style.display = 'block';
    // hide error message
    document.getElementById('upload_error').style.display = 'none';
}

function upload_finished(file,response)  {
    // hide progress bar
    document.getElementById('progress_bar').style.display = 'none';

    if( response.error == 'true' )    {
        // show error message
        document.getElementById('upload_error').style.display = 'block';
        // enable upload fields
        document.getElementById('file_name').value = "";
        document.getElementById('browse_filesystem').disabled = false;
        document.getElementById('start_upload').disabled = false;
        document.getElementById('file_extensions').style.display = 'block';
        // show switch to url link
        document.getElementById('switch_link').style.display = 'block';
    }
    else    {
        // show success message
        document.getElementById('upload_finished').style.display = 'block';
        // enable post-submit button
        document.getElementById('submit_button').disabled = false;
        // write url of the just uploaded file
        if( upload_type == 'audio' )    {
            document.getElementById('post_content').value =
                '<audio controls="controls" preload="none" src="' + response.url + '">' +
                'Your Browser does not support the audio tag' +
                '</audio>';
        }
        if( upload_type == 'image' )    {
            document.getElementById('post_content').value = response.url;
        }

        // update csrf token
        document.getElementById('csrf_token').value = response.csrf_token;
    }
}

function startUpload()  {
    document.getElementById('switch_link').style.display = 'none';
    upload.submit();
}

function switch_to_upload( trigger )    {
    if( trigger ) {
        // hide url field, show upload div
        document.getElementsByName('url_post')[0].style.display = 'none';
        document.getElementsByName('url_post')[1].style.display = 'none';
        document.getElementsByName('upload_post')[0].style.display = 'table-row';
        document.getElementsByName('upload_post')[1].style.display = 'table-row';
        // disable submit button
        document.getElementById('submit_button').disabled = true;
    }
    else  {
    // vice versa
        document.getElementsByName('upload_post')[0].style.display = 'none';
        document.getElementsByName('upload_post')[1].style.display = 'none';
        document.getElementsByName('url_post')[0].style.display = 'table-row';
        document.getElementsByName('url_post')[1].style.display = 'table-row';
        document.getElementById('submit_button').disabled = false;
    }
}

function submitPost()
{
    form = document.getElementById('postForm');
    document.getElementById('postFormTitle').value = document.getElementById('post_title').value;
    document.getElementById('postFormContent').value = document.getElementById('post_content').value;

    if( post_type != 'text' )
        document.getElementById('postFormComment').value = document.getElementById('post_comment').value;

    if( document.getElementById('public_post').checked )
        document.getElementById('postFormIsPublic').value = 'True'
    else
        document.getElementById('postFormIsPublic').value = 'False'

    document.getElementById('postFormContentType').value = post_type;

    form.submit();
}

window.onload = function() { initializeAjaxUpload(); };
