window.onload = function () {
    let ss = document.querySelector(".ctr .start");
    ss.onclick = function () {
        if (ss.classList.contains("stop")) {
            ss.textContent = '开始';
            ss.classList.remove("stop")
            ss.classList.add("start")
        }
        else {
            ss.textContent = '停止';
            ss.classList.remove("start")
            ss.classList.add("stop")
        }
    }
}
