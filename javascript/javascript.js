
    // 您的代码逻辑
    // 協助載入header
    $(document).ready(function(){
        $("#header-placeholder").load("header.html");
    });
    // 切換pc比賽紀錄
    $(".pc-header-gp-links-gradeGp").click(function() {
        $(".pc-header-gp-links-gradeGp-items").fadeToggle(); // 切换淡入淡出
    });
    $(".mobile-header-gp-links-gradeGp").click(function() {
        $(".mobile-header-gp-links-gradeGp-items").slideToggle(); // 切换淡入淡出
    });
    // 切換手機ham
    $(".btn_ham").click(function() {
        $(".mobile-overlay").fadeIn(300); // 切换淡入淡出
    });
    $(".btn_cross").click(function() {
        $(".mobile-overlay").fadeOut(300); // 切换淡入淡出
    });
    // 設定手機菜單出現尺寸
    $(window).on('resize', function() {
        var width = $(window).width();
        if (width > 1024) {
            $(".mobile-overlay").hide();
        }
    });
    // 旋轉icon使用
    $(".pc-header-gp-links-gradeGp").click(function() {
        $(this).find("img").toggleClass("rotate");
    });
    $(".mobile-header-gp-list").click(function() {
        $(this).find("img").toggleClass("rotate");
    });
