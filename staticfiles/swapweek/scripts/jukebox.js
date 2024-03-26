window.addEventListener('load', () => {
    let jukebox = document.getElementById("🎶");

    jukebox.src = "/static/swapweek/assets/classic.mp3";
    jukebox.load();
    jukebox.currentTime = 15;
    this.addEventListener('click', function play() {
        this.removeEventListener('click', play);
        jukebox.play();
    });
    console.info("👌");
});