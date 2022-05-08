const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const TYPE = urlParams.get('type');
const CITY = urlParams.get('city');


var MYDATA = eval(CITY + '_' + TYPE);

var responsiveSlider = function () {

    let box = document.querySelector('#slideWrap');
    let width = box.offsetWidth;
    // console.log(width);

    var slider = document.getElementById('slider');
    var sliderWidth = slider.offsetWidth;
    var slideList = document.getElementById('slideWrap');
    var count = 1;
    var items = slideList.querySelectorAll('li').length;
    var left_value = 1;

    var number_of_images = 1;
    var pictures_used = [];
    var ameniti_option = '<datalist id="cityname">';
    var ameniti_list = [];
    MYDATA.forEach(element => {

        // generic image
        if (element.picture.length == 0) {
           element.picture.push('images/citypark.png');
        }

        if (element.picture.length > 0 && !pictures_used.includes(element.picture[0])) {
            // console.log('s');
            var list = document.createElement('li');
            var img = document.createElement('img');
            pictures_used.push(element.picture[0]);
            img.src = element.picture[0];
            list.appendChild(img);
            document.getElementById('slideWrap').appendChild(list);
            number_of_images += 1;
        }

        if (element.amenities.length > 0 && element.picture.length > 0) {
            element.amenities.forEach(element => {
                if (!ameniti_list.includes(element)) {
                    ameniti_list.push(element);
                    ameniti_option += '<option value="' + element + '">';
                }

            });
        }
    });
    ameniti_option += '</datalist>';
    $('#ameniti_search_input').after(ameniti_option);

    var current_image = 1;
    var left_move_size = 0;
    var total_width = 0;
    // console.log(number_of_images);

    var nextSlide = function () {
        total_width = 0;

        for (let index = 1; index <= number_of_images; index++) {
            $('li img:eq(' + index + ')').each(function () {
                total_width += $(this).width();
            });
        }

        $('li img:eq(' + current_image + ')').each(function () {
            left_move_size += $(this).width();
            if ((total_width - left_move_size) < $('#slider').width()) {
                slideList.style.left = '0px';
                current_image = 1;
                left_move_size = 0;
            } else {
                slideList.style.left = '-' + left_move_size + 'px';
                current_image += 1;
            }
        });
    };

    setInterval(function () {
        nextSlide();
    }, 4000);

};

