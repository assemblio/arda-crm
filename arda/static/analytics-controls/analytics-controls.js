$(document).ready(function(){
  var menuLeft = document.getElementById( 'cbp-spmenu-s1' );
  var showLeft = document.getElementById( 'showLeft' );
  var menuTitle = document.getElementById( 'menuTitle' );
  
  classie.toggle( menuLeft, 'cbp-spmenu-open' );

  $('#menuTitle').click(function() {
    
    classie.toggle( document.body, 'cbp-spmenu-push-toleft' );
    classie.toggle( menuLeft, 'cbp-spmenu-open' );
    classie.toggle( menuTitle, 'showLeft-collapsed' );

    if(classie.has( menuTitle, 'showLeft-collapsed' )){
      $('#showLeft').html('&raquo');

      // Hide menu item borders when sidebar menu collapsed
      $( ".cbp-spmenu li" ).each(function() {
        $( this ).css('border-bottom-color', '#222')
      });


    }else{
      $('#showLeft').html('&laquo');

      // Show menu item borders when sidebar menu collapsed
      $( ".cbp-spmenu li" ).each(function() {
        $( this ).css('border-bottom-color', '#258ecd')
      });
    }
  });

  /* Accordion display between menu parent items and their children. */ 
  $( ".cbp-spmenu-vertical-item-parent" ).click(function() {
    var elemId = $(this).attr('id');

    if(elemId == "dates"){
      elemId = $('.chart-type:checked').val() + "-" + elemId;
    }

    if ( $( ".cbp-spmenu-vertical-item-child#" + elemId ).is( ":hidden" ) ) {
      $( ".cbp-spmenu-vertical-item-child#" + elemId ).slideDown( "fast", function() {
        // Animation complete.
      });
    }else{
      $( ".cbp-spmenu-vertical-item-child#" + elemId ).slideUp( "fast", function() {
          // Animation complete.
      });
    }
  });

  /* Checkbox actions. */
  $('.services-types-checkbox').click(function() {
    console.log(this.value);
  });

  $('.chart-type').click(function() {
    if($(this).val() == "pie-chart"){
      if($(".cbp-spmenu-vertical-item-child.line-chart-dates").css('display') != 'none'){
        $(".cbp-spmenu-vertical-item-child.line-chart-dates").css('display', 'none');
      }

      if($(".cbp-spmenu-vertical-item-child.pie-chart-dates").css('display') == 'none'){
        $( ".cbp-spmenu-vertical-item-child.pie-chart-dates").slideDown( "fast", function() {
          // Animation complete.
        });
      }
    }else if ($(this).val() == "line-chart"){
      if($(".cbp-spmenu-vertical-item-child.pie-chart-dates").css('display') != 'none'){
        $(".cbp-spmenu-vertical-item-child.pie-chart-dates").css('display', 'none');
      }

      if($(".cbp-spmenu-vertical-item-child.line-chart-dates").css('display') == 'none'){
        $( ".cbp-spmenu-vertical-item-child.line-chart-dates").slideDown( "fast", function() {
          // Animation complete.
        });
      }
    }
  });

});