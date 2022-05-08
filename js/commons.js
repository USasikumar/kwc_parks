
// const SUBMENUS  =[{name:'Dog Parks',icon:'images/dogs.svg',alt:'Dogs'},
//                      {name:'Parks',icon:'images/parks.svg',alt:'Parks'},
//                      {name:'Trails',icon:'images/trails.svg',alt:'Trails'},
//                      {name:'Gardens',icon:'images/gardens.svg',alt:'Gardens'}];
const SUBMENUS  =[{name:'Parks',icon:'images/parks.svg',alt:'park'},
                  {name:'Trails',icon:'images/trails.svg',alt:'trail'},
                  {name:'Gardens',icon:'images/gardens.svg',alt:'garden'}];


function get_coordinates(jq_element,offset,content) {

   let ioffset= jq_element.offset() ;
   let width= jq_element.outerWidth(!content?true:false);
   let height= jq_element.outerHeight(!content?true:false);
   
   offset = Object.assign({width:0,height:0,top:0,left:0},offset);
   return {width: width + (offset ? offset.width : 0),height: height + (offset ? offset.height : 0),top:ioffset.top + (offset ? offset.top : 0),left:ioffset.left + (offset ? offset.left : 0)};

}

function side_menu(jq_hidden_menu,anchor_selector,coordinates) {

  const anchor = coordinates ? coordinates : get_coordinates($(anchor_selector));

  const jq_hidden = get_coordinates(jq_hidden_menu);

  const left_start = '100vw';
  // console.log('gp',anchor,jq_hidden);
  if (anchor.top.toFixed(1) == jq_hidden.top.toFixed(1) && anchor.left.toFixed(1) == jq_hidden.left.toFixed(1)) {

     jq_hidden_menu.animate({left:left_start},500, () => {
       jq_hidden_menu.css('display','none');
    });

  } else {

     jq_hidden_menu.css('display','inherit');
     jq_hidden_menu.css('top',anchor.top);
     jq_hidden_menu.css('height',anchor.height);
     jq_hidden_menu.css('width',anchor.width);
     // jq_hidden_menu.css('left','-100vw');
     jq_hidden_menu.css('left',left_start);

     jq_hidden_menu.animate({left:anchor.left},100);
  }


}

function expand_menu(jq_menu,evt) {

      let all_menu_items = jq_menu;

      let target = $(evt.currentTarget);


      if (target.text() == '+') {

         // close all others that are opened
         for (let item of all_menu_items) {
           item = $(item);
           if (target != item) {
             if (item.text() == '-') {
               item.click();
            }
          }
        }

        target.text('-');

        let city = target.prev().prev().text().toLowerCase();

         for (let sitem of SUBMENUS) {
           target.parent().parent().append(
            `<div class="div_hidden_menu_item submenu_item"">
                <img  class="div_hidden_menu_img" src="${sitem.icon}" alt="${city} ${sitem.alt}"/>
                <span class="spacer"></span>
                <span class="subli_text" alt="${city} ${sitem.alt}"/>${sitem.name}</span>
                <span class="spacer"></span>
             </div>`);
               
       
             $('.div_hidden_menu_img,.subli_text').click((evt) => {

                let target = evt.currentTarget;
                let city_type = $(target).attr('alt').split(' ');
                let city = city_type[0];
                let type = city_type[1];

                window.redirect_on_click('explore.html',{city,type});

              });



         }

      } else {
         target.text('+');
         target.parent().parent().find('.submenu_item').remove();    
      }
}

function serialize (obj) {
  var str = [];
  for (var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
    }
  return str.join('&');
}

function redirect_on_click(page_to_redirect,query) {

  let redirect_to = `${page_to_redirect}${query?'?'+serialize(query):''}`;

  console.log(`Redirection to ${redirect_to}`);

  window.location.replace(redirect_to);
}


//exporting

window.SUBMENUS = SUBMENUS;
window.get_coordinates = get_coordinates;
window.side_menu = side_menu;
window.expand_menu = expand_menu;
window.redirect_on_click;


