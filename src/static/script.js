const progressBar = document.querySelector('.scrollbar');

let totalHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;

window.addEventListener('scroll', () =>  {
    let progress = (document.documentElement.scrollTop / totalHeight) * 100;
    progressBar.style.height = `${progress}%`;
    progressBar.style.opacity = `${progress}%`;
})

const progressBarClick = document.querySelector('.clickScrollbar');
progressBarClick.addEventListener('click', (e) => {

    let newPageScroll = e.clientY / progressBarClick.offsetHeight * totalHeight;
    window.scrollTo({
        top: newPageScroll,
        behavior: 'smooth'
    })

})

const lateralNav = document.querySelector('.lateral-nav');
window.addEventListener('scroll', () => {

    const {scrollTop} = document.documentElement;

    if (scrollTop > 270) {
        lateralNav.style.display = "block";
    } else {
        lateralNav.style.display = "none";
    }
})