function browse_filesystem()    {
    /* create a form and a file input and click() the input */
    var form = document.getElementById('_upload_form');
    if(form == null)    {
        form = document.createElement('form');
        var input = document.createElement('input');

        form.setAttribute('id', '_upload_form');
        form.setAttribute('enctype', 'multipart/form-data');
        input.setAttribute('type', 'file');
        input.setAttribute('name', 'file');
        input.setAttribute('id', '_file_input');

        document.body.appendChild(form);
        form.appendChild(input);

        input.addEventListener('change', user_picked_file, false);
    }
    else    {
        var input = document.getElementById('_file_input');
    }
    input.click();
}

function user_picked_file() {
    /* write file name in file_name field */
    var file_name = document.getElementById('_file_input').value;
    document.getElementById('file_name').value = file_name;
}

function start_upload() {
    /* hide error message from previous upload */
    document.getElementById('upload_error').style.display = 'none';

    var form = document.getElementById('_upload_form');
    var csrf_token = document.getElementById('__csrf_token').value;
    if(form == null)    {
        return;
    }

    var form_data = new FormData(form);
    form_data.append('csrf_token', csrf_token);

    request = new XMLHttpRequest();
    request.open('POST', '/upload/?json=true', true);
    request.onreadystatechange = upload_state_changed;

    request.send(form_data);
}

function upload_state_changed() {
    if(request.readyState == 1 || request.readyState == 2 ||
       request.readyState == 3) {
        upload_processing();
    }
    else if(request.readyState == 4)    {
        upload_finished();
    }
}

function upload_processing()    {
    /* show process bar */
    document.getElementById('upload_status').style.display = 'block';
    /* disable inputs */
    document.getElementById('browse_filesystem').disabled = true;
    document.getElementById('start_upload').disabled = true;
}

function upload_finished()  {
    /* hide progress bar */
    document.getElementById('upload_status').style.display = 'none';
    /* enable inputs */
    document.getElementById('browse_filesystem').disabled = false;
    document.getElementById('start_upload').disabled = false;
    /* clear file name field */
    document.getElementById('file_name').value = '';

    /* eval json response */
    var response = eval('(' + request.responseText + ')');

    /* check http status code */
    if(request.status != 200)   {
        var error_area = document.getElementById('upload_error');
        error_area.style.display = 'block';

        if(request.status == 413)   {
            error_area.innerHTML = 'Upload failed: The file was too large';
        }
        else    {
            error_area.innerHTML = 'Upload failed';
        }
    }
    else    {
        if(response.error == 'true')   {
            var error_area = document.getElementById('upload_error');
            error_area.style.display = 'block';
            error_area.innerHTML = 'Upload failed';
        }
        else    {
            var resource_area = document.getElementById('uploaded_resources');
            if(resource_area.value == '')    {
                resource_area.value = response.url;
            }
            else    {
                resource_area.value += '\r\n' + response.url;
            }
        }
    }

    /* update csrf token for next request */
    document.getElementById('csrf_token').value = response.csrf_token;
    document.getElementById('__csrf_token').value = response.csrf_token;

    /* clean up document tree */
    var input = document.getElementById('_file_input');
    var form = document.getElementById('_upload_form');
    form.removeChild(input);
    document.body.removeChild(form);
}

