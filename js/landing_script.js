

 function enable_positioning(jq_element,coordinate) {

   jq_element.css('position','absolute');
   jq_element.css(coordinate);
   jq_element.off('click');
}

function animate_panel(jq_panel,starting_coordinate,duration) {

  jq_panel.css('position','absolute');


  jq_panel.css('width',starting_coordinate.width);
  jq_panel.css('height',starting_coordinate.height);
  jq_panel.css('top','100vh');
  jq_panel.css('left',starting_coordinate.left);

  jq_panel.animate({top:starting_coordinate.top,
                    left:starting_coordinate.left,
                    with:starting_coordinate.with,
                    height:starting_coordinate.height},
                    duration,() => {

        jq_panel.css('position','initial');
        jq_panel.attr('style','');

        jq_panel.find('img').css('cursor','normal');
        jq_panel.find('img').css('display','initial');

   // }, $.bez([0.77, 0.2, 0.05, 1.0]));
      });

}

function animate_footer_nav(jq_panel,starting_coordinate,duration,from='up') {

  jq_panel.css('position','absolute');

  jq_panel.css('width',starting_coordinate.width);
  jq_panel.css('height',starting_coordinate.height);
  jq_panel.css('top',from=='up'?'-10vh':'200vh');
  jq_panel.css('left',starting_coordinate.left);

  jq_panel.animate({top:starting_coordinate.top,
                    left:starting_coordinate.left,
                    with:starting_coordinate.with,
                    height:starting_coordinate.height},
                    duration,() => {

      jq_panel.attr('style','');
      jq_panel.css('display','inherit');


   });

}

function animate_logo(jq_logo,ending_coordinate,duration,callback) {

   jq_logo.animate(ending_coordinate,duration,() => {
     jq_logo.animate({opacity: 0},duration/2,  () => {
         jq_logo.css('display','none');
         if (callback){
             callback();
         }
      });
    // }, $.bez([0.77, 0.2, 0.05, 1.0]));
    });

}

function final_state() {

      // fix grid to center better
      $('#container').css('grid-template-columns','repeat(9, 1fr)');
      $('.landing').css('display', 'inherit');
      $('.splash_text').css('display','none');
      $('.splash_img').css('display','none');

      $('#waterloo_ctn').attr('style','');
      $('#waterloo_ctn').css('position','initial');
      $('#waterloo_ctn').find('img').css('cursor','normal');
      $('#waterloo_ctn').find('img').css('display','initial');

      $('#cambridge_ctn').attr('style','');
      $('#cambridge_ctn').css('position','initial');
      $('#cambridge_ctn').find('img').css('cursor','normal');
      $('#cambridge_ctn').find('img').css('display','initial');

      $('#kitchener_ctn').css('position','initial');
      $('#kitchener_ctn').attr('style','');
      $('#kitchener_ctn').find('img').css('cursor','normal');
      $('#kitchener_ctn').find('img').css('display','initial');

     $('footer').attr('style','');
     $('footer').css('display','inherit');

     $('nab').attr('style','');
     $('nav').css('display','inherit');
}

// document ready
$(() => {


  $(window).resize(function() {
     $('#hidden_menu').css('display','none');
  });

  //get query parameters
  let state = (new URLSearchParams(window.location.search)).get('state'); 

  if (state && state == 'final') {

     final_state();

  } else {

      $('.clickable').click((evt) => {
       // from splash page to landing page

      // fix grid to center better
      $('#container').css('grid-template-columns','repeat(9, 1fr)');
      const kitchener_logo = window.get_coordinates($('#splash_kitchener'));
      const waterloo_logo = window.get_coordinates($('#splash_waterloo'));
      const cambridge_logo = window.get_coordinates($('#splash_cambridge'),);
      const splash_text = window.get_coordinates($('#splash_text'));

       //need to be none to calculate the right value for the panels coordinates.
       $('.splash_text').css('display','none');
       $('.splash_img').css('display','none');

       //show landing panels
       $('.landing').css('display', 'inherit');

       // get initial coordinates of the panels
      const left_panel = window.get_coordinates($('#waterloo_ctn'));
      const middle_panel = window.get_coordinates($('#kitchener_ctn'));
      const right_panel = window.get_coordinates($('#cambridge_ctn'));

      const kitchener_final_logo = window.get_coordinates($('#kitchener_ctn img'));
      const waterloo_final_logo = window.get_coordinates($('#waterloo_ctn img'));
      const cambridge_final_logo = window.get_coordinates($('#cambridge_ctn img'));

      const nav_panel = window.get_coordinates($('nav'));
      const footer_panel = window.get_coordinates($('footer'));

      //back to its original state
       $('.splash_text').css('display','inherit');
       $('.splash_img').css('display','inherit');


      //get initial sizes and coordinates of the logos
      $('#kitchener_ctn img').css('display','none');
      $('#waterloo_ctn img').css('display','none');
      $('#cambridge_ctn img').css('display','none');

       // enable positioning
       enable_positioning($('#splash_kitchener'),kitchener_logo);
       enable_positioning($('#splash_waterloo'),waterloo_logo);
       enable_positioning($('#splash_cambridge'),cambridge_logo);
       enable_positioning($('#splash_text'),splash_text);

       //fade out splash text
       $('.splash_text').animate({opacity: 0},500);

       //animate panels
       animate_panel($('#waterloo_ctn'),left_panel,1000);
       animate_panel($('#kitchener_ctn'),middle_panel,1000);
       animate_panel($('#cambridge_ctn'),right_panel,1000);

       //animate nav and footer
       animate_footer_nav($('nav'),nav_panel,1000,'up');
       animate_footer_nav($('footer'),footer_panel,1000,'down');

       //move logos
       animate_logo($('#splash_kitchener'),kitchener_final_logo,1000);
       animate_logo($('#splash_waterloo'),waterloo_final_logo,1000);
       animate_logo($('#splash_cambridge'),cambridge_final_logo,1000);


      });
  }
  // bind hamburger menu
  // $('#hamburger_menu').click(() => {
  //    window.side_menu($('#hidden_menu'),'#cambridge_ctn');
  // });

  // $('.expand_menu').click(evt => {
  //     window.expand_menu($('.expand_menu'),evt);
  // }); 

  //set links to button the lead to explore page
  $('.city_opts_icons > img').click((evt) => {

    let target = evt.currentTarget;

    let city_type = $(target).attr('alt').split(' ');

    let city = city_type[0];
    let type = city_type[1];

    window.redirect_on_click('explore.html',{city,type});

  });

  // $(window).on('load', function(){
  //   let query = window.location.search;
  //   if (query == '?state=final') {
  //       window.location.search = '';
  //   }
  // });

});
