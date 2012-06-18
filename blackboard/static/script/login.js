function checkForm()
{
    var user_field = document.getElementById('username');
    var pass_field = document.getElementById('password');
    var hashed_pass_field = document.getElementById('hashed_pw');
    var remember_field = document.getElementById('remember_me');

    if(user_field.value == '')    {
        alert('Please enter your username.');
        user_field.focus();
        return false;
    }
    if(pass_field.value == '')    {
        alert('Please enter your password.');
        pass_field.focus();
        return false;
    }

    pw_hash = SHA(pass_field.value);
    hashed_pass_field.value = pw_hash;

    return true;
}
