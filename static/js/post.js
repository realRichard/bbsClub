const deletePost = function() {
    let posts = e('.posts')
    bindEvent(posts, 'click', function(event) {
        let target = event.target
        if(target.classList.contains('delete-post')) {
            let p = target.parentElement
            let pId = p.dataset.id
            apiPostDelete(pId, function(r) {
                let s = JSON.parse(r)
                log('deleted p', s)
                if(s !== null) {
                    p.remove()
                }
            })
        }
    })
}


// const csrfToken = function() {
//     var csrftoken = $('meta[name=csrf-token]').attr('content')
//     $.ajaxSetup({
//         beforeSend: function(xhr, settings) {
//             if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
//                 xhr.setRequestHeader("X-CSRFToken", csrftoken)
//             }
//         }
//     })
// }


const __main = function() {
    // csrfToken()
    deletePost()
}


__main()