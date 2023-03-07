var formatsConfig = {
    "img": ["jpg", "jpeg", "png"],
    "html": ["html"],
    "table": ["csv"]
};

var viewType = "0";
var globalPaths = new Array();
var globalFrames = new Array();
var globalTotalProducts = 0;

let yVal = $('#y_select');
let zVal = $('#z_select');
let xVal=$('#x_select');

function createPanelsCarousel(totalPlots, frames, paths){

    let carouselId = createCarousel();
    let carouselContainer = document.getElementById(carouselId);
            
    let carouselItem = document.createElement('div');
    carouselItem.setAttribute('class','carousel-item active');

    let cardDiv = document.createElement('div');
    cardDiv.setAttribute('class', 'card card-primary');
    cardDiv.setAttribute('id', 'card_primary' + 0 + '-');
    carouselItem.appendChild(cardDiv);

    let cardBodyDiv = document.createElement('div');
    cardBodyDiv.setAttribute('class', 'card-body');
    cardBodyDiv.setAttribute('id', 'card_body');
    cardDiv.appendChild(cardBodyDiv);
            
    cardBodyDiv.appendChild(frames[0]);

    let inputElement = document.createElement('input');
    inputElement.setAttribute('class', 'zoom-center');
    inputElement.setAttribute('src', 'static/dist/img/zoom.png')
    inputElement.type = "image";

    inputElement.addEventListener('click', function () {
        event.preventDefault();
        clickHandler(paths[0]);
    });

    cardDiv.appendChild(inputElement);        
    carouselContainer.appendChild(carouselItem);
            
    for (let i = 1; i < totalPlots; i++) {
        let carouselItem = document.createElement('div');
        carouselItem.setAttribute('class','carousel-item');
        let cardDiv = document.createElement('div');
        cardDiv.setAttribute('class', 'card card-primary');
        cardDiv.setAttribute('id', 'card_primary' + i + '-');
        carouselItem.appendChild(cardDiv);
        let cardBodyDiv = document.createElement('div');
        cardBodyDiv.setAttribute('class', 'card-body');
        cardBodyDiv.setAttribute('id', 'card_body');
        cardDiv.appendChild(cardBodyDiv);
        cardBodyDiv.appendChild(frames[i]);     
        let inputElement = document.createElement('input');
         inputElement.setAttribute('class', 'zoom-center')
            inputElement.setAttribute('src', 'static/dist/img/zoom.png')
            inputElement.type = "image";
        cardDiv.appendChild(inputElement);

        inputElement.addEventListener('click', function () {
            event.preventDefault();
            clickHandler(paths[i]);
        });
        carouselContainer.appendChild(carouselItem);
    }
}
        
