
	/** 分页 */		
	var page = {
		init: function(options) {
            this.options = options;
            this.total = options.totalCount;
            this.pageSize = options.pageSize;
            this.current = options.curPage;
            this.totalPages = Math.ceil(this.total / this.pageSize);
			// 获得分页方式
			this.display = [2,3,2];
			// 计算显示最大分页个数
			this._maxPages = this.display[0]+this.display[1]+this.display[2];
            this.totalPages === 1 ? $('.pagination').hide() : this.changePaginationView();
			// 初始化创建分页
			this.createPage(this.getDisplay(this.current),this.current);
			// 设置分页状态
			this.changePaginationView();
			// 初始事件
            this.initEvent();
        },
		// 创建分页
		createPage: function(display,curPage){
		  $(".pagination-box .pagination").empty();
          $(".pagination-box .pagination").append('<li title="上一页" class="pagination-prev"><i class="iconfont icon-houtui"></i></li>')		 				
		  if(typeof display === "number" ){
            for(var i=0; i<display; i++){
                $(".pagination-box .pagination").append('<li title="'+(i+1)+'" class="pagination-item"><a>'+(i+1)+'</a></li>');
            }
          }else{
            // 带有省略号的分页 display: [[0,4],0,[8,9]]
            for(var j=0; j<display.length; j++){
              var data = display[j];
              if(data){ // 如果是0，就生成省略号
                  // 生成[0,4]，和[8,9]之间共7个分页项
                 for(var m=data[0]; m<=data[1]; m++){
                     $(".pagination-box .pagination").append('<li title="'+(m+1)+'" class="pagination-item"><a>'+(m+1)+'</a></li>');
                 }
              }else{
                  // 生成省略号
                  $(".pagination-box .pagination").append('<li class="pagination-ellipsis"><span class="teshu">...</span></li>');
              }
            }
        }
		  $(".pagination-box .pagination").append('<li title="下一页" class="pagination-next"><i class="iconfont icon-qianjin"></i></li>')		 
		  $("li[title='"+curPage+"']").addClass("pagination-item-active");
		},
		
		// 活动分页的显示方式
		getDisplay: function(current){
			 var pages = this.totalPages;  //获取总页数
			if(this._maxPages >= pages) return pages;
			var display = this.display;
			var newDisplay = [];

			//中间页的起始页和结尾页
			var start = current - Math.floor((display[1] - 1)/2);
			start = start < 0 ? 0 : start;
			var end = current + Math.ceil((display[1] - 1) / 2);
			end = end > pages ? pages : end;

			//若中间显示页的最后一页小于前和中显示页数，即前无...
			if(end < display[0] + display[1] ){
				newDisplay = [[0,display[0] + display[1] - 1] , 0 ,[pages - display[2] , pages - 1]];
				//若中间页
			}else if(pages - start <= display[1] + display[2]){
				newDisplay = [[0,display[0] - 1] , 0 , [pages - display[1] - display[2] , pages - 1]];
			}else{
				newDisplay = [[0 , display[0] - 1] , 0 ,
					[start , end] , 0 ,
					[pages - display[2] , pages - 1]
				];
			}
			return newDisplay;
			 
		},
		
		// 设置分页按钮的状态
        changePaginationView: function() {
            //去除所有元素的disabled状态
            $('.pagination .pagination-disabled').removeClass('pagination-disabled');		
            //若为第一页,上一页置灰
            this.current === 1 && $('.pagination-prev').addClass('pagination-disabled');
            //若为最后一页，则下一页置灰
            (this.current+1) > this.totalPages && $('.pagination-next').addClass('pagination-disabled');
			
        },
		
		//初始化事件
        initEvent: function() {
            var self = this;
            $('.pagination-box').on('click','li:not(".pagination-disabled")', function() {
                //点击按钮，获取当前页
                if($(this).hasClass('pagination-prev')) {
				    // 上一页
                    self.current -= 1;
					self.createPage(self.getDisplay(self.current),self.current);
                }else if($(this).hasClass('pagination-next')) {
				    // 下一页
                    self.current += 1;
					self.createPage(self.getDisplay(self.current),self.current);
                }else if($(this).hasClass('pagination-item')){
				    // 单击页码
				    self.current = parseInt($("a",this).text());
					self.createPage(self.getDisplay(self.current),self.current);
				}else{
				  return false;  // 防止单击省略号页面也跳转
				}
				//设置分页按钮的状态
                self.changePaginationView();
				// 跳转到指定页
                self.options.goToPage.call(self, self.current);
            });
        }
	};
