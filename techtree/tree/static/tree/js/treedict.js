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
        $(item).click(function(){
            $(item).addClass('clicked_card');
            var innercard = $("#"+ item.id + " > .card_inner");
            if( innercard.css('display') == 'none' ){
                innercard.css('display', '');
            } else {
                innercard.css('display', 'none');
            }
            
            redraw_svg();
        });
    });
    
});