function createPanels(totalPlots, frames, paths) {        
    var plotsByRow = 2;
    var plotSize = 'col-sm-5';
    var framesWidth = "600";
    var framesHeight = "400";

    var canvasDiv = document.getElementById('canvas');
    canvasDiv.innerHTML = "";

    var totalRows = Math.floor(totalPlots / plotsByRow);
    var extraPlots = totalPlots % plotsByRow;

    var counter = 0;
    for (let i = 0; i < totalRows; i++) {
        let rowDiv = document.createElement('div');
        rowDiv.setAttribute('class', 'row')
        rowDiv.setAttribute('id', 'row' + i);
        canvasDiv.appendChild(rowDiv);
        
        for (let j = 0; j < plotsByRow; j++) {
            let colDiv = document.createElement('div');
            colDiv.setAttribute('class', plotSize)
            colDiv.setAttribute('id', 'col' + i + '-' + j);
            rowDiv.appendChild(colDiv);
            
            let cardDiv = document.createElement('div');
            cardDiv.setAttribute('class', 'card card-primary');
            cardDiv.setAttribute('id', 'card_primary' + i + '-' + j);
            colDiv.appendChild(cardDiv);
            
            let cardBodyDiv = document.createElement('div');
            cardBodyDiv.setAttribute('class', 'card-body');
            cardBodyDiv.setAttribute('id', 'card_body');
            cardDiv.appendChild(cardBodyDiv);
                    
            cardBodyDiv.appendChild(frames[counter]);

            let inputElement = document.createElement('input');
            inputElement.setAttribute('class', 'zoom')
            inputElement.setAttribute('src', 'static/dist/img/zoom.png')
            inputElement.type = "image";
            let src = paths[counter];
            inputElement.addEventListener('click', function () {
                event.preventDefault();
                clickHandler(src);
            });
            cardDiv.appendChild(inputElement);

            counter += 1;
        }
    }

    let rowDiv = document.createElement('div');
    rowDiv.setAttribute('class', 'row')
    rowDiv.setAttribute('id', 'row' + totalRows);
    canvasDiv.appendChild(rowDiv);
    for (let i = 0; i < extraPlots; i++) {
        let colDiv = document.createElement('div');
        colDiv.setAttribute('class', plotSize)
        colDiv.setAttribute('id', 'col' + totalRows + '-' + i);
        rowDiv.appendChild(colDiv);
                
        let cardDiv = document.createElement('div');
        cardDiv.setAttribute('class', 'card card-primary');
        cardDiv.setAttribute('id', 'card_primary' + totalRows + '-' + i);
        colDiv.appendChild(cardDiv);
                
        let cardBodyDiv = document.createElement('div');
        cardBodyDiv.setAttribute('class', 'card-body');
        cardBodyDiv.setAttribute('id', 'card_body');
        cardDiv.appendChild(cardBodyDiv);

        cardBodyDiv.appendChild(frames[counter]);

        let inputElement = document.createElement('input');
        inputElement.type = "button";
        let src = paths[counter];
        inputElement.addEventListener('click', function () {
            event.preventDefault();
            clickHandler(src);
        });
        cardDiv.appendChild(inputElement);

        counter += 1;
    }
}
function createCarousel() {

    let canvas = document.getElementById('canvas');
    canvas.innerHTML = '';
    //<div id="carouselExampleControls" class="carousel slide" data-ride="carousel" style="width: 700px; margin: 0 auto">
    let carousel = document.createElement('div');
    carousel.setAttribute('id', 'carouselExampleControls');
    carousel.setAttribute('class','carousel slide');
    carousel.setAttribute('data-ride', 'carousel');
    carousel.setAttribute('style', 'width: 700px; margin: 0 auto');

        //<div class="carousel-inner" id="carouselContainer">
    let carouselContainerId = 'carouselContainer';
    let carouselContainer = document.createElement('div');
    carouselContainer.setAttribute('class', 'carousel-inner');
    carouselContainer.setAttribute('id', carouselContainerId);

    /*<a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="sr-only" style="color:black">Previous</span>
    </a>*/

    let prevArrow = document.createElement('a');
    prevArrow.setAttribute('class', 'carousel-control-prev');
    prevArrow.setAttribute('href','#carouselExampleControls');
    prevArrow.setAttribute('role', 'button');
    prevArrow.setAttribute('data-slide', 'prev');
    let prevArrowSpan1 = document.createElement('span');
    prevArrowSpan1.setAttribute('class', 'carousel-control-prev-icon');
    prevArrowSpan1.setAttribute('aria-hidden', 'true');
    prevArrow.appendChild(prevArrowSpan1);
    let prevArrowSpan2 = document.createElement('span');
    prevArrowSpan2.setAttribute('class', 'sr-only');
    prevArrow.appendChild(prevArrowSpan2);


    /*<a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
    </a>*/

    let nextArrow = document.createElement('a');
    nextArrow.setAttribute('class', 'carousel-control-next');
    nextArrow.setAttribute('href','#carouselExampleControls');
    nextArrow.setAttribute('role', 'button');
    nextArrow.setAttribute('data-slide', 'next');
    let nextArrowSpan1 = document.createElement('span');
    nextArrowSpan1.setAttribute('class', 'carousel-control-next-icon');
    nextArrowSpan1.setAttribute('aria-hidden', 'true');
    nextArrow.appendChild(nextArrowSpan1);
    let nextArrowSpan2 = document.createElement('span');
    nextArrowSpan2.setAttribute('class', 'sr-only');
    nextArrow.appendChild(nextArrowSpan2);

    carousel.appendChild(carouselContainer);
    carousel.appendChild(prevArrow);
    carousel.appendChild(nextArrow);

    canvas.appendChild(carousel);

    return carouselContainerId;
} 

