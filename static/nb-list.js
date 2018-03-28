(function (jq) {
    var CREATE_SEARCH_CONDITION=true;
    var GLOBAL_DICT={};
    String.prototype.Format=function (arg) {
    var temp=this.replace(/\{(\w+)\}/g,function(k,kk){
    return arg[kk];
    });
    return temp};
    
    function getSearchCondition() {
        var condition={};
        $('.search-list').find('input[type="text"],select').each(function () {
                   // console.log($(this)[0]) ;//获取所有得搜索条件
                    var name=$(this).attr('name');
                    var value=$(this).val();
                    if(value){
                        if(condition[name]){
                            condition[name].push(value)
                        }else{
                            condition[name]=[value];
                        }
                    }
                });
        return condition;
    }
    function initial(url){
        //执行一个函数，获取当前搜索条件
        var searchConfition=getSearchCondition();
        console.log(searchConfition);
        $.ajax({
            url: url,
            type: 'GET',
            data:{condition:JSON.stringify(searchConfition)},
            dataType:'JSON',
            success:function(arg){
                $.each(arg.global_dict,function (k,v) {
                    GLOBAL_DICT[k]=v;
                });
                initTableHeader(arg.table_config);
                initTableBody(arg.server_list,arg.table_config);
                initSearch(arg.search_config);
            }
        })
    }
    //初始化搜索条件
    function initSearch(searchConfig) {
        if(searchConfig && CREATE_SEARCH_CONDITION){
            // console.log(searchConfig)
            CREATE_SEARCH_CONDITION=false; //关闭初始化
            //找到searchArea ul 筛选条件
            $.each(searchConfig,function (k,v) {
                // if(k==0){
                //     $('#searchDefault').text(v.text)
                // }
                var li=document.createElement(('li'));
                $(li).attr('search_type',v.search_type);
                $(li).attr('name',v.name);
                if(v.search_type=='select'){
                     $(li).attr('global_name',v.global_name);
                }
                var a=document.createElement('a');
                a.innerHTML=v.text;
                $(li).append(a);
                $('.searchArea ul').append(li)
            });
            //初始化默认搜索条件
            //searchConfig[0] 初始化
            //初始化默认选中的值

            $('.search-item .searchDefault').text(searchConfig[0].text);
            if(searchConfig[0].search_type=='select'){
                var sel=document.createElement('select');
                $(sel).attr('class','form-control');
                $.each(GLOBAL_DICT[searchConfig[0].global_name],function (k,v) {
                    var op=document.createElement('option');
                    $(op).text(v[1]);
                    $(op).val(v[0]);
                    $(sel).append(op)
                });
                $('.input-group').append(sel);
            }else {
                var inp=document.createElement('input');
                $(inp).attr('name',searchConfig[0].name);
                $(inp).attr('type','text');
                $(inp).attr('class','form-control');
                $('.input-group').append(inp);
            }
        }

    }

    function initTableHeader(tableConfig){
        $('#tbHead').empty();
        var tr=document.createElement('tr');

        $.each(tableConfig,function(k,v){
        if(v.display){
            var tag = document.createElement('th');
            tag.innerHTML = v.title;
          $(tr).append(tag);
        }
    });
        $('#tbHead').append(tr);
}

    function initTableBody(serverList,tableConfig){
        $("#tbBody").empty();
        $.each(serverList,function(k,row){
            var tr = document.createElement('tr');
            tr.setAttribute('nid',row.id);
            $.each(tableConfig,function(kk,rrow){
                if(rrow.display){
                var td = document.createElement('td');
                /*
                if(rrow['q']){
                    td.innerHTML = row[rrow.q];
                }else{
                    td.innerHTML = rrow.text;
                }*/

                /*在td标签中添加内容*/
                var newKwargs={};
                $.each(rrow.text.kwargs,function (kkk,vvv) {
                    var av=vvv;
                    if(vvv.substring(0,2)=='@@'){
                        var global_dict_key=vvv.substring(2,vvv.length);
                        var nid=row[rrow.q];
                        $.each(GLOBAL_DICT[global_dict_key],function (gk,gv) {
                            if(gv[0] == nid){
                                av=gv[1];
                            }
                        })

                    }
                    else if(vvv[0]=='@'){
                        av=row[vvv.substring(1,vvv.length)]
                    }
                    newKwargs[kkk]=av;
                });
                var newText=rrow.text.tpl.Format(newKwargs);
                td.innerHTML = newText;
                /*在td中添加属性*/
                $.each(rrow.attrs,function (atkey,atval) {
                    if(atval[0]=='@'){
                        td.setAttribute(atkey,row[atval.substring(1,atval.length)])
                    }else {
                        td.setAttribute(atkey,atval)
                    }

                });

                $(tr).append(td);}
            });
            $('#tbBody').append(tr);

        });
    }
    function trIntoEdit($tr) {
            $tr.find('td[edit-enable="true"]').each(function () {
                 /*循环的每个td*/
                var editType=$(this).attr('edit-type');
                if(editType=='select'){
                    //找到数据源
                    var deviceTypeChoices=GLOBAL_DICT[$(this).attr('global_key')]
                    //生成下拉框
                    var selectTag=document.createElement('select');
                    var origin=$(this).attr('origin');
                    $.each(deviceTypeChoices,function (k,v) {
                        var option=document.createElement('option');
                        $(option).text(v[1]);
                        $(option).val(v[0]);
                        //显示默认选中值*/
                        if(v[0]==origin){
                            $(option).prop('selected',true)
                        }
                        $(selectTag).append(option);

                    });
                    $(this).html(selectTag)


                }else {

                    //获取原来td中的文本内容
                    var v1=$(this).text();
                    //创建input标签，并且内部设置值
                    var inp=document.createElement('input');
                    $(inp).val(v1);
                    $(this).html(inp); /*将内容替换成input的*/

                }

            })
        }
    function trOutEdit($tr) {
        $tr.find('td[edit-enable="true"]').each(function () {
            var editType=$(this).attr('edit-type');
            if(editType == 'select'){
                var option=$(this).find('select')[0].selectedOptions ;//变成dom并获取选中的option
                $(this).attr('new_origin',$(option).val());  //选中的id
                $(this).html($(option).text())
            }
            else {
                var inpuVal=$(this).find('input').val();
                $(this).html(inpuVal)  /*输入的值马上显示出来*/
            }

        });
    }
    
    jq.extend({
        xx:function (url) {
            initial(url);

            //编辑.checkbox绑定事件
            /*由于页面标签是后面生成的。所以要以委托的方式绑定函数。直接绑定是绑不上的*/
            $("#tbBody").on('click',':checkbox',function () {
                if ($("#inOutEditMode").hasClass('btn-warning')){
                    var $tr=$(this).parent().parent();
                    if($(this).prop('checked')){
                        /*进入编辑模式*/
                        trIntoEdit($tr);
                    }else{
                        /*退出编辑模式*/
                        trOutEdit($tr)
                    }
                }
            });


            //按钮绑定事件
             $("#checkAll").click(function () {
                //选中每一个并且进入编辑模式
                if ($("#inOutEditMode").hasClass('btn-warning')){
                    $("#tbBody").find(":checkbox").each(function () {
                    if(!$(this).prop('checked')){
                        var $tr=$(this).parent().parent();
                        trIntoEdit($tr);
                        $(this).prop('checked',true)
                    }
                })
                }else {
                    $("#tbBody").find(":checkbox").prop('checked',true);
                }


            });

             $("#checkReverse").click(function () {
                 if ($("#inOutEditMode").hasClass('btn-warning')){
                     $("#tbBody").find(":checkbox").each(function () {
                         var $tr=$(this).parent().parent();
                         if($(this).prop('checked')){
                                trOutEdit($tr);
                                $(this).prop('checked',false)
                            }else {
                                trIntoEdit($tr);
                                $(this).prop('checked',true)
                            }
                      })
                 }else {
                    $("#tbBody").find(":checkbox").each(function () {
                         var $tr=$(this).parent().parent();
                         if($(this).prop('checked')){
                                $(this).prop('checked',false)
                            }else {
                                $(this).prop('checked',true)
                            }
                      })
                 }
             });

             $("#checkCancel").click(function () {
                 if ($("#inOutEditMode").hasClass('btn-warning')){
                  $("#tbBody").find(":checkbox").each(function () {
                    if($(this).prop('checked')){
                            var $tr=$(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked',false)
                        }
                  })
                 }else {
                      $("#tbBody").find(":checkbox").prop('checked',false);
                 }
             });

             $("#inOutEditMode").click(function () {
                 if ($(this).hasClass('btn-warning')){
                     //退出编辑模式
                     $(this).removeClass('btn-warning');
                     $(this).text('进入编辑模式');
                     $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        }
                    })
                 }else{
                     //进入编辑模式
                     $(this).addClass('btn-warning');
                     $(this).text('退出编辑模式');
                     $('#tbBody').find(':checkbox').each(function(){
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                        }
                    })
                 }
             });

             $("#multiDel").click(function(){
                  //已经被选中的checkbox
                  var idList=[];
                  $("#tbBody").find(':checked').each(function () {
                      var v=$(this).val();
                      idList.push(v);
                  });
                  $.ajax({
                      url:url,
                      type:'delete',
                      data:JSON.stringify(idList),
                      success:function (arg) {
                          console.log(arg)
                      }
                  })
              });

             $("#refresh").click(function () {
                 initial(url);
             });
            
             $("#save").click(function () {
                 //退出编辑模式
                 if($("#inOutEditMode").hasClass("btn-warning")){
                    $("#tbBody").find(":checkbox").each(function () {
                         if($(this).prop('checked')){
                                var $tr=$(this).parent().parent();
                                trOutEdit($tr);
                         }
                    })
                 }
                 //获取用户修改过的数据，
                 var all_list=[];
                 $("#tbBody").children().each(function () {
                     var $tr=$(this);
                     var nid=$tr.attr('nid');
                     var row_dict={};
                     var flag=false;
                     $tr.children().each(function () {
                         if($(this).attr('edit-enable')) {
                            if($(this).attr('edit-type')=='select') {
                                var newData=$(this).attr('new_origin');
                                var oldData=$(this).attr('origin');
                                if (newData){
                                     if(newData!=oldData){
                                         var name=$(this).attr('name');
                                         row_dict[name]=newData;
                                         flag=true;
                                     }
                                 }
                            }else{
                                 var newData=$(this).text();
                                 var oldData=$(this).attr('origin');
                                 if (newData){
                                     if(newData!=oldData){
                                         var name=$(this).attr('name');
                                         row_dict[name]=newData;
                                         flag=true;
                                     }
                                 }

                             }
                         }
                     });
                     if(flag){
                         row_dict['id']=nid;
                     }
                     all_list.push(row_dict)

                 });
                 //通过ajax提交到后台
                 console.log(all_list);
                 $.ajax({
                     url:url,
                     type:'PUT',
                     data:JSON.stringify(all_list),
                     success:function (arg) {
                         console.log(arg)
                     }
                 })
             });

             //点击li执行函数
            $('.search-list ').on('click','li',function () {
                var wenben=$(this).text();
                var search_type=$(this).attr('search_type');
                var name=$(this).attr('name');
                var global_name=$(this).attr('global_name');

                //把显示的文本进行替换
                $(this).parent().prev().find('.searchDefault').text(wenben);
                if(search_type=='select'){
                    var sel=document.createElement('select');
                    $.each(GLOBAL_DICT[global_name],function (k,v) {
                        var op=document.createElement('option');
                        $(op).text(v[1]);
                        $(op).val(v[0]);
                        $(sel).append(op);
                    });
                    $(sel).attr('class','form-control');
                    $(sel).attr('name',name);
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(sel)
                }else {
                    var inp=document.createElement('input');
                    $(inp).attr('class','form-control');
                    $(inp).attr('name',name);
                    $(inp).attr('type','text');
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(inp);
                }
            });

            $(".search-list").on('click','.add-search-condition',function () {
                //复制一份新的搜索项
                var newSearchItem=$(this).parent().parent().clone();
                $(newSearchItem).find('.add-search-condition span').removeClass('glyphicon-plus').addClass('glyphicon-minus');
                $(newSearchItem).find('.add-search-condition').addClass('del-search-condition').removeClass('add-search-condition')
                $(".search-list").append(newSearchItem)

            });
            $('.search-list').on('click','.del-search-condition',function () {
                $(this).parent().parent().remove();
            });
            $('#doSearch').click(function () {
                // var condition={};
                // $('.search-list').find('input[type="text"],select').each(function () {
                //     console.log($(this)[0]) ;//获取所有得搜索条件
                //     var name=$(this).attr('name');
                //     var value=$(this).val();
                //     if(condition[name]){
                //         condition[name].push(value)
                //     }else{
                //         condition[name]=[value];
                //     }
                //
                //
                //
                //
                // });
                // console.log(condition)
                initial(url);
            })

            




        }
    })
    
   
        })(jQuery);
