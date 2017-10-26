$(function(){ //DOM Ready

    function navigate(url)
    {
        window.location.href = url;
    }

    $(document).attr("title", "Main panel");
    content_width = (170 + 7) * 2 + 7
    $('.gridster').width(content_width)
    $(".gridster ul").gridster({
        widget_margins: [7, 7],
        widget_base_dimensions: [170, 170],
        avoid_overlapped_widgets: true,
        max_rows: 15,
        max_size_x: 2,
        shift_widgets_up: false
    }).data('gridster').disable();
    
    // Add Widgets

    var gridster = $(".gridster ul").gridster().data('gridster');
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseiframe-default-dmi" id="default-dmi"><div class="outer-frame iframe"><iframe class="scaled-frame" data-bind="attr: {style: frame_style, src: frame_src}" allowfullscreen></iframe></div><div class="outer-image"><img class="img-frame" data-bind="attr: {src: img_src}"></img></div><h1 class="title" data-bind="text: title, attr: {style: title_style}"></h1></div></li>', 2, 1, 1, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-normal" id="default-normal"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 1, 2)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-pre-sleep" id="default-pre-sleep"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 2, 2)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-cozy" id="default-cozy"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 1, 3)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-movie-mode" id="default-movie-mode"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 2, 3)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-away" id="default-away"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 1, 4)
    
    
    
    var widgets = {}
    // Initialize Widgets
    
        widgets["default-dmi"] = new baseiframe("default-dmi", "", "default", {'widget_type': 'baseiframe', 'fields': {'title': '', 'frame_src': '', 'img_src': '', 'frame_style': '""'}, 'icons': [], 'static_css': {'title_style': 'color: #fff;background-color: rgba(0, 0, 0, 0.5);', 'widget_style': 'background-color: #444;'}, 'css': {}, 'static_icons': [], 'refresh': 60, 'img_list': ['http://servlet.dmi.dk/byvejr/servlet/byvejr_dag1?by=8240&mode=long&eps=true']})
    
        widgets["default-normal"] = new baseswitch("default-normal", "", "default", {'widget_type': 'baseswitch', 'entity': 'input_select.context', 'state_active': 'Normal', 'enable': 1, 'post_service_active': {'service': 'script/turn_on', 'entity_id': 'script.normal'}, 'fields': {'title': '', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'mdi-weather-sunny', 'icon_off': 'mdi-weather-sunny'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'icon_on': 'mdi-weather-sunny', 'icon_off': 'mdi-weather-sunny'})
    
        widgets["default-pre-sleep"] = new baseswitch("default-pre-sleep", "", "default", {'widget_type': 'baseswitch', 'entity': 'input_select.context', 'state_active': 'Pre-sleep', 'enable': 1, 'post_service_active': {'service': 'script/turn_on', 'entity_id': 'script.pre_sleep'}, 'fields': {'title': '', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'mdi-weather-night', 'icon_off': 'mdi-weather-night'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'icon_on': 'mdi-weather-night', 'icon_off': 'mdi-weather-night'})
    
        widgets["default-cozy"] = new baseswitch("default-cozy", "", "default", {'widget_type': 'baseswitch', 'entity': 'input_select.context', 'state_active': 'Cozy', 'enable': 1, 'post_service_active': {'service': 'script/turn_on', 'entity_id': 'script.cozy'}, 'fields': {'title': '', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'mdi-coffee', 'icon_off': 'mdi-coffee'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'icon_on': 'mdi-coffee', 'icon_off': 'mdi-coffee'})
    
        widgets["default-movie-mode"] = new baseswitch("default-movie-mode", "", "default", {'widget_type': 'baseswitch', 'entity': 'input_select.context', 'state_active': 'Movie-mode', 'enable': 1, 'post_service_active': {'service': 'script/turn_on', 'entity_id': 'script.movie_mode'}, 'fields': {'title': '', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'mdi-movie', 'icon_off': 'mdi-movie'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'icon_on': 'mdi-movie', 'icon_off': 'mdi-movie'})
    
        widgets["default-away"] = new baseswitch("default-away", "", "default", {'widget_type': 'baseswitch', 'entity': 'input_select.context', 'state_active': 'Away', 'enable': 1, 'post_service_active': {'service': 'script/turn_on', 'entity_id': 'script.away'}, 'fields': {'title': '', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'mdi-lock', 'icon_off': 'mdi-lock'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'icon_on': 'mdi-lock', 'icon_off': 'mdi-lock'})
    

    // Setup click handler to cancel timeout navigations

    $( ".gridster" ).click(function(){
        clearTimeout(myTimeout);
    });

    // Set up timeout

    var myTimeout

    if (location.search != "")
    {
        var query = location.search.substr(1);
        var result = {};
        query.split("&").forEach(function(part) {
        var item = part.split("=");
        result[item[0]] = decodeURIComponent(item[1]);
        });

        if ("timeout" in result && "return" in result)
        {
            url = result.return
            argcount = 0
            for (arg in result)
            {
                if (arg != "timeout" && arg != "return")
                {
                    if (argcount == 0)
                    {
                        url += "?";
                    }
                    else
                    {
                        url += "?";
                    }
                    argcount ++;
                    url += arg + "=" + result[arg]
                }
            }
            myTimeout = setTimeout(function() { navigate(url); }, result.timeout * 1000);
        }
    }

    // Start listening for HA Events
    if (location.protocol == 'https:')
    {
        wsprot = "wss:"
    }
    else
    {
        wsprot = "ws:"
    }
    var stream_url = wsprot + '//' + location.host + '/stream'
    ha_status(stream_url, "Main panel", widgets);

});