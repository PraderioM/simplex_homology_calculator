function initialize() {
    document.addEventListener('keydown', function (event){
        getKeyDown(event);
    });
    initialize_data_upload();
}

function getKeyDown(event) {
    var key = event.key.toUpperCase();
    if (key === 'ENTER') {
        nextImg();
    }
}

function nextImg () {
    save_label(1);
    changeImage();
}

function prevImg () {
    save_label(-1);
    changeImage();
}

function save_label(direction) {
    var text = document.getElementById('plateText');
    LABELS[LAST_LABELED] = text.value;

    LAST_LABELED += direction;
    if (LAST_LABELED < LABEL_INIT) {
        if (LAST_LABELED < 0) {
            LAST_LABELED = 0;
        }
        LABEL_INIT = LAST_LABELED;
    }
    else if (LAST_LABELED >= LABELS.length) {
        LAST_LABELED = LABELS.length -1;
    }
    update_progress();
}

function changeImage() {
    var plateImg = document.getElementById('plateImg');
    plateImg.style.backgroundImage = "url(/static/Imgs/"+IMAGES[LAST_LABELED]+")";
    var text = document.getElementById('plateText');
    text.value = LABELS[LAST_LABELED];
}


function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    const form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(let key in params) {
        if(params.hasOwnProperty(key)) {
            let hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

function initialize_data_upload(){
    var div = document.createElement('div');

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

    var imgLoader = document.createElement('INPUT');
    imgLoader.type = "file";
    imgLoader.id = "filePhoto";
    imgLoader.style.width = '100%';
    imgLoader.style.height = '100%';
    imgLoader.style.opacity = 0;
    div.appendChild(imgLoader);
    document.body.appendChild(div);
}

function update_progress() {
    var progress = document.getElementById('progressBar');
    progress.innerHTML = '<center>' +
        'processades ' + (LAST_LABELED+1) + ' imatges de ' + LABELS.length +
        '</center>';

}


function readData(e) {
    var reader = new FileReader();
    reader.readAsText(e.target.files[0]);
    reader.onloadend = function(){
        var loaded = reader.result;
        var lines = loaded.split('\n').slice(0,-2);
        LAST_LABELED = parseInt(lines[0].split('=')[1]);
        LABEL_INIT = parseInt(lines[1].split('=')[1]);
        for (var i=2; i<lines.length; i++){
            var image = lines[i].split('file="')[1].split('"')[0].split("/");
            image = image[image.length-1];
            IMAGES[i-2] = image;
            LABELS[i-2] = lines[i].split('text="')[1].split('"')[0];
        }
        post();
    };
}