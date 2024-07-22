axios
  .get("/api/channels/list")
  .then((result) => {
    let data = result.data;
    if (data.success) {
      let table = document.getElementById("channelsTable").tBodies;
      let class_template = [
        "whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0",
        "whitespace-nowrap px-3 py-4 text-sm text-gray-500",
      ];
      data.data.forEach((channel) => {
        let tr = document.createElement("tr");
        let td = document.createElement("td");
        td.classList = class_template[0];
        td.innerText = channel.id;
        tr.appendChild(td);
        td = document.createElement("td");
        td.classList = class_template[1];
        td.innerText = channel.adapter;
        tr.appendChild(td);
        td = document.createElement("td");
        td.classList = class_template[1];
        td.innerText = channel.channel_name;
        tr.appendChild(td);
        td = document.createElement("td");
        td.classList = class_template[1];
        td.innerText = channel.paneladdr;
        tr.appendChild(td);
        td = document.createElement("td");
        td.classList = class_template[1];
        td.innerText = channel.username;
        tr.appendChild(td);
        td = document.createElement("td");
        td.classList = class_template[1];
        td.innerText = channel.instances_count;
        tr.appendChild(td);
        td = document.createElement("td");
        td.classList = class_template[1];
        td.innerHTML = `<button class="text-green-500" onclick="pingChannel(${channel.id})">测试</button>
                        <button class="text-blue-500" onclick="window.location.href='/channels/${channel.id}'">查看</button>
                        <button class="text-red-500" onclick="deleteChannel(${channel.id})">删除</button>`;
        tr.appendChild(td);
        table[0].appendChild(tr);
      });
    } else {
      swal({
        title: "渠道列表获取失败失败",
        text: data.message,
        icon: "error",
      });
    }
  })
  .catch((err) => {
    swal({
      title: "渠道列表获取失败失败",
      text: `网络错误：${err.message}`,
      icon: "error",
    });
    console.log(err);
  });

axios
  .get("/api/adapters/list")
  .then((result) => {
    let data = result.data;
    if (data.success) {
      adpater_list = data.data;
      let select = document.getElementById("adapterSelect");
      select.innerHTML = "";
      adpater_list.forEach((adapter) => {
        let option = document.createElement("option");
        option.value = adapter;
        option.text = adapter;
        select.appendChild(option);
      });
    } else {
      swal({
        title: "接口列表获取失败",
        text: data.message,
        icon: "error",
      });
    }
  })
  .catch((err) => {
    swal({
      title: "接口列表获取失败",
      text: `网络错误：${err.message}`,
      icon: "error",
    });
    console.log(err);
  });

document.querySelector("form").addEventListener("submit", function (e) {
  e.preventDefault();
  let adapter = e.target.querySelector('select[name="adapter"]').value;
  let channel_name = e.target.querySelector('input[name="channel_name"]').value;
  let paneladdr = e.target.querySelector('input[name="paneladdr"]').value;
  let apikey = e.target.querySelector('input[name="apikey"]').value;
  axios
    .post("/api/channels/create", {
      adapter: adapter,
      channel_name: channel_name,
      paneladdr: paneladdr,
      apikey: apikey,
    })
    .then((result) => {
      let data = result.data;
      if (data.success) {
        swal({
          title: "创建成功",
          text: `用户名：${data.data.username}
实例数：${data.data.instances_count}`,
          icon: "success",
          buttons: false,
          closeOnClickOutside: false,
          closeOnEsc: false,
        });
        setTimeout(function () {
          window.location.href = "/channels";
        }, 1000);
      } else {
        swal({
          title: "创建失败",
          text: data.message,
          icon: "error",
        });
      }
    })
    .catch((err) => {
      swal({
        title: "创建失败",
        text: `网络错误：${err.message}`,
        icon: "error",
      });
    });
});
