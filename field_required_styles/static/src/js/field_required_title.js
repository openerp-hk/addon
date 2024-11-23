$(document).ready(function () {
    $('.o_wrap_field').each(function () {
        let $input = $(this).find('.o_required_modifier input')
        let $label = $(this).find('label')
        if ($input.length > 0) {
            var initialValue = $input.val().trim();
            if (initialValue === '') {
                $input.addClass('field_required_input');
                debugger
                if($label.length >0){
                    $label.addClass('field_required_label')
                }

            } else {
                $input.removeClass('field_required_input');
                if($label.length >0){
                    $label.removeClass('field_required_label')
                }
            }
        }

    })

});