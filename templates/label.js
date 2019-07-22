function initialize(){
    let div = document.createElement('div');

    div.style.position = 'absolute';
    // div.style.top = window.innerHeight/8+'px';
    div.style.top = '13%';
    // div.style.left = window.innerWidth/4+'px';
    div.style.left = '25%';

    // div.style.height = window.innerHeight/2+'px';
    div.style.height = '50%';
    // div.style.width = window.innerWidth/2+'px';
    div.style.width = '50%';

    div.style.backgroundImage = "url(/static/Imgs/dragDrop.png)";
    div.class = "uploader";
    div.id = "plateImg";
    // div.style.height = window.innerHeight/2+'px';
    div.style.height = '50%';
    div.onclick = "$('#filePhoto').click()";
    div.style.backgroundRepeat = "no-repeat";
    div.style.backgroundSize = 'contain';
    div.addEventListener('change', readData, false);

    let imgLoader = document.createElement('INPUT');
    imgLoader.type = "file";
    imgLoader.id = "filePhoto";
    imgLoader.style.width = '100%';
    imgLoader.style.height = '100%';
    imgLoader.style.opacity = 0;
    div.appendChild(imgLoader);
    document.body.appendChild(div);
}

function printResult(text) {
    let div = document.getElementById('plateImg');
    div.innerText = text;
    div.style.backgroundImage = null;
}


function readData(e) {
    let reader = new FileReader();
    reader.readAsText(e.target.files[0]);
    reader.onloadend = function(){
        let text = reader.result;
        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/readData', true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        xhr.send(text);
        xhr.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                printResult(this.responseText);
            }
        };
    };
}