function centrar(elem,posy){ 
    var posicion;
    if(posy==0){
        posicion=60;
    }else{
        posicion=posy;
    }
    elem.style.top=posicion + 'px'
    
}

function clickHandler(path) {
    let divModal = document.getElementById('modal');
    divModal.style.display="block";
    divModal.innerHTML = "";
    
    let divCerrar = document.createElement('div');
    divCerrar.setAttribute('class', 'modal-close');
    
    let iconCerrar= document.createElement('img');
    iconCerrar.setAttribute('src', 'static/dist/img/cerrar.png')
    divCerrar.appendChild(iconCerrar);

    divModal.appendChild(divCerrar);

    divCerrar.addEventListener('click',function(){
        event.preventDefault();
        closeModal();
    });

    let divContent=document.createElement('div');
    divContent.setAttribute('class','modal-content');

    let frame=document.createElement('iframe');
    frame.setAttribute('src',path);

    divContent.appendChild(frame);
    divModal.appendChild(divContent);
    var y = window.scrollY;
    console.log("posicion del scroll",y);
    $("html, body").css("overflow","hidden");
    centrar(divModal,y);
}

function closeModal(){
    let divModal = document.getElementById('modal');
    divModal.style.display="none";
    $("html, body").css("overflow","scroll");
}
        
$(document).ready(function () {
    $('#x_select').on('change', function () {
        xVal=this;
        panelStatus(xVal,yVal,zVal);
    });

    $('#y_select').on('change', function () {
        yVal=this;
        panelStatus(xVal,yVal,zVal);
    });

    $('#z_select').on('change', function () {
        zVal=this;
        panelStatus(xVal,yVal,zVal);
    });

});

function panelStatus(valX,valY,valZ){
    let paths = new Array();
    let path;
    if(valX.value!=0&&valX.value!=undefined&&(valY.value==0||valY.value==undefined)){
        console.log('entro en x');
        path = "1-LVL-" + valX.name + "=" + valX.value + "-subtask-c3-regression_serv";
        paths.push(path);
        path = "1-LVL-" + valX.name + "=" + valX.value + "-subtask-c5-charts-sv";
        paths.push(path);
        path = "1-LVL-" + valX.name + "=" + valX.value + "-subtask-c8-maps";
        paths.push(path);
        path = "1-LVL-" + valX.name + "=" + valX.value + "-subtask-c10-DST";
        paths.push(path);
        path = "1-LVL-" + valX.name + "=" + valX.value + "-MAP-c1-data-catalogs";
        getJSON(1, valX.value);
    }
    if(valY.value!=undefined && valY.value!=0&&(valX.value!=0||valX.value!=undefined)){
        console.log('entro en y');
        path = "2-LVL-" + valX.name + "=" + valX.value + "_" + valY.name + "=" + valY.value + '-subtask-c3-regression_serv';
        paths.push(path);
        getJSON(2, valY.value);
    }
    if(valZ!=0 && valZ.value!=undefined&&(valX!=0 && valX.value!=undefined)&&(valY!=0 && valY.value!=undefined)){
        console.log('entro en z');
        path = "3-LVL-" + valX.name + "=" + valX.value + "_"+valY.name + "=" + valY.value +"_" + valZ.name + "=" + valZ.value + '-subtask-c9-charts-sv';
        paths.push(path);
    }
    get_panels(paths);
}

function loadingScreen(){
    let canvas = document.getElementById('canvas');
    canvas.innerHTML = '';
    let spinnerDiv = document.createElement('div');
    spinnerDiv.setAttribute('class', 'spinner-border');
    spinnerDiv.setAttribute('role', 'stauts');

    let spinnerSpan = document.createElement('span');
    spinnerSpan.setAttribute('class', 'sr-only')
    spinnerSpan.innerHTML = "Cargando...";

    spinnerDiv.appendChild(spinnerSpan);
    canvas.appendChild(spinnerDiv);

}

