/* post functions */

function showPost() {
  var post_id = document.getElementById('post_id').value;
  if( post_id != '' ) {
    window.location.pathname = '/admin/post/' + post_id + '/';
  }
}

function delPost(post_id)  {
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/post/';

  setting_form[0].value = 'delete';
  setting_form[1].value = post_id;

  var check = confirm('Do you realy want do delete post #' + post_id);
  if( check ) {

    setting_form.submit();
  }
}

function setPublic(post_id, value)  {
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/post/';

  setting_form[0].value = 'public';
  setting_form[1].value = post_id;

  if( value ) {
    setting_form[2].value = 'True';
  }
  else  {
    setting_form[2].value = 'False';
  }

  setting_form.submit();
}

/* user functions */

function setPw(user_id)
{
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/user/';

  var pw = '';
  while( pw == '' )  {
    pw = prompt('Enter new password:');
  }
  if(pw == null)
    return;

  setting_form[0].value = 'password';
  setting_form[1].value = user_id;
  setting_form[2].value = SHA(pw);

  setting_form.submit();
}

function deleteUser(user_id)
{
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/user/';

  setting_form[0].value = 'delete';
  setting_form[1].value = user_id;

  var check = confirm('Do you realy want to delete the user with id ' + user_id);
  if( check ) {
    setting_form.submit();
  }
}

function setActive(user_id, active)
{
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/user/';

  setting_form[0].value = 'activate';
  setting_form[1].value = user_id;
  if(active)
    setting_form[2].value = 'True';
  else
    setting_form[2].value = 'False';

  setting_form.submit();
}

/* comment functions */

function showComment()
{
  var comment_id = document.getElementById('comment_id').value;
  if(comment_id != '')  {
    window.location.pathname = '/admin/comment/' + comment_id + '/';
  }
}

function deleteComment(comment_id)
{
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/comment/';

  setting_form[0].value = 'delete';
  setting_form[1].value = comment_id;

  setting_form.submit();
}

/* general settings */
function changeSetting(setting)
{
  var setting_form = document.getElementById('setting_form');
  setting_form.action = '/admin/settings/';

  setting_form[0].value = setting;

  value = document.getElementById(setting).value;
  if(value == null)
    return;
  setting_form[1].value = value;

  setting_form.submit();
}
