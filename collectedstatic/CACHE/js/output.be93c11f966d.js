var token=$('input[name=csrfmiddlewaretoken]').val();$('#id_edit').click(function(){$.ajax({url:'/blog/set_nickname/',type:'post',data:{'new_nickname':$('#id_new_nickname').val(),csrfmiddlewaretoken:token,},success:function(args){if(args.code==2000){swal({title:"",text:args.msg,type:"success",},function(){window.location.reload()});}else{swal(args.msg,'','warning')}}})});let parentId=null
var token=$('input[name=csrfmiddlewaretoken]').val();$('.action').click(function(){let isLike=$(this).hasClass('diggit');let $div=$(this);$.ajax({url:'/comment/like/',type:'post',data:{'article_id':'1','is_like':isLike,csrfmiddlewaretoken:token,},success:function(args){if(args.code==1000){$('#digg_tips').text(args.msg)
let oldNum=$div.children().text();$div.children().text(Number(oldNum)+1)}else{$('#digg_tips').html(args.msg)}}})})
$('#id_submit').click(function(){let conTent=$('#id_comment').val();if(parentId){let indexNum=conTent.indexOf('\n')+1;conTent=conTent.slice(indexNum)}
$.ajax({url:'/comment/send_comment/',type:'post',data:{'article_id':'1','content':conTent,'parent_id':parentId,csrfmiddlewaretoken:token,},success:function(args){if(args.code==1000){$('#error').text(args.msg)
window.location.reload()
$('#id_comment').val('')
parentId=null;}}})})
$('.reply').click(function(){let commentUserName=$(this).attr('nickname');parentId=$(this).attr('comment_id');$('#id_comment').val('@'+commentUserName+'\n').focus()});