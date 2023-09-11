$(document).ready(function() {
    // для версии в маленьким экраном.
    $(".btn-details").on("click touchstart", function(event) {
        event.preventDefault();
        var stockId = $(this).closest(".stock-card").attr("id").split("-")[2];
        $("#stock-description-" + stockId).addClass("show");
        $(".main-content").addClass("darken");
    });

    $(".btn-close").on("click touchstart", function(event) {
        event.preventDefault();
        $(this).closest(".stock-description").removeClass("show");
        $(".main-content").removeClass("darken");
    });


    // для мобильной версии
    $(".btn-details").on("click touchstart", function(event) {
        event.preventDefault();
        var stockId = $(this).closest(".stock-card").attr("id").split("-")[2];
        $("#stock-descriptionMobile-" + stockId).addClass("show");
        $(".main-content").addClass("darken");
    });

    $(".btn-close").on("click touchstart", function(event) {
        event.preventDefault();
        $(this).closest(".stock-descriptionMobile").removeClass("show");
        $(".main-content").removeClass("darken");
    });


    //затемнение
    $(".btn-details").on("click touchstart", function(event) {
        event.preventDefault();
        var stockId = $(this).data("stock-id");
        $("#stock-description-" + stockId).addClass("show");
        $("body").addClass("darken");
    });
    $(".btn-close").on("click touchstart", function(event) {
        event.preventDefault();
        $(this).closest(".stock-description").removeClass("show");
        $("body").removeClass("darken");
    });
});