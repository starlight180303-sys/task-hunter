['difficulty','progress'].forEach(id=>{const i=document.getElementById(id),o=document.getElementById(id+'-output');if(i&&o){const u=()=>o.value=i.value;i.addEventListener('input',u);u();}});
