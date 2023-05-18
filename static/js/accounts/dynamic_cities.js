
// Carga las opciones de ciudad de forma dinámica según el departamento que seleccione el usuario.
$(document).ready(function() {
    $('#region').change(function() {
        let regionId = $(this).val();
        if (regionId) {
            $.ajax({
                url: '/region/' + regionId + '/cities/',
                type: 'get',
                dataType: 'json',
                success: function(cities) {
                    let $citySelect = $('#city');
                    $citySelect.empty();
                    $citySelect.append('<option value="">Seleccione una ciudad...</option>');
                    $.each(cities, function(index, city) {
                        $citySelect.append('<option value="' + city.id + '">' + city.name + '</option>');
                    });
                },
                error: function(xhr, status, error) {
                    console.log(xhr.responseText);
                }
            });
        }
    });
});