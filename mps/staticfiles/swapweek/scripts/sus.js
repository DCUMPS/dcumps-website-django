window.addEventListener('load', () => {
    let jukebox = document.getElementById("🎶");

    document.getElementById("📀").addEventListener('click', function kill() {
        this.removeEventListener('click', kill);
        this.classList.toggle("🦴");
        jukebox.loop = false;
        jukebox.src = "/static/swapweek/assets/record.mp3";
        jukebox.play();
        jukebox.addEventListener('ended', function party() {
            this.removeEventListener('ended', party);
            document.getElementById("😵‍💫").classList.toggle("😁");
            document.getElementById("🔪").classList.toggle("hidden");
            document.querySelector('body').classList.toggle("🚨");
            jukebox.loop = true;
            jukebox.src = "/static/swapweek/assets/secret.mp3";
            jukebox.play();
            document.getElementById("📀").addEventListener('click', function revive() {
                this.removeEventListener('click', revive);
                this.classList.toggle("🦴");
                document.getElementById("😵‍💫").classList.toggle("😁");
                document.getElementById("🔪").classList.toggle("hidden");
                document.querySelector('body').classList.toggle("🚨");
                jukebox.src = "/static/swapweek/assets/classic.mp3";
                jukebox.play();
                this.addEventListener('click', kill);
            });
        });
    });
    console.info("👌");
});