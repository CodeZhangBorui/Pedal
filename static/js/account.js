axios.get('/api/clients/account').then((result) => {
    let data = result.data;
    if (data.success) {
        document.querySelectorAll('#display-username').forEach((element) => {
            element.innerText = data.username;
        });
        document.querySelectorAll('#display-email').forEach((element) => {
            element.innerText = data.email;
        });
        document.querySelectorAll('#display-perm-level').forEach((element) => {
            element.innerText = data.permission;
        });
    } else{
        window.location.href = '/login';
    }
}).catch((err) => {
    window.location.href = '/login';
});

document.querySelector('form#changepass').addEventListener('submit', function(e) {
    e.preventDefault();
    let oldpass = e.target.querySelector('input[name="old-password"]').value;
    let newpass = e.target.querySelector('input[name="new-password"]').value;
    let newpass2 = e.target.querySelector('input[name="confirm-password"]').value;
    if (newpass !== newpass2) {
        swal({
            title: "修改密码失败",
            text: "两次输入的新密码不一致",
            icon: "error",
        });
        return;
    }
    axios.post('/api/clients/changepass', {
        'oldpass': oldpass,
        'newpass': newpass
    }).then((result) => {
        let data = result.data;
        if (data.success) {
            swal({
                title: "修改密码成功",
                text: "\n",
                icon: "success",
                buttons: false,
                closeOnClickOutside: false,
                closeOnEsc: false
            });
            setTimeout(function() {
                window.location.href = '/account';
            }, 1000);
        } else {
            swal({
                title: "修改密码失败",
                text: data.message,
                icon: "error",
            });
        }
    }).catch((error) => {
        swal({
            title: "修改密码失败",
            text: `网络错误：${error.message}`,
            icon: "error",
        });
        console.log(error)
    });
});

document.querySelector('button#gen-api-key').addEventListener('click', function(e) {
    swal({
        title: "暂未开发！",
        text: "请等待后续版本更新",
        icon: "info"
    });
});