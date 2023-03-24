$(document).on('click', '.compare-button', function () {
    var button = $(this);
    var modelSlug = button.data('model-name');
    var categoryName = button.data('asdf');
    $.ajax({
        url: '/comparison/add/' + categoryName + '/' + modelSlug,
        method: 'GET',
        success: function (response) {
            if (response.success) {
                button.text('В сравнении');
                button.prop('disabled', true);
            } else {
            }
        }
    });
});



