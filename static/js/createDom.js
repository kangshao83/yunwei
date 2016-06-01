$(function(){
	/** 菜单树 */

	// todo 初始化加载菜单树
	$.ajax({  
        type:"get",  
        url:"http://127.0.0.1:8000/api/v1/groups/",
        dataType: "json", 	
        success: function(data){
            var data = data.objects



		  // 隐藏loading
		  $(".sliderMenu-area .loading").hide();
          loadMenu(data);
        },
		error: function(){
		  alert("请求失败！");		  
		}  
    });  			
	
	// 创建菜单
	function loadMenu(menuArr){
        console.log(menuArr)
	  var li = "";
	  for(var i=0, len=menuArr.length; i<len; i+=1){
	    if(menuArr[i].isSelected){
	      li += '<li groupname="'+menuArr[i].id+'" id="'+menuArr[i].id+'" class="menu-item menu-selected">'+menuArr[i].content+'</li>';
		}else{
		  li += '<li id="'+menuArr[i].id+'" class="menu-item" start="'+menuArr[i].actionstart+'" stop="'+menuArr[i].actionstop+'" restart="'+menuArr[i].actionrestart+'" deploy="'+menuArr[i].actiondeploy+'" >'+menuArr[i].groupname+'</li>';
		}
	  }
	  $(".sliderMenu-list").append(li);
	  
	  // 页面加载后，展开默认选中的菜单和其对应的内容
		var menu_li = $(".sliderMenu-list li.menu-selected");
		menu_li.length && menu_li.trigger("click");
	}
	
	// 分页：当前页为第一页
    var curPage = 1; 
	// 单击菜单
	$(".sliderMenu-list").on("click","li",function(){
	  // 1、 改变按钮状态
	  $(this).addClass("menu-selected").siblings().removeClass("menu-selected");
	  // 2、发送ajax请求，根据id和当前页查询菜单对应的主体内容
	  //var id =  $(this).attr('id');
	  var groupname =  $(this).attr('groupname');
        //console.log(groupname)
      var menuName = $(this).text();  


	  $.ajax({  
	    url:"/get_host_list/",
        type:"post",
        data: {"groupname": menuName},
        dataType: "json",
        beforeSend: function(){
			$(".main").append('<div class="loading"><img src="/static/images/loading.gif" width="24px"></div>');
		},		
        success: function(data){

        console.log(data)

		   // 生成主体数据
		   loadMain_html(menuName,data);
           page.init({
			   curPage: 1,                            // 当前页
			   pageSize: data.page.pageSize,          // 每页展示
			   totalCount: data.page.totalCount,      // 总记录数
			   goToPage: function(curPage){
				 // todo 跳转页面代码
				 loadData(curPage);
			  }
	       });      			
        },
		error: function(){
		  alert("请求失败！");
		}  
    }); 
	  
	});
	
	// 创建主内容区域
    function loadMain_html(menuname,data) {
        $(".main").empty();
	   var main_html = '<div class="breadcrumb-box"><ul class="breadcrumb"><li class="active">'+menuname+'</li></ul> </div>'+
		   				'<div class="wrap">'+
					   '<div class="card clearfix">';

			//生成card
		main_html += createCard(data.data);

		//生成分页
		main_html += '</div><div class="pagination-box"> <ul class="pagination"></ul></div></div>';
		$(".main").append(main_html);
    }


	
	
	// 单击分页请求下一页数据
	function loadData(current){
	    // todo: 根据current获得发送ajax请求数据
		$.get("../js/card.json",{current: current},
		function(data){
		    $(".card").empty().append(createCard(data));
		});
	}
	
	
	

	//生成卡片列表
	function createCard(cards) {
		var cardstr = '';
		for(var i=0,len=cards.length; i<len; i++)
        {

			var card = cards[i];
			cardstr += '<div class="card-content">' +
				'<div class="card-body"><p>'+card.hostip+'</p></div>' +
				'<div class="card-cell" ip="' + card.hostip + '">' +
				'<a href="javascript:;" attr="' + card.actionstop + '" class="btn-card">停止</a> | ' +
				'<a href="javascript:;" attr="' + card.actionstart + '" class="btn-card">启动</a> | ' +
				'<a href="javascript:;" attr="' + card.actionrestart + '" class="btn-card">重启</a> | ' +
				'<a href="javascript:;" attr="' + card.actiondeploy + '" class="btn-card">发布</a>' +
				'</div>' +
				'</div>' ;
		}
		return cardstr;
	}

});