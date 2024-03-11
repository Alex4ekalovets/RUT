let imageView = document.getElementById('imageView')
let imageLabel = document.getElementById('imageLabel')
let width = document.getElementById('width')
let height = document.getElementById('height')
let x0 = document.getElementById('X0')
let x1 = document.getElementById('X1')
let y0 = document.getElementById('Y0')
let y1 = document.getElementById('Y1')
let rotate = document.getElementById('rotate')
let blur = document.getElementById('blur')
let gray = document.getElementById('gray')
let proportions = document.getElementById('proportions')
let red = document.getElementById('red')
let green = document.getElementById('green')
let blue = document.getElementById('blue')
let properties = document.querySelectorAll(".param")
let save_ratio_side = ''

let current_file = ''

document.getElementById('imageFile').onchange = async function () {
    let file = this.files[0];
    let formData = new FormData();

    formData.append("file", file);
    let response = await fetch('/image_tools/uploadfile', {method: "POST", body: formData});

    if (response.ok) {
        let data = await response.json()
        imageView.src = `/image_tools/image/?name=${data.filename}`
        imageLabel.innerHTML = `${data.filename}`
        width.value = Number(data.width)
        height.value = Number(data.height)
        x0.value = 0
        y0.value = 0
        x1.value = 0
        y1.value = 0
        blur.value = 0
        red.value = 0
        green.value = 0
        blue.value = 0
        rotate.value = 0
        current_file = data.filename
    }

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

properties.forEach(function (c) {
    c.onchange = async function () {

            let data = {
                "name": imageLabel.innerHTML,
                "resize": {
                    "height": Number(height.value),
                    "width": Number(width.value),
                    "save_ratio": false,
                    "side": save_ratio_side
                },
                "crop": {
                    "top": Number(y0.value),
                    "bottom": Number(y1.value),
                    "left": Number(x0.value),
                    "right": Number(x1.value)
                },
                "rotate": {
                    "angle": Number(rotate.value)
                },
                "blur": {
                    "blur": Number(blur.value)
                },
                "rgb": {
                    "red": Number(red.value),
                    "green": Number(green.value),
                    "blue": Number(blue.value),
                }
            }

            if (proportions.checked) {
                data.resize.save_ratio = true
                if (c.id == "width" || c.id == "height") {
                    data.resize.side = c.id
                    save_ratio_side = c.id
                }
            }

          let response = await postData("/image_tools/change", data)
          if (response.ok) {
            let json = await response.json()
            imageView.src = `/image_tools/image/?name=${json.filename}`
            current_file = json.filename
          }
    }
});

document.getElementById('saveImageBtn').onclick = function () {
    fetch(`/image_tools/save/?name=${current_file}`)
      .then( res => res.blob() )
      .then( blob => {
        var file = window.URL.createObjectURL(blob);
        window.location.assign(file);
      });
}
