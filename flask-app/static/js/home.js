// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/reports',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
                console.log(data);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $employeeName = $('#employeeName'),
        $annual_leave = $('#annual_leave'),
        $sick_leave = $('#sick_leave'),
        $hours_worked = $('#hours_worked'),
        $hours_counted = $('#hours_counted'),
        $hours_under_over = $('#under_over'),
        $shifts_worked = $('#shifts_worked'),
        $shifts_counted = $('#shifts_counted'),
        $shifts_wfh = $('#shifts_wfh');
        ;

    // return the API
    return {
        reset: function() {
            $annual_leave.val('');
            $employeeName.val('').focus()
        },
        update_editor: function(employeeName, annual_leave) {
            $annual_leave.val(annual_leave);
            $employeeName.val(employeeName).focus();
        },
        build_table: function(reports) {
            let rows = ''

            // clear the table
            $('.reports table > tbody').empty();

            if (reports) {
                for (let i=0, l=reports.length; i < l; i++) {
                    rows += `<tr><td class="employeeName">${reports[i].employeeName}</td><td class="annual_leave">${reports[i].annual_leave['January']}</td><td class="sick_leave">${reports[i].sick_leave['January']}</td><td class="hours_worked">${reports[i].hours_worked['January']}</td><td class="hours_counted">${reports[i].hours_counted['January']}</td><td class="under_over">${reports[i].hours_counted['under/over']}</td><td class="shifts_worked">${reports[i].shifts_worked['January']}</td><td class="shifts_counted">${reports[i].shifts_counted['January']}</td><td class="shifts_wfh">${reports[i].shifts_wfh['January']}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $employeeName = $('#employeeName'),
        $annual_leave = $('#annual_leave'),
        $sick_leave = $('#sick_leave'),
        $hours_worked = $('#hours_worked'),
        $hours_counted = $('#hours_counted'),
        $hours_under_over = $('#under_over'),
        $shifts_worked = $('#shifts_worked'),
        $shifts_counted = $('#shifts_counted'),
        $shifts_wfh = $('#shifts_wfh');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(employeeName, annual_leave) {
        return employeeName !== "" && annual_leave !== "";
    }

    // $('table > tbody').on('dblclick', 'tr', function(e) {
    //     let $target = $(e.target),
    //         employeeName,
    //         annual_leave;

    //     employeeName = $target
    //         .parent()
    //         .find('td.employeeName')
    //         .text();

    //     annual_leave = $target
    //         .parent()
    //         .find('td.annual_leave')
    //         .text();

    //     view.update_editor(employeeName, annual_leave);
    // });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
