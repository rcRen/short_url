$(document).ready(function () {
    $("#show_table").hide()

    $("#create_form").submit(function (event) {
        event.preventDefault();
        let formData = {
            path: $('#input_path').val(),
            country_code: $('#input_country_code').val(),
            utm_source: $('#input_utm_source').val(),
            utm_campaign: $('#input_utm_campaign').val(),
            utm_medium: $('#input_utm_medium').val(),
            utm_content: $('#input_utm_content').val(),
            utm_term: $('#input_utm_term').val()
        };

        $.ajax({
            type: 'POST',
            url: '/api/create',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            complete: function ({ status, responseJSON }) {
                if (status == 201) {
                    showData(responseJSON)
                }
                if (status == 422) {
                    showData(responseJSON)
                    $(".message").text(`* ${responseJSON.message}`)
                }
                if (status == 400) {
                    $(".message-error").text(`* ${responseJSON.message}`)
                }

            }
        })
    })

    const showData = (data) => {
        if (data) $("#show_table").show()
        const { short_code, country_code, campaign_params } = data;
        $("#short_code").find("a").text(short_code)
        $("#country_code").text(country_code)
        let domain;
        switch (data.country_code) {
            case "ca":
                domain = "https://www.thenewsbucket.com"
                break;
            case "fr":
                domain = "https://fr.thenewsbucket.com"
                break;
            case "jp":
                domain = "https://.thenewsbucket.com"
                break;
        }

        $("#short_code").find("a").attr("href", `${domain}/${campaign_params}`)

    }
})
