$(document).ready(function(){
    
    $('#treedict-sidebar')
        .sidebar({context:$('#app')});
        //.sidebar('setting', 'transition', 'overlay')
        //.sidebar('toggle');
    
    // render tree
    treeMaker(js_data.tree_structure, {
        id: 'mytree',
        treeParams: js_data.tree_param,
        card_click: function(element){
            alert(element.id);
        }
    });
    
});

