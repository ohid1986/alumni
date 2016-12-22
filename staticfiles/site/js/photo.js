     $( function() {
        $( "#id_birth_date, #id_child_birth_date, #id_member_start_date, #id_member_end_date" ).attr("placeholder", "dd/mm/yyyy").datepicker({ dateFormat: 'dd/mm/yy',
                altFormat: 'yy-mm-dd'});

     });

    $(function() {
        $('.add-photo').click(function(ev){
            ev.preventDefault();
            var count = parseInt($('#id_gallery_set-TOTAL_FORMS').attr('value'), 10);
            var tmplMarkup = $('#gallery-template').html();
            var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count)
            console.log(compiledTmpl);
            $('div.gallery').append(compiledTmpl);
            $('#id_gallery_set-TOTAL_FORMS').attr('value', count + 1);

        });
    });


    $(document).ready(function () {
        document.getElementById('id_gallery_set-0-title').onchange = function() {
            var e = document.getElementById('id_gallery_set-0-slug');
            if (!e._changed) { e.value = URLify(document.getElementById('id_gallery_set-0-title').value, 50); }
            }
    });

    $(document).ready(function () {
                $('body').on('input','div[id^="gallery-"] input[id$="title"]',function() {
                    el = $(this).parent().find('> input[id$="slug"]');
                    el.val( URLify($(this).val(),50))
                 });
          });



   $(document).ready( function() {

        $("#mycarousel").carousel( { interval: 2000 } );
              $("#carousel-pause").click(function(){
            $("#mycarousel").carousel('pause');
        });

        $("#carousel-play").click(function(){
            $("#mycarousel").carousel('cycle');
        });



    });