function getMapLink(city,map_element){


     let map = null;
     let url ='';

     let extract_from_b64 = (map_encoded) => {

          let decoded_map = atob(map_element);
          map = decoded_map.match(/RenderGoogleMap\(\"(-?\d+\.?\d*)\",\s*"(-?\d+\.?\d*)\"[^\)]+\)/);
          if (!map) {
            map = atob(map_element).match(/\"latitude\":\"(-?\d+\.?\d*)\",\s*\"longitude\":\"(-?\d+\.?\d*)\"/);
          }
          return map;
     };

     switch(city.toLowerCase()) {
        case 'kitchener':
          map = extract_from_b64(map_element);
          url = `https://maps.google.com/maps?q=${map[1]},${map[2]}&hl=es&z=17&amp;output=embed`;
          break;
        case 'cambridge':
          map = extract_from_b64(map_element);
          url = `https://maps.google.com/maps?q=${map[1]},${map[2]}&hl=es&z=17&amp;output=embed`;
          break;
        default:
             // waterloo
             url = `https://maps.google.com/maps?q=${map_element[0]},${map_element[1]}&hl=es&z=17&amp;output=embed`;
     }

     // will be lazy loaded
     return url;

}

var setCards = function (amenities = null) {
    var number_of_cards = 0;
    var final_html = '';
    var pictures_used = [];
    let nelement =  0;
    MYDATA.forEach(element => {
        nelement=+1;
        
        // generic image
        if (element.picture.length == 0) {
           element.picture.push('images/citypark.png');
        }

        if (amenities == null) {
            if (element.picture.length > 0 && number_of_cards <= 8 && !pictures_used.includes(element.picture[0])) {
                final_html += `
                           <div class="each_card">
                           <div class="rating_container">
                              <div class="rating_star">
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star"></span>
                              </div>
                           </div>
                           <div style="background: url(${element.picture[0]}) no-repeat;    background-size: cover;" class="explore_card">
                             <h2 class="card_description">${element.name}</h2>
                          </div>
                          <div class="modal-container">
                            <input class="modal-toggle" type="checkbox">
                            <div class="modal-backdrop">
                              <div class="modal-content" style="background-color: rgba(0, 0, 0, 0.70);">
                                <div class="blur_overlay"> 
                                  <div class="modal-content-header">
                                     <h2></h2>
                                     <h2>${element.name}</h2>
                                     <h2 class="modal-content-exit">[X]</h2>
                                  </div>
                                <section class="modal-content-body">
                                  <div class="modal-content-desc">
                                     ${element.description.charAt(0).toUpperCase() + element.description.slice(1)}
                                  </div>
                                  <div class="modal-content-address">
                                    Address: 
                                  </div>
                                  <span>  ${element.address} </span> 
                                  <div class="modal-content-address">
                                    Hours: 
                                  </div>
                                  <span> ${element.hours?element.hours:''} </span> 
                                  <div >Amenities:</div>
                                     <ul class="modal-content-amenities">
                                     ${ element.amenities.map(el=> {
                                       return '<li>' + el + '</li>';
                                     }).join('')}
                                     </ul>
                                  <div class="modal-content-map">
                                    Map: 
                                  </div>
                                     <div class="map_url">
                                       ${getMapLink(CITY,element.map)}
                                     </div>
                                </section>
                               </div>
                              </div>
                            </div>
                           </div>
                          </div>`;
                pictures_used.push(element.picture[0]);
            }
        } else {
            if (element.picture.length > 0 && number_of_cards <= 8 && !pictures_used.includes(element.picture[0])) {
                if (element.amenities.includes(amenities)) {
                final_html += `
                           <div class="each_card">
                           <div class="rating_container">
                              <div class="rating_star">
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star"></span>
                              </div>
                           </div>
                           <div style="background: url(${element.picture[0]}) no-repeat;    background-size: cover;" class="explore_card">
                             <h2 class="card_description">${element.name}</h2>
                          </div>
                          <div class="modal-container">
                            <input class="modal-toggle" type="checkbox">
                            <div class="modal-backdrop">
                              <div class="modal-content" style="background-color: rgba(0, 0, 0, 0.70);">
                                <div class="blur_overlay"> 
                                  <div class="modal-content-header">
                                     <h2></h2>
                                     <h2>${element.name}</h2>
                                     <h2 class="modal-content-exit">[X]</h2>
                                  </div>
                                <section class="modal-content-body">
                                  <div class="modal-content-desc">
                                     ${element.description.charAt(0).toUpperCase() + element.description.slice(1)}
                                  </div>
                                  <div class="modal-content-address">
                                    Address: 
                                  </div>
                                  <span>  ${element.address} </span> 
                                  <div class="modal-content-address">
                                    Hours: 
                                  </div>
                                  <span> ${element.hours?element.hours:''} </span> 
                                  <div >Amenities:</div>
                                     <ul class="modal-content-amenities">
                                     ${ element.amenities.map(el=> {
                                       return '<li>' + el + '</li>';
                                     }).join('')}
                                     </ul>
                                  <div class="modal-content-map">
                                    Map: 
                                  </div>
                                     <div class="map_url">
                                       ${getMapLink(CITY,element.map)}
                                     </div>
                                </section>
                               </div>
                              </div>
                            </div>
                           </div>
                          </div>`;
                    number_of_cards += 1;
                    pictures_used.push(element.picture[0]);
                }
            }
        }
        // let decoded_map  = atob(element.map);
        // console.log(decoded_map);
    });
    document.getElementById('card_container').innerHTML = final_html;

    //attach clicks
    $('.each_card').click((evt) => {

         let target = $(evt.currentTarget).find('.modal-toggle');

         if(evt.target.classList.contains('modal-content-exit')) {
           target.prop('checked',false);
         } else if ( ! target.prop('checked')) {

           let parent_ctn = $(evt.currentTarget).find('.map_url').parent();
           
           if (parent_ctn.find('iframe').length == 0) {
             let map_ctn =$(evt.currentTarget).find('.map_url');

             let url = map_ctn.text();
             let frame = `<iframe 
                          height="370"
                          width="800"
                          frameborder="0"
                          scrolling="no"
                          marginheight="0"
                          marginwidth="0"
                          src="${url}"
                         >
                         </iframe>`;
             parent_ctn.append(frame);

             //asjust overlay panel
             let panel_coords = window.get_coordinates(target.parent().find('.modal-content-body'),undefined,true);
             let coords = window.get_coordinates(parent_ctn.find('iframe'));

             let panel_bottom = panel_coords.top + panel_coords.height;
             let map_bottom = coords.top + coords.height;


             if (map_bottom  >= panel_coords ) {

               let new_height = coords.height + (map_bottom - panel_coords); 
               target.parent().find('.modal-content').css('height',new_height + 10);

             }

           }
           target.prop('checked',true);
         }
    });

};

var showResult = function () {
    var amenities_value = $('#ameniti_search_input').val();
    setCards(amenities_value);
};

var clearResult = function () {
    setCards();
};

window.onload = function () {


    document.getElementById('search_button').addEventListener('click', showResult);
    document.getElementById('clear_button').addEventListener('click', clearResult);
    document.getElementById('city_name').innerHTML = `
                 <img class="city_name_icon" src="images/${CITY =='Kitchener'?'kit3.svg':(CITY=='Waterloo'? 'wat3.svg':'cam3.svg')}" alt="${CITY} icon"/>
                 <h2>${CITY}</h2>`;

    var svg_image_element = document.createElement('img');
    svg_image_element.src = 'images/' + TYPE + 's.svg';
    document.getElementById('park_type').appendChild(svg_image_element);

    responsiveSlider();
    setCards();


    var objToday = new Date(),
        weekday = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
        dayOfWeek = weekday[objToday.getDay()],
        domEnder = function () { var a = objToday; if (/1/.test(parseInt((a + '').charAt(0)))) return 'th'; a = parseInt((a + '').charAt(1)); return 1 == a ? 'st' : 2 == a ? 'nd' : 3 == a ? 'rd' : 'th'; }(),
        dayOfMonth = today + (objToday.getDate() < 10) ? '0' + objToday.getDate() + domEnder : objToday.getDate() + domEnder,
        months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'),
        curMonth = months[objToday.getMonth()],
        curYear = objToday.getFullYear();
    var today = dayOfWeek + ' ' + dayOfMonth + ' of ' + curMonth + ', ' + curYear;

    $('#date').text(today);


};

