function changeSetting(setting)
{
  var setting_form = document.getElementById('change_setting');
  var setting_field = document.getElementById('setting');
  var value_field = document.getElementById('value');
  var old_value_field = document.getElementById('old_value');

  if(setting == 'password') {
    var old_pass = document.getElementById('old_pass');
    var new_pass_1 = document.getElementById('new_pass_1');
    var new_pass_2 = document.getElementById('new_pass_2');

    if(old_pass.value == '')  {
      alert('Please enter your password.');
      old_pass.focus();
      return;
    }
    if(new_pass_1.value == '')  {
      alert('Please enter your new password.');
      new_pass_1.focus();
      return;
    }
    if(new_pass_1.value != new_pass_2.value)  {
      alert('The entered passwords do not match.');
      new_pass_1.focus();
      return;
    }

    var new_pw = SHA(new_pass_1.value);
    var old_pw = SHA(old_pass.value);

    setting_field.value = 'password';
    value_field.value = new_pw;
    old_value_field.value = old_pw;

    setting_form.submit();
  }
  else if(setting == 'email')  {
    var new_email = document.getElementById('new_email');

    if(new_email.value == '')   {
      alert('Please enter your new email address.');
      new_email.focus();
      return;
    }
    if(new_email.value.indexOf('@') == -1 ||
       new_email.value.indexOf('.') == -1 ) {
      alert('Bitte eine valide E-Mail-Adresse angeben');
      new_email.focus();
      return;
    }

    setting_field.value = 'email';
    value_field.value = new_email.value;

    setting_form.submit();
  }
  else if(setting == 'posts_per_page')  {
    var posts_per_page = document.getElementById('posts_per_page');

    setting_field.value = 'posts_per_page';
    for(var i=0; i<posts_per_page.length; i++)  {
      if(posts_per_page[i].selected)    {
        value_field.value = posts_per_page[i].value;
        break;
      }
    }

    setting_form.submit();
  }
  else if(setting == 'email_notification')  {
    var email_notification = document.getElementById('email_notification');

    setting_field.value = 'email_notification';
    if(email_notification[0].checked)
      value_field.value = 'False';
    else
      value_field.value = 'True';

    setting_form.submit();
  }
  else if(setting == 'facebook_integration') {
    var facebook_integration = document.getElementById('facebook_integration');

    setting_field.value = 'facebook_integration';
    if(facebook_integration[0].selected)
      value_field.value = 'False';
    else
      value_field.value = 'True';

    setting_form.submit();
  }
  else if(setting == 'template')    {
    var template = document.getElementById('template');

    setting_field.value = 'template';
    for(var i=0; i<template.length; i++)  {
      if(template[i].selected)  {
        value_field.value = template[i].value;
        break;
      }
    }

    setting_form.submit();
  }
}
