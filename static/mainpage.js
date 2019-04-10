$(document).ready(function () {
    hobby = $('.video').attr('data-hobby')

    testing = $(".hobbies-videos").children('div');
    
    $(".create_event_button").on('click', function(e){
        e.preventDefault();
        console.log('hi')
        let yout = $(this).parent().siblings("section")[0]
        $(this).parent().parent().find(`.${yout.className}`).hide()
        $(this).parent().parent().find('.user_events_by_hobbies').hide()
        $(this).parent().parent().find('.create_event').show()
    });

    $(".render_events_button").on('click', function(e){
        e.preventDefault();
        let yout = $(this).parent().siblings("section")[0].className
   
        $(this).parent().parent().find(`.${yout}`).hide()
        $(this).parent().parent().find('.create_event').hide()
        $(this).parent().parent().find('.user_events_by_hobbies').show()
    });

    $(".render_starter_videos").on('click', function(e){
        e.preventDefault();
        console.log('hi')
        let yout = $(this).parent().siblings("section")[0]
        if(yout.style.display === "none" && yout.childElementCount > 0 && yout.children[0].attributes.title.nodeName === "beginner"
        ){
            console.log("Find it")
            $(`.${yout.className}`).show()
        }else;{
            $(`.${yout.className}`).show()
            $(this).parent().parent().find('.create_event').hide()
            $(this).parent().parent().find('.user_events_by_hobbies').hide()
            let hobbyQuery = [`beginner videos on ${$(this).parent().parent()[0].className}`,"beginner"]
            loadVids(hobbyQuery,yout)
        }

    });

    $(".render_expert_videos").on('click', function(e){
        e.preventDefault();
        console.log('hi')
        let yout = $(this).parent().siblings("section")[0]
        
        if(yout.style.display === "none" && yout.childElementCount > 0 && yout.children[0].attributes.title.nodeName === "expert"
        ){
            console.log("Find it")
            $(`.${yout.className}`).show()
        }else;{
            $(`.${yout.className}`).show()
            $(this).parent().parent().find('.create_event').hide()
            $(this).parent().parent().find('.user_events_by_hobbies').hide()
            let hobbyQuery = [`expert videos on ${$(this).parent().parent()[0].className}`,"expert"]
            loadVids(hobbyQuery,yout)
        }

    });

    
    function loadVids(query,yout) {
        // console.log(videosInfo)
        let key = 'AIzaSyANSe_cz96V28J240r95IxG7UgK9UUn6Ns';
        let secondkey = 'AIzaSyD6q5y-uYCaks7oXXKLa2nFDdZ4K4UnAM4';
        let URL = ' https://www.googleapis.com/youtube/v3/search';

        console.log(yout)
        let options = {
                part: 'snippet',
                type:'video',
                key: secondkey,
                maxResults: 3,
                q : query[0]
                }
            
            
        $.getJSON(URL, options, function (data) {
                id = data.items[0].id.videoId
                mainVid(data,yout,query);
            });
    
    }


    function mainVid(data,yout,query) {

        $(`.${yout.className}`).empty()
        $.each(data.items, function (i, item) {
            console.log(item)
            var title = item.snippet.title
            var description = item.snippet.description
            var id = item.id.videoId
            var thumb = item.snippet.thumbnails.medium.url
            $(`.${yout.className}`).append(`
							<article class="item" data-key="${id}" title=${query[1]}>

                            <iframe width="560" height="315" src="https://www.youtube.com/embed/${id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
								<div class="details">
                                    <h4>${title}</h4>
                                    <p>${description}</p>
								</div>

							</article>
						`);

        })

    }

});

