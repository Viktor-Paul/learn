(function($){
	$.fn.addPagingBarToTable = function(obj){
		function pagingObject($pagingTable){
			this.$pagingBar = null;
			var currentObj = this;
			var pagingInfo = {
					current:1,	//当前页数
					pages:0,	//总页数,
					records:20,	//每页条数
					count:0		//总条数
				};
			if(obj.records){
				pagingInfo.records = obj.records;
			}
			this.init = function(){
				if(obj.foldPrefix){
					var selecterStr = "[class*="+obj.foldPrefix+"]"
					pagingInfo.count = $pagingTable.children("tbody").children("tr").not(":first").not(selecterStr).length;
				}else{
					pagingInfo.count = $pagingTable.find("tr").not(":first").length;
				}
				if(pagingInfo.count < 15){
					return;
				}
				//加入分页div
				var pagingHtmlStr = '<div class="cmn_page" style="text-align:center;">'+
				' <a href="#" class="first" >首页</a> '+
				' <a href="#" class="prev">上一页</a> '+
				'<select class="paging_pages"></select>'+
				' <a href="#" class="next">下一页</a> '+
				' <a href="#" class="last">末页</a> '+
				'  [每页 <select class="paging_records">'+
				'<option value="5">5</option>'+
				'<option value="10">10</option>'+
				'<option value="20">20</option>'+
				'<option value="50">50</option>'+
				'<option value="100">100</option></select>条]'+
				'   [共<span class="paging_count">0</span>条]'+
				'</div>';
				if($pagingTable.next().attr("class") == "cmn_page"){
					$pagingTable.next().replaceWith(pagingHtmlStr);
				}else{
					$pagingTable.after(pagingHtmlStr);
				}
				var $pagingBar = this.$pagingBar = $pagingTable.next();
				$pagingBar.find("select.paging_records option").each(function(index,ele){
					if($(ele).val() == pagingInfo.records){
						$(ele).attr("selected","selected");
					}
				});
				$pagingBar.find("select.paging_records").bind("change",recordsChange);
				$pagingBar.find("span.paging_count").text(pagingInfo.count);
				//第一次计算总页数
				calculatePages($pagingBar);	
				doPaging($pagingBar);
				//注册事件
				$pagingBar.delegate("a.first","click",function(e){
					pagingInfo.current = 1;
					var current_str = pagingInfo.current+'/'+pagingInfo.pages;
					$pagingBar.find("select.paging_pages").val(pagingInfo.current);
					doPaging($pagingBar);
					return false;
				});
				$pagingBar.delegate("a.last","click",function(e){
					pagingInfo.current = pagingInfo.pages;
					var current_str = pagingInfo.current+'/'+pagingInfo.pages;
					$pagingBar.find("select.paging_pages").val(pagingInfo.current);
					doPaging($pagingBar);
					return false;
				});
				$pagingBar.delegate("a.prev","click",function(e){
					pagingInfo.current--;
					if(pagingInfo.current <= 0){
						pagingInfo.current = 1;
					}
					var current_str = pagingInfo.current+'/'+pagingInfo.pages;
					$pagingBar.find("select.paging_pages").val(pagingInfo.current);
					doPaging($pagingBar);
					return false;
				});
				$pagingBar.delegate("a.next","click",function(e){
					pagingInfo.current++;
					if(pagingInfo.current > pagingInfo.pages){
						pagingInfo.current = pagingInfo.pages;
					}
					var current_str = pagingInfo.current+'/'+pagingInfo.pages;
					$pagingBar.find("select.paging_pages").val(pagingInfo.current);
					doPaging($pagingBar);
					return false;
				});
			};
			//定义select event handler
			//select标签的change事件在ie中是不会冒泡的。所以不能用事件代理
			function pagesChange(e){
				pagingInfo.current = currentObj.$pagingBar.find("select.paging_pages").val();
				doPaging(currentObj.$pagingBar);
				return false;
			}
			function recordsChange(e){
				pagingInfo.records = currentObj.$pagingBar.find("select.paging_records").val();
				pagingInfo.current = 1;
				calculatePages(currentObj.$pagingBar);	
				doPaging(currentObj.$pagingBar);
			}
			/*定义函数*/
			//切换每页条数时，需要重新计算总页数
			var calculatePages = function($pagingBar){
				//计算新页数
				var pages_round = Math.round(pagingInfo.count/pagingInfo.records);
				var pages_calculate = pagingInfo.count/pagingInfo.records;
				if(pages_round >= pages_calculate){
					pagingInfo.pages = pages_round;
				}else if(pages_round < pages_calculate){
					pagingInfo.pages = pages_round + 1;
				}
				//设置当前页下拉框
				pagingInfo.current = 1;
				var $new_select = '<select class="paging_pages">';
				for(var page_index = 1;page_index<=pagingInfo.pages;page_index++){
					page_index_str = page_index+'/'+pagingInfo.pages;
					$new_select += '<option value = "'+page_index+'" >'+page_index_str+'</option>';
				}
				$new_select += '</select>';
				$pagingBar.find("select.paging_pages").replaceWith($new_select);
				$pagingBar.find("select.paging_pages").bind("change",pagesChange);
			};
			//进行分页 
			var doPaging = function($pagingBar){
				//计算要隐藏的行
				var start_index = (pagingInfo.current-1)*pagingInfo.records + 1;
				var end_index = pagingInfo.current*pagingInfo.records;
				if(obj.foldPrefix){
					var selecterStr = "[class*="+obj.foldPrefix+"]"
					$pagingTable.children("tbody").children("tr").not(":first").filter(selecterStr).each(function(index,ele){
						$(ele).hide();
					});
					$pagingTable.children("tbody").children("tr").not(":first").not(selecterStr).each(function(index,ele){
						var tr_index = index+1;
						var $tr = $(ele);
						if(tr_index>=start_index && tr_index<=end_index){
							$tr.show();
							while($tr.next().hasClass("show")){
								$tr.next().css("display","table-row");
								$tr = $tr.next();
							}
						}else{
							$tr.hide();
						}
					});
				}else{
					$pagingTable.find("tr").not(".first_title").each(function(index,ele){
						var tr_index = index+1;
						var $tr = $(ele);
						if(tr_index>=start_index && tr_index<=end_index){
							$tr.show();
						}else{
							$tr.hide();
						}
					});
				}
			};
		};
		var $pagingTable = this;
		this.pagingObj = new pagingObject($pagingTable);
		this.pagingObj.init();
	};
}
)(jQuery);