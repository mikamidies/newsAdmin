let url = '/admin/translation/edit'

$(document).on('click', '.tranlation-update-btn', (e) => {
    let id = $(e.target).attr("data-id")

    $.ajax({
        url: url,
        type: "GET",
        datatype: 'json',
        data: {'id': id},
        success: (data) => {
            console.log(data.value)
            let form = $('#translation-update-form')
            $(form).find("#transl_title_error").html('')
            $(form).find('#transl_key_error').html('')
            $('#exampleModalLabel').html(`${data.group}.${data.key}`)
            $(form).find("[name='id']").val(data.id)
            $(form).find('#group-key-name').html(data.group + '.')
            $(form).find("[name='key']").val(data.key)
            for(let key in data.value) {
                $(form).find(`[name='value#${key}']`).val(data.value[String(key)])
            }
        }, 
        error: () => {
            console.log('error')
        }


    })

})


$(document).on('submit', '#translation-update-form', (e) => {
    e.preventDefault()
    let data = $(e.target).serialize()

    $.ajax({
        url: url,
        data: data,
        type: 'POST',
        success: (data) => {
            console.log(data)
            if ('key_error' in data) {
                $('#transl_key_error').css('display', 'block')
                $('#transl_key_error').html(data['key_error'])
                return;
            } else if ('lng_error' in data) {
                $('#transl_lng_error').css('display', 'block')
                $('#transl_lng_error').html(data['lng_error'])
                return;
            }
            console.log('success')
            let itemBlock = $(`tr[data-id=${data.id}]`)

            $(itemBlock).find('.transl-key').html(`${data.group}.${data.key}`)

            for(let key in data.value) {
                $(itemBlock).find(`span[data-lang=${key}]`).html(data.value[String(key)])
            }

            $('#exampleModal').modal("hide")
        },
        error: () => {

        }
    })

})