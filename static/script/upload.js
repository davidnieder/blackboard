function initializeAjaxUpload()   {
  upload = new AjaxUpload('upload_button', {
            action: upload_handler,
            name: 'file',
            autoSubmit: false,
            onChange: function(file,extension){ write_filename(file,extension); },
            onSubmit: function(){ upload_started(); },
            onComplete: function(file,response){ upload_finished(file,response); }
          });
}

function write_filename(file,extension) {
  document.getElementById('filename').value = file;
}

function upload_started()    {
  // disable upload fields
  document.getElementById('filename').disabled = true;
  document.getElementById('upload_button').disabled = true;
  document.getElementById('start_upload').disabled = true;
  // hide allowed file extensions
  document.getElementById('file_extensions').style.display = 'none';
  // show progress bar
  document.getElementById('progress_bar').style.display = 'block';
}

function upload_finished(file,response)  {
  // hide progress bar
  document.getElementById('progress_bar').style.display = 'none';

  if( response == "error" )   {
    // show error message
    document.getElementById('upload_error').style.display = 'block';
    // enable upload fields
    //document.getElementById('filename').disabled = false;
    document.getElementById('upload_button').disabled = false;
    document.getElementById('start_upload').disabled = false;
    document.getElementById('file_extensions').style.display = 'block';
    // show switch to url link
    document.getElementById('switch_link').style.display = 'block';
  }
  else    {
    // show success message
    document.getElementById('upload_finished').style.display = 'block';
    // write url of the just uploaded file
    document.getElementById('uploaded_file_url').value = response;
    // enable post-submit button
    document.getElementById('submit_button').disabled = false;
  }
}

function start()    {
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
  }
  else  {
    // vice versa
    document.getElementsByName('upload_post')[0].style.display = 'none';
    document.getElementsByName('upload_post')[1].style.display = 'none';
    document.getElementsByName('url_post')[0].style.display = 'table-row';
    document.getElementsByName('url_post')[1].style.display = 'table-row';
  }
}    

window.onload = function() { initializeAjaxUpload(); };
