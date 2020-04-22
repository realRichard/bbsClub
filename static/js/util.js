const log = function() {
    console.log.apply(console, arguments)
}


const e = function(selector) {
    return document.querySelector(selector)
}


const es = function(selector) {
    return document.querySelectorAll(selector)
}


const bindEvent = function(tab, eventName, callback) {
    tab.addEventListener(eventName, callback)
}


const ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // set csrf token
    let csrftoken = $('meta[name=csrf-token]').attr('content')
    r.setRequestHeader("X-CSRFToken", csrftoken)
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}


const apiPostDelete = function(postId, callback) {
    let path = '/post/delete?id=' + postId
    ajax('POST', path, '', callback)
}




