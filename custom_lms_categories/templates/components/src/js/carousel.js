document.addEventListener('DOMContentLoaded', function() {
     Video Modal Functions
    function openVideoModal(videoUrl) {
        let videoId = videoUrl;
        if (videoUrl.includes('youtube.com')  videoUrl.includes('youtu.be')) {
            videoId = extractYouTubeId(videoUrl);
            videoUrl = `httpswww.youtube.comembed${videoId}autoplay=1&mute=1&controls=1&rel=0`;
        } else if (videoUrl.includes('vimeo.com')) {
            videoId = extractVimeoId(videoUrl);
            videoUrl = `httpsplayer.vimeo.comvideo${videoId}autoplay=1&muted=1`;
        }
        
        document.getElementById('teaserVideoFrame').src = videoUrl;
        document.querySelector('.video-modal').classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeVideoModal() {
        document.getElementById('teaserVideoFrame').src = '';
        document.querySelector('.video-modal').classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    function extractYouTubeId(url) {
        const regExp = ^.(youtu.bevuwembedwatchv=&v=)([^#&]).;
        const match = url.match(regExp);
        return (match && match[2].length === 11)  match[2]  null;
    }

    function extractVimeoId(url) {
        const regExp = ^.(vimeo.com)((channels[A-z]+)(groups[A-z]+videos))([0-9]+);
        const match = url.match(regExp);
        return match  match[5]  null;
    }

     Event Listeners
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeVideoModal();
        }
    });

    document.querySelector('.close-btn').addEventListener('click', closeVideoModal);
    document.querySelector('.back-btn').addEventListener('click', () = history.back());

     Initialize Owl Carousels
    document.querySelectorAll('.owl-carousel').forEach(el = {
        $(el).owlCarousel({
            loop true,
            margin 20,
            nav true,
            responsive {
                0 { items 1 },
                768 { items 2 },
                1024 { items 3 }
            }
        });
    });

     Expose functions to global scope
    window.openVideoModal = openVideoModal;
    window.closeVideoModal = closeVideoModal;
});