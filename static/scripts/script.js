
function showPresentation(e) {
    screen.orientation.lock('landscape');
    var elem = document.getElementById("project-canvas");
    var p_editables=elem.getElementsByClassName('editable-box')
    document.getElementById('close_btn').style.visibility='visible'
    for (let p of p_editables) {
        p.setAttribute('contenteditable', false)
    };
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
      }
}

function closePresentation(e) {
    document.getElementById('close_btn').style.visibility='hidden'
    if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) { /* Firefox */
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { /* IE/Edge */
        document.msExitFullscreen();
      }
}

function zoom(zoom_in){
  var elem=document.getElementById("project-canvas");
  zoom_value=elem.style.transform
  console.log(zoom_value)
  if(zoom_in){
    elem.style.transform='scale(1)'
  }else{
    elem.style.transform='scale(0.9)'

  }
}

function seeCanvas(e,project){
    console.log(project)
}

function saveCanvas(){
    var data={}
    data.name= document.getElementById('project-name').textContent;
    data.title= document.getElementById('canvas-title').textContent;
    data.user= document.getElementById('project-user').textContent;
    created= document.getElementById('project-date').textContent;
    var boxes=document.getElementsByClassName('editable-box')
    var data_boxes=[]
    for (let box of boxes) {
        data_boxes.push({'box_text':box.textContent, 'box_ID':box.getAttribute('id')})        
    };
    data.boxes=data_boxes
    created=created.replace(/(\r\n|\n|\r| )/gm,"").trim()
    if(created==''){ //es un proyecto nuevo
        fetch("/canvas", {
            method: "POST", 
            body: JSON.stringify(data)
          }).then(res => {
            window.location="/user?user="+data.user
            return false
          });
    }else{ // es un proyecto editado
        id=document.getElementById('project_id').textContent
        fetch("/canvas?id="+id, {
            method: "PUT", 
            body: JSON.stringify(data)
        }).then(res => {
            window.location="/user?user="+data.user
            return false
        });
    }
}


function deleteCanvas(){
    user= document.getElementById('project-user').textContent;
    id=document.getElementById('project_id').textContent
    fetch("/canvas?id="+id+'&user='+user, {
        method: "DELETE"
    }).then(res => {
        window.location="/user?user="+user
        return false
    });
    
}