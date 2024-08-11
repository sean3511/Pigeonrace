var overlay = document.getElementById("full_pop");
var closer =document.getElementsByClassName("close")[0];


$(".tile").click(function(){
    //讓header透明
    $('.page-header-bg').addClass('header-bg-visable');
    $('.page-header-bg').css("z-index","5")

     //顯示談窗
     overlay.style.display="block";
     //綁定滾動
     var tops = $(document).scrollTop();//当页面滚动时，把当前距离赋值给页面，这样保持页面滚动条不动
     $(document).bind("scroll",function (){$(document).scrollTop(tops); });

     if(screen.width < 770){
        $('#full_pop').toggleClass('slider');
     }
  });
$(".closer").click(function(){
    var child = Img_container.lastElementChild;  
    while (child) { 
        Img_container.removeChild(child); 
        child = Img_container.lastElementChild; 
    } 
    //關閉YT按鈕開啟30px的blocker
    $('.title_blocker').show();
    $('.linkicon').css('display','none'); 
    $('.ytcon').css('display','none'); 
    //讓header透明
    $('.page-header-bg').removeClass('header-bg-visable');
    $('.page-header-bg').css("z-index","9999")
     //解開滾動#
     $(document).unbind("scroll");
     $('.scroller-bar').scrollTop(0);
     //隱藏彈窗
     if(screen.width > 770)
     {
     overlay.style.display="none";
    }
     if(screen.width < 770){
        $('#full_pop').removeClass("slider");
        setTimeout(() => { overlay.style.display="none"; }, 500);
    }
  });
window.onclick = function(event){
    if(event.target == overlay){
        //關閉YT按鈕開啟30px的blocker
        $('.title_blocker').show();
        $('.ytcon').css('display','none'); 
        $('.linkicon').css('display','none'); 
        //讓header透明
        $('.page-header-bg').removeClass('header-bg-visable');
        $('.page-header-bg').css("z-index","9999");
        //解開滾動
        $(document).unbind("scroll");
        //重製scroller到頂部
        $('.scroller-bar').scrollTop(0);
        //隱藏彈窗
        if(screen.width > 770)
        {
        overlay.style.display="none";
        }
        //刪除圖片
   
        var child = Img_container.lastElementChild;  
        while (child) { 
            Img_container.removeChild(child); 
            child = Img_container.lastElementChild; 
        } 
        
        if(screen.width < 770){
            $('#full_pop').removeClass("slider");
            setTimeout(() => { overlay.style.display="none"; }, 500);
        }
    }
}
//創建元素在所選的作品
//新增刪除class name
function hasClass(el, className) {
    if (el.classList)
        return el.classList.contains(className);
    else
        return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
}
      
function addClass(el, className) {
    if (el.classList)
        el.classList.add(className);
    else if (!hasClass(el, className)) {
        el.className += " " + className;
    }
}

function removeClass(el, className) {
    if (el.classList)
        el.classList.remove(className);
    else if (hasClass(el, className)) {
        var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
        el.className=el.className.replace(reg, ' ');
    }
}
//淡出淡入
$(document).ready(function() {
    $('#home').css('display', 'none');
    $('#home').fadeIn(400); //一開始淡入
    $('a.link').click(function(event) { //點選 class 為 link 的 a 元件時觸發
     event.preventDefault(); //取消事件預設動作
     newLocation = this.href;
     $('#home').fadeOut(400, newpage); //點選後淡出
    });
    
    function newpage() {
     window.location = newLocation;
    }
   });
 // 當滾動時畫面的頂部離當前滾動位置>50則增加增加header背景
$(window).scroll(function(){
    ($(window).scrollTop() >= 50) ? (
        $('.page-header-bg').addClass('scrolled')
    ) : (
        $('.page-header-bg').removeClass('scrolled')
    );

    ($(window).scrollTop() >= 100) ? (
        $('.arrow_container').addClass('arrow_visable')
    ) : (
        $('.arrow_container').removeClass('arrow_visable')
    );
});
$(".nav-ham").click(function(){
    if($(this).hasClass('openclicked')) {
    //關閉div

    $('.mobile-nav').css("opacity", "1.0").animate({opacity: 0}, 50, function(){
        $('.mobile-nav').css("visibility", "hidden");
    });

    //解開滾動
    $(document).unbind("scroll");
    
    $(this).animate({opacity:0},300,function(){
        $('.nav-ham-logo').toggleClass('nav-logo-changer');
    })
    $(this).animate({opacity:1},300,)
    $(this).removeClass('openclicked');
    }
    else {
     //打開div
     $(".mobile-nav").css({'visibility': "visible",'opacity':'0' }).animate({opacity: 1}, 50);

     //綁定滾動
     var tops = $(document).scrollTop();//当页面滚动时，把当前距离赋值给页面，这样保持页面滚动条不动
     $(document).bind("scroll",function (){$(document).scrollTop(tops); });   

        $(this).animate({opacity:0},300,function(){
            $('.nav-ham-logo').toggleClass('nav-logo-changer');
        })
        $(this).animate({opacity:1},300,)
      $(this).addClass('openclicked');
    }
    $('.page-header').toggleClass('header-limitH');
    $('.page-header-bg').toggleClass('header-expend');
});
