let on_alias_like = function(a_id){
    t = $("#alias_num_"+a_id.toString()).text();
    $("#alias_num_"+a_id.toString()).text(parseInt(t)+1);
    $.get('/a/l/'+a_id.toString());
};

let on_alias_create = function(c_code){
    name = $('#alias_create_input_'+c_code).val();
    alert(name);
    $.get('/a/c/'+c_code+'/'+name);
};

let on_prereq_like = function(a_id){
    t = $("#prereq_num_"+a_id.toString()).text();
    $("#prereq_num_"+a_id.toString()).text(parseInt(t)+1);
    $.get('/p/l/'+a_id.toString());
};

let on_prereq_create = function(c_code){
    name = $('#prereq_create_input_'+c_code).val();
    alert(name);
    $.get('/p/c/'+name +'/'+c_code);
};

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
        

        
        if(the_course){
            alias_table += `
                <p>
                    ${the_course.description}
                </p>
                <div class="ui horizontal list">
            `;
    
            $.each(the_course.best_aliases, function(index, item){
                //li.push([item[4], item[3]])
                alias_table += `
                    <div class="item">
                        <div>
                            <div id="alias_${item[4]}" class="ui labeled button">
                                <div class="ui button" onclick="on_alias_like(${item[4]})">
                                    <i class="tags icon"></i> ${item[0]} Like
                                </div>
                                <a id="alias_num_${item[4]}" class="ui basic left pointing label">
                                    ${item[1]}
                                </a>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            alias_table += `
                <div class="item">
                <div class="ui right labeled left icon input">
                    <i class="tags icon"></i>
                    <input id="alias_create_input_${item_code}" type="text" placeholder="Enter new alias..." ></input>
                    
                    <a class="ui tag label" onclick="on_alias_create('${item_code}')">
                        Add alias
                    </a>
                    
                    </div>
    </div>
    <hr></hr>
    
    `;
            $.each(the_course.best_prerequisites, function(index, item){
                //li.push([item[4], item[3]])
                alias_table += `
                    <div class="item">
                        <div>
                            <div id="prereq_${item[4]}" class="ui labeled button">
                                <div class="ui button" onclick="on_prereq_like(${item[4]})">
                                    <i class="tags icon"></i> ${item[0]} Like
                                </div>
                                <a id="prereq_num_${item[4]}" class="ui basic left pointing label">
                                    ${item[1]}
                                </a>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            alias_table += `
                <div class="item">
                <div class="ui right labeled left icon input">
                    <i class="tags icon"></i>
                    <input id="prereq_create_input_${item_code}" type="text" placeholder="Enter new prerequisite..."></input>
                    
                    <a class="ui tag label" onclick="on_prereq_create('${item_code}')">
                        Add prerequisite
                    </a>
                    
                    </div>
    </div>
    <hr></hr>
    
    `;
    
        } else {
            alias_table += $(item).text()+' <div>';
        }
        
        
        $(item).append(
            `<div id="treedict_modal_${ item_code }" class="ui modal">
                <i class="close icon"></i>
                <div class="header">
                    ${item_code}
                </div>
                <div class="scrolling content">

                        ${alias_table}
                    </div>
                </div>
            </div>`
        );
        

        
        $(item).click(function(){
            $("#treedict_modal_"+item_code).modal('show');
            redraw_svg();
        });
    });

    
});

