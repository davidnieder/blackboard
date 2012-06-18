function checkForm()
{
    var user = document.getElementById('username');
    var pass1 = document.getElementById('password_1');
    var pass2 = document.getElementById('password_2');
    var pass = document.getElementById('password');
    var email = document.getElementById('email');

    if(user.value == '')  {
        alert('Please enter a username.');
        user.focus();
        return false;
    }
    if(pass1.value == '') {
        alert('Please enter a password.');
        pass1.focus();
        return false;
    }
    if(pass1.value != pass2.value)    {
        alert('The entered password do not match.');
        pass1.focus();
        return false;
    }
    if(email.value == '') {
        alert('Please enter an email address.');
        email.focus();
        return false;
    }
    if(email.value.indexOf('@') == -1 ||
        email.value.indexOf('.') == -1)    {
        alert('Please enter a valid email address.');
        email.focus();
        return false;
    }

    var hashed_pw = SHA(pass1.value);
    pass.value = hashed_pw;

    return true;
}
