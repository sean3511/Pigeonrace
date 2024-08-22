    //自動加載區域相關功能
    // 1自動加載PC背景
    document.addEventListener("DOMContentLoaded", function() {
        const imageDirectory = 'image/piegon_img/'; // 相对路径
        const imageExtension = '.jpg';
        const areas = document.querySelectorAll('.pc-areagroup .item-area');
    
        areas.forEach((area, index) => {
            let imageNumber = (index + 1).toString().padStart(2, '0');
            let imageUrl = `${imageDirectory}${imageNumber}${imageExtension}`;
            console.log("Loading image from:", imageUrl); // 调试输出
            area.style.backgroundImage = `linear-gradient(180deg, rgba(0, 0, 0, 0.00) 0%, rgba(0, 0, 0, 0.60) 100%), url(${imageUrl})`;
        });
    });
    
    
    
    // 您的代码逻辑
    // 協助載入header
    $(document).ready(function(){
        $("#header-placeholder").load("header.html");
    });
    // 切換pc比賽紀錄
    $(".show-grade").click(function() {
        $(".list-grade").toggleClass("visible");
    });
    $(".show-piegon").click(function() {
        $(".list-piegon").toggleClass("visible");
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

// 此功能用於各季節鴿子的即將到來
document.addEventListener("DOMContentLoaded", function() {
    // 获取所有带有 `coming-soon` 类的元素
    const comingSoonElements = document.querySelectorAll('.coming-soon');
  
    // 遍历每个元素，在其底部添加 <p> 标签
    comingSoonElements.forEach(function(element) {
      const p = document.createElement('p');
      
      // 使用 classList.add 添加多个类
      p.classList.add('itam_area_padding', 'comming-soon-font');
      p.textContent = '即將到來';
  
      // 将 <p> 标签添加到目标元素的末尾
      element.appendChild(p);
    });
  });
  