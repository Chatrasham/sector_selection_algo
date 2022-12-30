$(".close_position_button").click(function (event) {
    event.preventDefault();
    console.log(event);
    console.log($(this));
    let form = $(this).parent('form');
    let id = form.attr('id');
    let csrf = form.getElementById('csrfmiddlewaretoken');
    let qty = form.attr('id');
    let price = form.attr('id');
    let data = {
        id: id, quantity: qty, price: price, csrfmiddlewaretoken: csrf
    };
    $.post('/markets/close-position/', data, function (data, success){
        alert(data);
        alert(success);
    });
});