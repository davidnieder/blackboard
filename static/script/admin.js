function userdel(username, id)  {
    check = confirm("Den user "+ username +" wirklich löschen?");
    if (check)  {
        window.location.pathname = '/admin/user/'+ id +'/del';
    }
}

function setpw(userid)  {
    pw = prompt("Das neue Passwort:", "")
    if (pw == "")   {
        return false
    }
    else    {
        a = document.createElement('script');
        a.setAttribute('type','text/javascript');
        a.setAttribute('src','/static/script/sha1.js');
        document.getElementsByTagName('head')[0].appendChild(a);

        hash = SHA( pw );

        document.hiddenform.pw.value = hash;
        document.hiddenform.submit();
    }
}

function delpost()  {
    post = document.getElementById('postid').value;
    if (post != "") {
        window.location.pathname = '/admin/posts/' + post + '/';
    }
}