function get_panels(paths) {            
    loadingScreen();
    $.ajax({
        url: "/get_panels",
        type: "GET",
        data: {
            "paths": paths
        },
        success: function (response) {
        console.log(response);
        globalTotalProducts = response['total_files'];

                    if (globalTotalProducts > 0) {
                        globalPaths = response['paths'];
                        globalFrames = createFrames(globalTotalProducts, globalPaths);
                        if (viewType == "0") {
                            createPanels(globalTotalProducts, globalFrames, globalPaths);

                        }
                        else {
                            createPanelsCarousel(globalTotalProducts, globalFrames, globalPaths);
                        }

                    } else {
                        let canvas = document.getElementById('canvas');
                        canvas.innerHTML = '';
                    }

                },
                error: function (error) {
                    console.log(error);
                    let canvas = document.getElementById('canvas');
                    canvas.innerHTML = '';
                },
            });
}
function get_all_panels() {            
    loadingScreen();
    $.ajax({
        url: "/get_all_panels",
        type: "GET",
        success: function (response) {
            console.log(response);
            globalTotalProducts = response['total_files'];
        
            if (globalTotalProducts > 0) {
                globalPaths = response['paths'];
                globalFrames = createFrames(globalTotalProducts, globalPaths);
                if (viewType == "0") {
                    createPanels(globalTotalProducts, globalFrames, globalPaths);        
                }else {
                    createPanelsCarousel(globalTotalProducts, globalFrames, globalPaths);
                }        
            } else {
                let canvas = document.getElementById('canvas');
                canvas.innerHTML = '';
            }
        },
        error: function (error) {
            console.log(error);
            let canvas = document.getElementById('canvas');
            canvas.innerHTML = '';
        },
    });
}

function getExtension(filename) {
    let filenamePieces = filename.split(".");
    return filenamePieces[filenamePieces.length - 1]
}

function getJSON(level, label) {
    $.ajax({
        url: "/get_json",
        type: "GET",
        data: {
            "level": level,
            "label": label
        },
        success: function (response) {
            console.log(response);
            if (level == 1) {
                $.each(response, function (index, value) {
                    $('#y_select').append($('<option>').val(value).text(value));
                });
            } else {
                $.each(response, function (index, value) {
                    $('#z_select').append($('<option>').val(value).text(value));
                });
            }
        },
        error: function (error) {
            console.log(error);
        },
    });
}

function createFrames(totalFiles, paths) {
    var frames = new Array();
    for (let i = 0; i < totalFiles; i++) { 
        let src = paths[i];
        let extension = getExtension(src);
        let elementName;
        for (const [key, value] of Object.entries(formatsConfig)) {
            if (value.includes(extension)) {
                elementName = key
            }
        }
        if (elementName == "img") {
            let img = document.createElement('img');
            img.setAttribute('src', src);
            img.setAttribute('style', 'height: 100%; width: 100%; object-fit: contain');
            img.setAttribute('alt', 'Imagen ' + i);
            frames.push(img);
        } else if (elementName == "html") {
            let frame = document.createElement('iframe');
            frame.setAttribute('src', src);
            frame.setAttribute('id', 'scaled-frame');
            frames.push(frame);
        } else if (elementName == "table"){
            let table = document.createElement('table');
            table.setAttribute('class','table table-striped table-bordered table-sm');            
            let frame = document.createElement('div');
            frame.setAttribute('style','overflow:scroll; height:100%;')
            //frame.setAttribute('src', src);
            //frame.setAttribute('id', 'scaled-frame');
            fetch(src)
            .then(res => res.text())
            .then(csv => {
                table.innerHTML = "";
                for (let row of CSV.parse(csv)) {
                    let tr = table.insertRow();
                    for (let col of row) {
                        let td = tr.insertCell();
                        td.innerHTML = col;
                    }
                }
                frame.appendChild(table);            
                            
            });
            frames.push(frame);
        }
    }
    return frames;
}

function readCSV(path) {
    alert("LEERE CSV");
    alert(path);
    fetch(path)
        .then(res => res.text())
        .then(csv => {
            alert(csv)
            table.innerHTML = "";
            for (let row of CSV.parse(csv)) {
                    let tr = table.insertRow();
                    for (let col of row) {
                        let td = tr.insertCell();
                        td.innerHTML = col;
                    }
                }
        });
}
