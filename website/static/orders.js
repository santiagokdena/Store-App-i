let row;
let input_name;
let input_lab;
let input_id;
let product; //productordered

function uncomplete_fields(row){
  var forms=row.getElementsByTagName("form");
  if(forms == null){
    return true;
  }
  var uncomplete=false;
  for(var i=0;i<forms.length;i++){
    var input=forms[i].firstElementChild.firstElementChild;
      if(input.value==''){
        input.style.border="1px solid red";
        // Remove the flicker class after 2 seconds (adjust as needed)
        setTimeout(function(element) {
            element.style.border="";
        }, 2000,input);
        uncomplete=true;
      }
    }
  return uncomplete;
}

function del(e){
  e.preventDefault();
  const row=e.target.closest('tr');
  uncomplete_fields(row);
  // if(!uncomplete_fields(row)){

  // }
  var id=row.querySelector("input[placeholder='ID']").value;
  var name=row.querySelector("input[placeholder='NOMBRE DEL PRODUCTO']").value;
  if (confirm("Are you sure you want to delete '" + name + "'")){
    window.location.href = '/deleteregister/' + id;
  }
}

function addRow() {
  row=document.querySelector("tbody tr");
  if(row && uncomplete_fields(row)){
    alert("Debe completar los campos vacios");
  }
  else{
    var table = document.getElementById("Product").getElementsByTagName("tbody")[0];
    row = table.insertRow(-1);
    
    row.innerHTML=`
    <td>
      <form action="" autocomplete="off">
        <div class="autocomplete-wrapper">
          <input id="id" type="text" placeholder="ID" class="autocomplete-input" >
        </div>
      </form>    
    </td>
    <td>
      <form action="" autocomplete="off">
        <div class="autocomplete-wrapper">
            <input id="name" class="autocomplete-input" type="text" placeholder="NOMBRE DEL PRODUCTO">
        </div>
      </form>    
    </td>
    <td>
      <form action="" autocomplete="off">
        <div  class="autocomplete-wrapper">
          <input id="lab" class="autocomplete-input" type="text" placeholder="LABORATORIO">
        </div>
      </form>
    </td>
    <td>
      <form action="" autocomplete="off">
        <div class="autocomplete-wrapper">
          <input id="quant" pattern="\d+" placeholder="CANTIDAD" readonly onblur=onBlurQuant(event)>
        </div>
      </form>
    </td>
    <td>
      <form action="" autocomplete="off">
        <div>
          <input id="price" type="text" placeholder="PRECIO TOTAL" readonly>
        </div>
      </form>
    </td>
    <td>
      <div>
        <a href='#' class='btn btn-sm btn-danger' onclick='del(event)'><i class='fa-solid fa-trash'></i></a>
      </div>
    </td>
    <td>
      <div>
        <button type= class="btn btn-outline-success" onclick='save(event)'><i class="fa-solid fa-floppy-disk"></i></a>
      </div>
    </td>
    
    `;
    const inputEls = row.querySelectorAll(".autocomplete-input");
    inputEls.forEach((inputEl) => {
      inputEl.addEventListener("input", onInputChange);
      inputEl.addEventListener("blur",onBlur);
    });
    input_name=row.querySelector("td form div input#name");
    input_lab=row.querySelector("td form div input#lab");
    input_id=row.querySelector("td form div input#id");
  }
  }

async function onBlurQuant(event){
  console.log("onBlurQuant");
  const value=event.target.value;
  var pattern=/^\d+$/;
  if(!pattern.test(value) || value>product["quant"]){
  alert("Cantidad de producto inválida");
  value="";
  }
  else{
    console.log("PRECIO CALCUADO");
    var priceEl= row.querySelector("td div input#price");
    console.log(priceEl);
    priceEl.value=product["price"]*value;
    product["quant"]-=value;
  }
}

async function onBlur(event){
  var input = event.target;
  if(input.nextElementSibling){
    input.value="";
  }
}  

async function  onInputChange(e) {
  await fetch('/search', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json' // Configura el tipo de medio como JSON
      },
      body: JSON.stringify({"name":input_name.value,"lab":input_lab.value,"id":input_id.value}) // Convierte el objeto a JSON
  }).then(function (response) { //POST
      return response.json();
  }).then(function (data) { //GET 
    createAutocompleteDropdown(data["lab"],input_lab);
    createAutocompleteDropdown(data["name"],input_name);
    createAutocompleteDropdown(data["id"],input_id);
  }).catch(function (err) {
      console.warn('Something went wrong.', err);
  });
  var list=e.target.nextElementSibling;
  if(list){
    list.style.visibility="visible";
  }
}


function createAutocompleteDropdown(list,inputEl){
  removeAutocompleteDropdown(inputEl);
  const listEl=document.createElement("ul");
  const current_parent=inputEl.parentElement;
  listEl.className="autocomplete-list";
  if (list){
    list.forEach(element => {
      const listItem=document.createElement("li");
      const Button=document.createElement("button");
      Button.innerHTML=element;
      Button.addEventListener("click", function (e) {
        onButtonClick(e);
      });
      listItem.appendChild(Button);
      listEl.appendChild(listItem);
    }); 
    current_parent.appendChild(listEl);
  }
}

function removeAutocompleteDropdown(input){
  const listEl=input.nextElementSibling;
  if(listEl){
      listEl.remove();
  }

}

function onButtonClick(e){
  console.log("CLICK!!");
  e.preventDefault();
  const buttonEl=e.target;//target points to the element that triggers the element
  const inputEl=buttonEl.parentElement.parentElement.previousElementSibling;
  removeAutocompleteDropdown(inputEl);
  inputEl.value=buttonEl.innerHTML;
  if ((input_name.value!=""  && input_lab.value!="")|| (input_id.value!="" && input_name.value=="" && input_lab.value=="")){
    console.log("ADENTROO");
    fetch('/autocomplete', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json' // Configura el tipo de medio como JSON
      },
      body: JSON.stringify({"name":input_name.value,"lab":input_lab.value,"id":input_id.value} ) // Convierte el objeto a JSON
      }).then(function (response) { //POST
          return response.json();
      }).then(function (data) { //GET ss
        console.log(data);

        input_id.value=data["cb"];
        input_lab.value=data["lab"];
        input_name.value=data["name"];
        product=data;
        row.querySelector("td form div input#quant").readOnly=false;
      });
  }
  }

function save(){
  var elements= row.querySelectorAll("td form div input")
  if(!uncomplete_fields(row)){
    var list =[];
    console.log(elements);
    elements.forEach(element=>{
      element.readOnly=true;
    });
  }

}
function send(){
  fetch('/save', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json' // Configura el tipo de medio como JSON
    },
    body: JSON.stringify(product) // Convierte el objeto a JSON
    }).then(function (response) { //POST
        return response.json();
    });
}

