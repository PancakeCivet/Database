$(document).ready(function() {
    $("#get-product").click(function() {
        $.ajax({
            url: "get_message.html",
            method: "GET",
            success: function(data) {
                var name = $(data).find("#product-name").text();
                var price = $(data).find("#product-price").text();
                var description = $(data).find("#product-description").text();
                var image = $(data).find("#product-image").attr("src");
                console.log("商品名称：", name);
                console.log("商品价格：", price);
                console.log("商品简介：", description);
                console.log("商品图片：", image);
            },
            error: function() {
                console.log("请求失败");
            }
        });
    });
});