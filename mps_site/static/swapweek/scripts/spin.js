window.addEventListener('load', () => {
    document.querySelectorAll('.🌀').forEach((circlegraph) => {
        let circles = circlegraph.querySelectorAll('div');
        let angle = 360 - 90;
        let dangle = 360 / circles.length;
        for (let i = 0; i < circles.length; i++) {
            let circle = circles[i];
            angle += dangle;
            circle.style.transform = `rotate(${angle}deg) translate(${circlegraph.clientWidth / 2}px)`;
        }
    });
    console.info("👌");
});