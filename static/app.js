$(document).ready(function () {
    hobby = $('.video').attr('data-hobby')

    testing = $(".hobbies-videos").children('div')
    console.log(testing)


    loadVids(testing);

    function loadVids(videosInfo) {
        // console.log(videosInfo)
        let key = 'AIzaSyANSe_cz96V28J240r95IxG7UgK9UUn6Ns';
        let secondkey = 'AIzaSyD6q5y-uYCaks7oXXKLa2nFDdZ4K4UnAM4';
        let URL = ' https://www.googleapis.com/youtube/v3/search';

        for(let i=0; i<videosInfo.length; i++){
            // console.log(videosInfo[i].className)
            let options = {
                part: 'snippet',
                type:'video',
                key: secondkey,
                maxResults: 2,
                q : "how to learn " + videosInfo[i].className
                }
            let hobbyName = videosInfo[i].className;
            
            $.getJSON(URL, options, function (data) {
                // console.log(data.items)
                id = data.items[0].id.videoId
                mainVid(data,hobbyName);
            });
        }
    }

    function mainVid(data,hobbyName) {
        $.each(data.items, function (i, item) {
            console.log(item)
            var title = item.snippet.title
            var description = item.snippet.description
            var id = item.id.videoId
            var thumb = item.snippet.thumbnails.medium.url

            $(`.${hobbyName}`).append(`
							<article class="item" data-key="${id}">

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

