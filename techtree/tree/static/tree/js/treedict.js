$(document).ready(function(){
    
    $('#treedict-sidebar')
        .sidebar({context:$('#app')});
        //.sidebar('setting', 'transition', 'overlay')
        //.sidebar('toggle');
    
    // render tree
    function makeTree(){
        treeMaker(js_data.tree_structure, {
            id: 'mytree',
            treeParams: js_data.tree_param,
            card_click: function(){}
        });
    }
    makeTree();
    
    function redraw_svg(){
        window.onresize();
    }
    
    $('.tree__container__step__card p').each( function(index, item) {
        const item_code = item.id.toString().split("_")[1];
        $(item).append(
            '<div id="treedict_modal_' + item_code + '" class="ui modal">' +
                '<i class="close icon"></i>' +
                '<div class="header">' +
                    item_code +
                '</div>' +
                '<div class="scrolling content">' +
                    '<p>Data about aliases and prerequisites</p>' +
                '</div>' +
            '</div>'
        );
        
        $(item).click(function(){
            $("#treedict_modal_"+item_code).modal('show');
            redraw_svg();
        });
    });
    
});

