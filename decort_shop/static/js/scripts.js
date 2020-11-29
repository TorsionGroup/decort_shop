function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}

// Filter movies
// const forms = document.querySelector('form[name=filter]');
//
// forms.addEventListener('submit', function (e) {
//     // Получаем данные из формы
//     e.preventDefault();
//     let url = this.action;
//     let params = new URLSearchParams(new FormData(this)).toString();
//     ajaxSend(url, params);
// });

function render(data) {
    // Рендер шаблона
    let template = Hogan.compile(html);
    let output = template.render(data);

    const div = document.querySelector('.left-ads-display>.row');
    div.innerHTML = output;
}

let html = '\
{{#movies}}\
    <div class="col-md-4 product-men">\
        <div class="product-shoe-info editContent text-center mt-lg-4">\
            <div class="men-thumb-item">\
                <img src="/media/{{ poster }}" class="img-fluid" alt="">\
            </div>\
            <div class="item-info-product">\
                <h4 class="">\
                    <a href="/{{ url }}" class="editContent">{{ title }}</a>\
                </h4>\
                <div class="product_price">\
                    <div class="grid-price">\
                        <span class="money editContent">{{ tagline }}</span>\
                    </div>\
                </div>\
                <ul class="stars">\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-o" aria-hidden="true"></span></a></li>\
                </ul>\
            </div>\
        </div>\
    </div>\
{{/movies}}'


// Add star rating
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});



	/*----------------------------------------*/
	/*  Torsion's Switch language
 /*----------------------------------------*/

$('#language-list a').on('click', function(event) {
    event.preventDefault();
    var target = $(event.target);
    var url = target.attr('href');
    var language_code = target.data('language-code');
    $.ajax({
        type: 'POST',
        url: url,
        data: {language: language_code},
        headers: {"X-CSRFToken": getCookie('csrftoken')}
    }).done(function(data, textStatus, jqXHR) {
        reload_page();
    });
});


function getCookie(name) {
    var value = '; ' + document.cookie,
        parts = value.split('; ' + name + '=');
    if (parts.length == 2) return parts.pop().split(';').shift();
}

function reload_page() {
    window.location.reload(true);
}

