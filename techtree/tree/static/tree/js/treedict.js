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
        
        let alias_table = "";
        let the_course = null;
        let li = [];
        
        $.each(js_data.course_dataset, function(index, item){
            if(item.course_code == item_code){
                the_course = item;
            }
        });
        
        alias_table += ``;
        
        if(the_course){
            $.each(the_course.best_aliases, function(index, item){
                li.push([item[4], item[3]])
                alias_table += `
                    <div class="item">
                        <a id="alias_header_${item[4]}" class="header">${item[0]} ++${item[1]} </a>
                        <div class="description">
                            made by ${item[2]}
                            <div id="alias_${item[4]}" class="ui toggle checkbox">
                                <input type="checkbox" name="${item[4]}"></input>
                                <label>Like</label>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        
        $(item).append(
            `<div id="treedict_modal_${ item_code }" class="ui modal">
                <i class="close icon"></i>
                <div class="header">
                    ${item_code}
                </div>
                <div class="scrolling content">
                    <div class="ui relaxed divided list">
                        ${alias_table}
                    </div>
                </div>
            </div>`
        );
        
        $.each(li, function(index, item){
            if(item[1]){
                $('#alias_'+item[0].toString()).checkbox('check');
            }
            $('#alias_'+item[0].toString()).checkbox({
                onChecked: function() {
                    $.get('/alias/toggle/'+item_code+"/"+item[0]+'/0').done(function(jqXHR){
                        window.location.href = window.location.href;
                    }).fail(function(jqXHR){
                        alert('로그인이 필요합니다!');
                        $('#alias_'+item[0].toString()).checkbox("set unchecked");
                    });
                },
                onUnchecked: function() {
                    $.get('/alias/toggle/'+item_code+"/"+item[0]+'/1');
                }
            });
        });
        
        $(item).click(function(){
            $("#treedict_modal_"+item_code).modal('show');
            redraw_svg();
        });
    });
    
});

