$(document).ready(function(){
    
    //slider========================/
    var $slider = $(".slider"),
      $slideBGs = $(".slide__bg"),
      diff = 0,
      curSlide = 0,
      numOfSlides = $(".slide").length-1,
      animating = false,
      animTime = 2500,
      autoSlideTimeout,
      autoSlideDelay = 9000,
      $pagination = $(".slider-pagi");
  
  function createBullets() {
    for (var i = 0; i < numOfSlides+1; i++) {
      var $li = $("<li class='slider-pagi__elem'></li>");
      $li.addClass("slider-pagi__elem-"+i).data("page", i);
      if (!i) $li.addClass("active");
      $pagination.append($li);
    }
  };
  
  createBullets();
  
  function manageControls() {
    $(".slider-control").removeClass("inactive");
    if (!curSlide) $(".slider-control.left").addClass("inactive");
    if (curSlide === numOfSlides) $(".slider-control.right").addClass("inactive");
  };
  
  function autoSlide() {
    autoSlideTimeout = setTimeout(function() {
      curSlide++;
      if (curSlide > numOfSlides) curSlide = 0;
      changeSlides();
    }, autoSlideDelay);
  };
  
  autoSlide();
  
  function changeSlides(instant) {
    if (!instant) {
      animating = true;
      manageControls();
      $slider.addClass("animating");
      $slider.css("top");
      $(".slide").removeClass("active");
      $(".slide-"+curSlide).addClass("active");
      setTimeout(function() {
        $slider.removeClass("animating");
        animating = false;
      }, animTime);
    }
    window.clearTimeout(autoSlideTimeout);
    $(".slider-pagi__elem").removeClass("active");
    $(".slider-pagi__elem-"+curSlide).addClass("active");
    $slider.css("transform", "translate3d("+ -curSlide*100 +"%,0,0)");
    $slideBGs.css("transform", "translate3d("+ curSlide*50 +"%,0,0)");
    diff = 0;
    autoSlide();
  }

  function navigateLeft() {
    if (animating) return;
    if (curSlide > 0) curSlide--;
    changeSlides();
  }

  function navigateRight() {
    if (animating) return;
    if (curSlide < numOfSlides) curSlide++;
    changeSlides();
  }

  $(document).on("mousedown touchstart", ".slider", function(e) {
    if (animating) return;
    window.clearTimeout(autoSlideTimeout);
    var startX = e.pageX || e.originalEvent.touches[0].pageX,
        winW = $(window).width();
    diff = 0;
    
    $(document).on("mousemove touchmove", function(e) {
      var x = e.pageX || e.originalEvent.touches[0].pageX;
      diff = (startX - x) / winW * 70;
      if ((!curSlide && diff < 0) || (curSlide === numOfSlides && diff > 0)) diff /= 2;
      $slider.css("transform", "translate3d("+ (-curSlide*100 - diff) +"%,0,0)");
      $slideBGs.css("transform", "translate3d("+ (curSlide*50 + diff/2) +"%,0,0)");
    });
  });
  
  $(document).on("mouseup touchend", function(e) {
    $(document).off("mousemove touchmove");
    if (animating) return;
    if (!diff) {
      changeSlides(true);
      return;
    }
    if (diff > -8 && diff < 8) {
      changeSlides();
      return;
    }
    if (diff <= -8) {
      navigateLeft();
    }
    if (diff >= 8) {
      navigateRight();
    }
  });
  
  $(document).on("click", ".slider-control", function() {
    if ($(this).hasClass("left")) {
      navigateLeft();
    } else {
      navigateRight();
    }
  });
    
    $(document).on("click", ".slide .next", function() {
        curSlide++;
      if (curSlide > numOfSlides) curSlide = 0;
      changeSlides();
  });
  
  $(document).on("click", ".slider-pagi__elem", function() {
    curSlide = $(this).data("page");
    changeSlides();
  });
    //slider========================/
    
    
    
    
    
    $("body").append("<div id='setHeight' style='position:fixed; top:0; bottom:0;left:0;right:0;z-index:-10'></div>")
         var activeHeight = $("#setHeight").innerHeight();
         $("#setHeight").remove();

        if (($(".coming-soon").length) && ($(window).innerHeight() > $(window).innerWidth())) {
            $(".coming-soon").innerHeight(activeHeight);
        }
    
        if (($(".page_404").length) && ($(window).innerHeight() > $(window).innerWidth())) {
            $(".page_404 .wrap_float").innerHeight(activeHeight);
        }
    
        if (($(".homepage_slider").length) && ($(window).innerHeight() > $(window).innerWidth()) && ($(window).innerHeight() > 680) && ($(window).innerWidth() <= 1024)) {
            $(".homepage_slider").innerHeight(activeHeight);
        }
    
    

    
    
    
    //platform scripts========================/
    var iOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
    var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
    
    if (/IEMobile|Windows Phone/i.test(navigator.userAgent)) {
        var windowsPhone = true;
    }
    
    if ((isSafari && (screen.width <= 1050))) {
        $("body").addClass('iosSafari');
    }
    
    if ((isChrome && (screen.width <= 1050))) {
        $("body").addClass('chromeMobile');
    }
    
    var iOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    
    if (/IEMobile|Windows Phone/i.test(navigator.userAgent)) {
        var windowsPhone = true;
    }
    //platform scripts========================/


    //popup scripts========================/
    function popupFunction(){  
        if((iOS == true) || (windowsPhone == true)) {
            var scrollTop = $(window).scrollTop();
            var windowH = $(window).innerHeight();

            $("body").addClass("pop-up-open");
            $("body").attr("data-top", scrollTop);
            if (windowsPhone == true) {
                $("body").css("top", scrollTop);
            }
            $("body").css({
                "top": "-" + scrollTop + "px"
            });
        } 
    }

    function popupCloseFunction(){
        if((iOS == true) || (windowsPhone == true)) {
            var scTop = $("body").attr("data-top");
            if (windowsPhone == true) {
                var scTop = $("body").css("top");
            }
            var suffix = scTop.match(/\d+/);
            $("body").removeClass("pop-up-open");
            $("body").removeAttr("style");

            $("html, body").scrollTop(parseInt(suffix));
        }
    }
    //popup scripts========================/
    
    
    //main slider categories========================/
    $("#header_other_items .item").on("click", function(){
       var thisParent = $(this).parents("#header_categories");
        
        thisParent.toggleClass("scrolled");
    });
    //main slider categories========================/
    
    
    //search========================/
    $("#search_link").on("click", function(){
        $("#overlay").fadeIn(100);    
        $("#search_form").show();
        $("body").css("margin-right", scrollbarWidth());
        setTimeout(function () {
            $("#search_form").addClass("visible");
        }, 100);
        popupFunction();
        $("html, body").addClass("locked");
    });
    
    $("#search_form .close").on("click", function(){
        $("#overlay").fadeOut(100);    
        $("#search_form").hide();
        $("#search_form").removeClass("visible");
        popupCloseFunction();
        $("html, body").removeClass("locked");
        $("body").css("margin-right", "0");
    });
    //search========================/
    
    
    //scrollbar width========================/
    function scrollbarWidth() {
        var block = $('<div>').css({'height':'50px','width':'50px'}),
            indicator = $('<div>').css({'height':'200px'});

        $('body').append(block.append(indicator));
        var w1 = $('div', block).innerWidth();    
        block.css('overflow-y', 'scroll');
        var w2 = $('div', block).innerWidth();
        $(block).remove();
        return (w1 - w2);
    }
    //scrollbar width========================/
    
    
    //Gallery========================/
    $('.lightgallery').lightGallery({
        mode: 'lg-slide-circular',
        counter: false
    });
    
    $('.lightgallery').on('onBeforeOpen.lg',function(event){
        $("body").css("margin-right", scrollbarWidth());
    });
    $('.lightgallery').on('onBeforeClose.lg',function(event){
        $("body").css("margin-right", "0");
    });
    //Gallery========================/
    
    
    
    //Sliders========================/
    if ($("#most_popular__slider").length) {
        $('#most_popular__slider').slick({
            arrows: true,
            dots: false,
            slidesToShow: 2,
            slidesToScroll: 1,
            infinite: true,
            swipe: false,
            fade: false,
            touchMove: false,
            draggable: false,
            autoplay: true,
            variableWidth: true,
            speed: 400,
            autoplaySpeed: 20000,
            prevArrow: $('#most_popular__arrows .arrow.prev'),
            nextArrow: $('#most_popular__arrows .arrow.next'),
            
            responsive: [
                {
                  breakpoint: 1000,
                  settings: {
                      variableWidth: false,
                      slidesToShow: 1,
                      fade: false,
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                },
                {
                  breakpoint: 760,
                  settings: {
                      variableWidth: false,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                      fade: false,
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                }
              ]
        });
    }
    
    if ($("#popular_destination__slider").length) {
        $('#popular_destination__slider').slick({
            arrows: true,
            dots: false,
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: true,
            swipe: false,
            fade: false,
            touchMove: false,
            draggable: false,
            autoplay: true,
            variableWidth: true,
            speed: 400,
            autoplaySpeed: 20000,
            prevArrow: $('#popular_destination__arrows .arrow.prev'),
            nextArrow: $('#popular_destination__arrows .arrow.next'),
            responsive: [
                {
                  breakpoint: 1000,
                  settings: {
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                },
                {
                  breakpoint: 610,
                  settings: {
                      variableWidth: false,
                      slidesToShow: 1,
                      fade: false,
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                }
              ]
        });
    }
    
    if ($("#about-slider").length) {
        $('#about-slider').slick({
            arrows: true,
            dots: false,
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
            swipe: false,
            fade: false,
            touchMove: false,
            draggable: false,
            autoplay: false,
            centerMode: true,
            variableWidth: true,
            speed: 400,
            autoplaySpeed: 20000,
            prevArrow: $('.about-slider-arrows .arrow.prev'),
            nextArrow: $('.about-slider-arrows .arrow.next'),
            responsive: [
                {
                  breakpoint: 1000,
                  settings: {
                      swipe: true,
                        touchMove: false,
                        draggable: false,
                      variableWidth: false,
                      centerMode: false
                  }
                },
                {
                  breakpoint: 610,
                  settings: {
                      variableWidth: false,
                      slidesToShow: 1,
                      fade: false,
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                }
              ]
        });
    }
    
    if ($("#single-tour-slider").length) {
        $('#single-tour-slider').slick({
            arrows: true,
            dots: false,
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: true,
            swipe: false,
            fade: false,
            touchMove: false,
            draggable: false,
            autoplay: false,
            centerMode: true,
            variableWidth: true,
            speed: 300,
            autoplaySpeed: 20000,
            prevArrow: $('.tour-single-arrows .arrow.prev'),
            nextArrow: $('.tour-single-arrows .arrow.next'),
            responsive: [
                {
                  breakpoint: 1000,
                  settings: {
                      swipe: false,
            touchMove: false,
            draggable: false,
                      variableWidth: true,
                      centerMode: false
                  }
                }
              ]
        });
    }
    //Sliders========================/
    
    //Calendar========================/
    $(".js_calendar").datepicker({
      dateFormat: "dd/mm/yy",

        dayNamesMin: [ "S", "M", "T", "W", "T", "F", "S" ],
        dayNames: [ "Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота" ],
        monthNames: [ "January", "February", "March", "April", "May", "June", "Jule", "August", "September", "October", "November", "December" ],
        firstDay: 0,
        changeMonth: true,
        changeYear: true,
        yearRange: "1950:2024"
    });
    //Calendar========================/
    
    //Video replace========================/
    if ((screen.width <= 1050) && ($(".homepage_slider").length)) {
        $(".video_bg .video").remove();
        $(".video_bg[data-background]").each(function(){
            var thisScr = $(this).attr("data-background");

            $(this).attr("style", "background-image: url("+thisScr+")");
            $(this).removeAttr("data-background");
        });
    }
    //Video replace========================/
    
    
    //Accordeon========================/
    if ($(".faq_item").length) {
        $(".faq_item .faq_tab").on("click", function(e){
            e.preventDefault();
            
            var thisTab = $(this),
                thisItem = $(this).parent(),
                thisContent = $(this).next();
            
            thisItem.toggleClass("active");
            thisContent.slideToggle();
        });
    }
    //Accordeon========================/
    
    //Slick Gallery========================/
    if ($("#galleryslider").length) {
        $('#galleryslider .slider-top').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: true,
            dots: false,
            fade: false,
            variableWidth: true,
            infinite: true,
            asNavFor: '#galleryslider .slider-bottom',
            prevArrow: $('#galleryslider .arrow.prev'),
            nextArrow: $('#galleryslider .arrow.next'),
            responsive: [
                {
                  breakpoint: 1400,
                  settings: {
                      variableWidth: false,
                      slidesToShow: 1,
                      variableWidth: false
                  }
                },
                {
                  breakpoint: 1076,
                  settings: {
                      variableWidth: false,
                      slidesToShow: 1,
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                }
              ]
        });
        $('#galleryslider .slider-bottom').slick({
            slidesToShow: 3,
            slidesToScroll: 1,
            asNavFor: '#galleryslider .slider-top',
            dots: false,
            centerMode: false,
            variableWidth: true,
            infinite: true,
            focusOnSelect: true,
            responsive: [
                {
                  breakpoint: 1076,
                  settings: {
                      variableWidth: false,
                      swipe: true,
                        touchMove: false,
                        draggable: false
                  }
                }
              ]
        });
    }
    //Slick Gallery========================/
    
    //Single tabs========================/
    $("#tabsblock-tabs .tabsblock-tabs-tab").on("click", function(e){
        e.preventDefault();
        
        var thisTab = $(this),
            thisHref = thisTab.attr("data-href"),
            thisContent = $(thisHref);
        
        $("#tabsblock-tabs .tabsblock-tabs-tab").not(thisTab).removeClass("active");
        thisTab.addClass("active");
        $("#tabsblock_content .content").not(thisContent).hide();
        thisContent.show();
    });
    //Single tabs========================/
    
    
    //Dropdown menu========================/
    if (screen.width > 1076) {
        $(".dropdown_li").on({
            mouseenter: function () {
                var thisLi = $(this),
                   thisA = thisLi.children("a"),
                   thisMenu = thisLi.children("div");
                    thisMenu.stop( true, true ).fadeIn();
                    thisA.addClass("hover");
            },
            mouseleave: function () {
                var thisLi = $(this),
               thisA = thisLi.children("a"),
               thisMenu = thisLi.children("div");
                thisMenu.stop( true, true ).fadeOut();
              thisA.removeClass("hover");
            }
        });
    }
    $(".header__bottom .menu .scroll_wrap ul li.dropdown_li > a").on("click", function(e){
       e.preventDefault(); 
    });
    
    if (screen.width <= 1076) {
        $(".dropdown_li > a").on("click", function(){
            var thisA = $(this),
               thisLi = thisA.parent(),
               thisMenu = thisA.next("div");
                thisMenu.stop( true, true ).slideToggle();
              thisA.toggleClass("hover");
        });
    }
    //Dropdown menu========================/
    
    
    //Mobile menu========================/
    $("#mobile_btn").on("click", function(e){
        e.preventDefault();
        $("#js-menu").fadeIn();
        $("html, body").addClass("locked");
        popupFunction();
    });
    
    $("#js-menu .close").on("click", function(e){
        e.preventDefault();
        $("#js-menu").fadeOut();
        $("html, body").removeClass("locked");
        popupCloseFunction();
    });
    //Mobile menu========================/
    
    
    //User rating========================/
    $(".user-rating .star").on({
        mouseenter: function () {
            var thisStar = $(this),
               thisParent = thisStar.parent(".stars"),
               thisStarNum = thisStar.index();
              thisParent.children(".star").removeClass("fill");
              thisParent.children(".star").slice(0,thisStarNum+1).addClass("fill");
        },
        mouseleave: function () {
            var thisStar = $(this),
               thisParent = thisStar.parent(".stars"),
               thisStarNum = thisStar.index();
              thisParent.children(".star").removeClass("fill");
        }
    });

    $(".user-rating .star").on("click", function(e){
        e.preventDefault();
        var thisStar = $(this),
           thisParent = thisStar.parent(".stars"),
           thisStarNum = thisStar.index();

          thisParent.children(".star").slice(0,thisStarNum+1).addClass("selected");
    });
    //User rating========================/
    
    //открытие модалок
    $('.getModal').on('click', function(e){
        e.preventDefault();
        var thisLink = $(this);
        var target_modal = $(this).attr("data-href");
        $(target_modal).arcticmodal({
            openEffect:{speed:150},
            beforeOpen: function(data, el) {
                popupFunction();
            },
            afterOpen: function(data, el) {
                
            },
            afterClose: function(data, el) {
                popupCloseFunction();
            }
        });
    });
    
    $('.modal_close').on('click', function(){
        $(this).arcticmodal('close');
    });
    
    
    
    //Footer fix========================/
    $(window).on('resize',function() {
        var footerHeight = $(".footer").innerHeight(),
            windowHeight = $(window).innerHeight(),
            containerHeight = $(".container").innerHeight();
        
//        alert(windowHeight);
//        alert(containerHeight);
        
        if (!$(".footer").hasClass("absolute")) {
            if (containerHeight <= windowHeight) {
                $(".footer").addClass("absolute");
                $(".container").addClass("fullheight");
            }
        } else {
            if ((containerHeight+footerHeight) >= windowHeight) {
                $(".footer").removeClass("absolute");
                $(".container").removeClass("fullheight");
            }
        }
        
    });
    //Footer fix========================/


    $(window).trigger('resize');
    
    
    var spincrement = true;
    
    if ($("#statistic").length) {
        var statisticSection = $("#statistic").offset().top;
        
        $(".spincrement").each(function(){
           $(this).attr("data-final", ($(this).text()));
        });
    }
    
    

    $(window).on("scroll", function() {
        var scroll = $(window).scrollTop();
        var contentH = $(window).innerHeight();
        
        if ($(".tour-single").length) {
            var singleContentOffset = $(".tour-single .single-content").offset().top;
            var singleContentEndOffset = $(".tour-single #end-single-content").offset().top;
            
            if ((scroll>singleContentOffset) && (scroll<singleContentEndOffset)) {
                $('.mobile-fixed-bottom').fadeIn().css("display", "flex");
            } else {
                $('.mobile-fixed-bottom').fadeOut();
            }
        }

        if ($("#statistic").length) {
            if ((scroll>statisticSection - contentH) && (spincrement==true)) {
                spincrement = false;
                
                $(".spincrement").each(function(){
                   var thisSpincrement = $(this),
                       thisFinal = +(thisSpincrement.attr("data-final")),
                       thisStart = +(thisSpincrement.attr("data-start"));
                    
                    thisSpincrement.spincrement({
                        from: thisStart,
                        to: thisFinal,
                        decimalPlaces: 0, 
                        decimalPoint: ".",
                        thousandSeparator: "",
                        duration: 5000
                    });
                });
            }
        }
        
    });
    
    $(".day-item .day-head").on("click", function(){
       var thisDayHead = $(this),
           thisDayBody = thisDayHead.next(".day-body");
        
        thisDayHead.toggleClass("active");
        thisDayBody.slideToggle();
    });
    
    if ($("#gmap").length) {
        // When the window has finished loading create our google map below
    google.maps.event.addDomListener(window, 'load', init);

    function init() {
        var mapOptions = {
            zoom: 15,
            scrollwheel: false,
            navigationControl: false,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            zoomControl: true,
            fullscreenControl: true,
            fullscreenControlOptions: {
                position: google.maps.ControlPosition.LEFT_BOTTOM
            },
            /*draggable: false,*/

            // The latitude and longitude to center the map (always required)
            center: new google.maps.LatLng(40.6064628, -74.1244976), // New York
            styles:
            [
                {
                    "stylers": [
                        {
                            "visibility": "simplified"
                        }
                    ]
                },
                {
                    "stylers": [
                        {
                            "color": "#131314"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "stylers": [
                        {
                            "color": "#131313"
                        },
                        {
                            "lightness": 7
                        }
                    ]
                },
                {
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "visibility": "on"
                        },
                        {
                            "lightness": 25
                        }
                    ]
                }
            ]
        };

        var mapElement = document.getElementById('gmap');

        // Create the Google Map using our element and options defined above
        var map = new google.maps.Map(mapElement, mapOptions);

        // Let's also add a marker while we're at it
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(40.6064628, -74.1244976),
            map: map,
            title: 'Address',
            icon: "img/map-marker.svg"
        });
    }
    }
    
});	
