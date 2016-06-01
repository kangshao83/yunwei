

/** 侧边栏搜索 */
$(".icon-sousuo").click(function(){
	$(".sliderMenu-list li").hide()
	                        .filter(":contains('"+($('.search-area .search').val())+"')").show()
							.trigger("click"); // 搜索后默认打开当前菜单对应的数据
});

/** 卡片 */
/*$(".main").on({
	"mouseover": function(){
		$(this).is(".card-disabled") || $(this).find(".card-cell").stop(true,false).animate({"bottom": 0+"px"},300);
	},
	"mouseout": function(){
		$(this).find(".card-cell").stop(true,false).animate({"bottom": -42+"px"},200);
	}
},".card-content");*/


/** 关闭滑动面板*/
$(".panel .close").click(function(){
	$(".slider-panel").fadeOut("1200").css("right",-500+"px");
	$(".overlay").hide();  
});
	
/** 打开模态框 */
$(".userMenu li:eq(1)").click(function(){
	$(".overlay,.modal-dialog-box").show();
	$(".modal-footer .btn-sure").attr("bid","logout");   // 给弹框确定按钮加标识
});
	
/** 关闭模态框 */
$(".close, .btn-cancel").click(function(e){
	$(".overlay,.modal-dialog-box").hide();
});

// 单击确定按钮关闭模态框
$(".btn-sure[bid='logout']").click(function(){
	$(".overlay,.modal-dialog-box").hide();
	// todo 单击确定后的业务操作
});
	
/*$(".modal-dialog-box .overlay").click(function(e){
	if($(e.target).is(".overlay")){
	    $(".overlay,.modal-dialog-box").hide();
	 }
});*/

