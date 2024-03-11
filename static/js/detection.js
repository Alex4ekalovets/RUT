let imageView = document.getElementById('imageView')
let imageLabel = document.getElementById('imageLabel')
let carousel = document.getElementById('carousel')
let dot = document.getElementById('dot')

let images = new Array()

document.getElementById('imageFile').onchange = async function () {
    let files = this.files;
    let formData = new FormData();

    for (let x = 0; x < files.length; x++) {
        formData.append("files", files[x]);
    }
    let response = await fetch('/detection/uploadfile', {method: "POST", body: formData});

    if (response.ok) {
        let response_data = await response.json()
        updateSlider(response_data.filenames)
    }
}

document.getElementById('detectFacesBtn').onclick = async function () {
    let data = {
        'filenames': images
    }
    let response = await postData('/detection/face_detection', data)
    if (response.ok) {
        let response_data = await response.json()
        updateSlider(response_data.filenames)
    }
}

function updateSlider (filenames) {
    images = new Array()
    carousel.innerHTML = ''
    dot.innerHTML = ''
    for (let i = 0; i < filenames.length; i++) {
        carousel.innerHTML += `
           <div class="mySlides">
            <div class="numbertext">${i} / ${filenames.length}</div>
            <img src="/detection/image/?name=${filenames[i]}" style="width:100%">
            <div class="text">${filenames[i]}</div>
           </div>
        `
        dot.innerHTML += `
            <span class="dot" onclick="currentSlide(${i})"></span>
        `
        images.push(filenames[i])
    }
    carousel.innerHTML += `
        <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
        <a class="next" onclick="plusSlides(1)">&#10095;</a>
    `
    showSlides(1);
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    return await response;
}


