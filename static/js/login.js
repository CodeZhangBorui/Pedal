document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    let username = e.target.querySelector('input[name="username"]').value;
    let password = e.target.querySelector('input[name="password"]').value;
    axios.post('/api/clients/login', {
        'username': username,
        'password': password
    }).then((result) => {
        let data = result.data;
        if (data.success) {
            swal({
                title: "登录成功",
                text: "\n",
                icon: "success",
                buttons: false,
                closeOnClickOutside: false,
                closeOnEsc: false
            });
            setTimeout(function() {
                window.location.href = '/';
            }, 1000);
        } else {
            swal({
                title: "登录失败",
                text: data.message,
                icon: "error",
            
            });
        }
    }).catch((error) => {
        swal({
            title: "登录失败",
            text: `网络错误：${error.message}`,
            icon: "error",
        });
        console.log(error)
    });
});