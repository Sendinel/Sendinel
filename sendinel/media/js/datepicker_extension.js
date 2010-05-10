/*
 * This plugin also affects the jquery-ui datepicker code
 * View line 701 in jquery-ui.js for the function call
 */

if(!Sendinel) { var Sendinel = {}; }

Sendinel.Datepicker = {    
    init : function() {
        var buttons_div = $("<div id='ui-sendinel-datepicker-buttons'></div>");
        
        $("#datepicker").append(buttons_div);
        
        Sendinel.Datepicker.show_month_names();
    },    
    
    adjust_month: function(adjustment) {
        DP_jQuery.datepicker._adjustDate('#datepicker', adjustment, 'M');
        Sendinel.Datepicker.show_month_names();
    },
    
    build_month_link: function(direction, year, month) {
        var adjustments = {'next': 1, 'prev': -1};
        var adjustment = adjustments[direction]
        var dp_link = $(".ui-datepicker-" + direction);
        var month_name = dp_link.attr("title");
        var link;
        
        if(dp_link.hasClass("ui-state-disabled")) {
            link = $('<div>' + month_name + "</div>")
                    .addClass("ui-state-disabled");
        } else {
            link = $('<a>' + month_name + "</a>")
                .addClass("menu-hover")
                .addClass("link")
                .click(function() {
                    Sendinel.Datepicker.adjust_month(adjustment);
                });
        }
        
        link.addClass("ui-sendinel-datepicker-" + direction)
                     .addClass("ui-sendinel-datepicker-button")
                     .addClass("background-grey")
                     .addClass("ui-corner-all");
        return link;
    },
    
    show_month_names : function () {        
        var prev_link = $('.ui-datepicker-prev');
        var next_link = $('.ui-datepicker-next');
    
        if(prev_link.length === 1 && next_link.length === 1) {         
            var buttons_div = $("#ui-sendinel-datepicker-buttons").empty();
            
            var prev_link = Sendinel.Datepicker.build_month_link('prev');
            var next_link = Sendinel.Datepicker.build_month_link('next');
                        
            buttons_div.append(prev_link);
            buttons_div.append(next_link);
            
            $("#datepicker").append(buttons_div);
            
            if(!$("#date").val()) {        
                $(".ui-state-active").removeClass("ui-state-active")
                                     .removeClass("ui-state-hover");
            }
        }
    }
};

$(document).ready(Sendinel.Datepicker.init);