$(document).on('click', '.favorites-button', function () {
    var button = $(this);
    var modelSlug = button.data('model-name');
    var categoryName = button.data('asdf');
    $.ajax({
        url: '/favorites/add/' + categoryName + '/' + modelSlug,
        method: 'GET',
        success: function (response) {
            if (response.success) {
                button.text('В избранном');
                button.prop('disabled', true);
            } else {
            }
        }
    });
});



