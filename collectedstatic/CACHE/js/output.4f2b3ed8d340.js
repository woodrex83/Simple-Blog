var csrftoken=$('input[name=csrfmiddlewaretoken]').val();function csrfSafeMethod(method){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
$(document).ready(function(){$("tr").on("click","#ajax_delete",function(){var flag=confirm("您真的確定要删除嗎？")
if(flag){var pk=$(this).data('id');var slug1=$(this).data('slug');var url='/blog/'+slug1+'/article/'+pk+'/delete'
$.ajax({url:url,type:"POST",beforeSend:function(xhr,settings){if(!csrfSafeMethod(settings.type)&&!this.crossDomain){xhr.setRequestHeader("X-CSRFToken",csrftoken);}},success:function(res){swal({title:"Deleted！",text:"文章已刪除!",type:"error",},function(){$('#ajax_delete').parents('tr').remove()
window.location.reload()});}})}})});