$(document).on('click', '.compare-button', function () {
    var button = $(this);
    var modelSlug = button.data('model-name');
    $.ajax({
        url: '/comparison/add/' + modelSlug,
        method: 'GET',
        success: function (response) {
            if (response.success) {
                button.text('Добавлено');
                button.prop('disabled', true);
            } else {
            }
        }
    });
});



