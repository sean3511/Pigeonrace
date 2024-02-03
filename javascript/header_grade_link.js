// 获取包含链接的容器元素
var pcHeaderLinksContainer = document.querySelector('.pc-header-gp-links-gradeGp-items');
var mobileHeaderLinksContainer = document.querySelector('.mobile-header-gp-links-gradeGp-items');

// 目录的相对路径
var directoryPath = 'area/';

// 需要生成的链接文本和文件名
var linksData = [
    { text: '新北鷺江', fileName: '新北鷺江.html' },
    // 在这里添加更多链接数据
];

// 遍历链接数据并生成链接元素
linksData.forEach(function(linkData) {
    var link = document.createElement('a');
    link.href = directoryPath + linkData.fileName;
    link.textContent = linkData.text;

    // 添加链接到pc-header容器
    var pcHeaderLink = link.cloneNode(true);
    pcHeaderLinksContainer.appendChild(pcHeaderLink);

    // 添加链接到mobile-header容器
    var mobileHeaderLink = link.cloneNode(true);
    mobileHeaderLinksContainer.appendChild(mobileHeaderLink);
});