$(document).on("click", ".delete-transl.no_ajax", (e) => {
    $(e.target).parent().parent().parent().remove()
})


$(document).on("click", ".delete-transl.with_ajax", (e) => {
    let result = confirm("Хотите удалить?")

    if(!result) {
        return;
    } 

    const id = $(e.target).attr("data-id");
    let data = {}
    data["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: `/admin/translations/${id}/delete`,
        type: "POST",
        data: data,
        success: () => {
            $(e.target).parent().parent().parent().remove()

            $('.messages').append(
            `
                <div class="alert alert-success notifs" role="alert">
                    Объект удален
                </div>
            `
            )

            setTimeout(() => {
                $('.notifs').remove()
            }, 2000)
        },
        error: () => {

            $('.messages').append(
                `
                <div class="alert alert-error notifs" role="alert">
                    Ошибка
                </div>
            `
            )

            setTimeout(() => {
                $('.notifs').remove()
            }, 2000)

        }
    })

})


async function translate(text, lang_from, lang_to) {
    let url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${lang_from}&tl=${lang_to}&dt=t&q=${text}`

    let response = await fetch(url);
    let tranlation = ""

    if (response.ok) { 
        let json = await response.json();

        tranlation = json[0][0][0]
    }

    return tranlation
}



$(document).on("click", "#translate_btn", (e) => {
    $("#translations-list > tr").each((i, e) => {
        let default_value = $(e).find(".value_td").first().find("input").val()
        let default_lang = $(e).find(".value_td").first().attr("data-lang")

        if(default_value != "") {
            $(e).find(".value_td").each(async (l, td) => {
                if(l != 0) {
                    let lang = $(td).attr("data-lang")
                    let translation = await translate(default_value, default_lang, lang)
                    $(td).find("input").val(translation)
                }
            })
        }
    })
})