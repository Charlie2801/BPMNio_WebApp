import $, { event } from 'jquery';

import BpmnModeler from 'bpmn-js/lib/Modeler';

import diagramXML from 'raw-loader!../resources/newDiagram.bpmn';
import { is } from 'bpmn-js/lib/util/ModelUtil';

var container = $('#js-drop-zone');

var modeler = new BpmnModeler({
  container: '#js-canvas',
  keyboard: {
    bindTo: window
  }
});

function createNewDiagram() {
  openDiagram(diagramXML);
  document.getElementById("openbtn").style.display="block";
}

async function openDiagram(xml) {

  try {

    await modeler.importXML(xml);

    container
      .removeClass('with-error')
      .addClass('with-diagram');
  } catch (err) {

    container
      .removeClass('with-diagram')
      .addClass('with-error');

    container.find('.error pre').text(err.message);

    console.error(err);
  }
}

function registerFileDrop(container, callback) {

  function handleFileSelect(e) {
    e.stopPropagation();
    e.preventDefault();

    var files = e.dataTransfer.files;

    var file = files[0];

    var reader = new FileReader();

    reader.onload = function(e) {

      var xml = e.target.result;

      callback(xml);
    };

    reader.readAsText(file);
  }

  function handleDragOver(e) {
    e.stopPropagation();
    e.preventDefault();

    e.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
  }

  container.get(0).addEventListener('dragover', handleDragOver, false);
  container.get(0).addEventListener('drop', handleFileSelect, false);
}

function makeRequest() {
    console.log("hi");
}


// file drag / drop ///////////////////////

// check file api availability
if (!window.FileList || !window.FileReader) {
  window.alert(
    'Looks like you use an older browser that does not support drag and drop. ' +
    'Try using Chrome, Firefox or the Internet Explorer > 10.');
} else {
  registerFileDrop(container, openDiagram);
}

// bootstrap diagram functions

$(function() {


  $('#js-create-diagram').click(function(e) {
    e.stopPropagation();
    e.preventDefault();

    createNewDiagram();
  });

  var downloadLink = $('#js-download-diagram');
  var downloadSvgLink = $('#js-download-svg');

  $('.buttons a').click(function(e) {
    if (!$(this).is('.active')) {
      e.preventDefault();
      e.stopPropagation();
    }
  });

  function setEncoded(link, name, data) {
    var encodedData = encodeURIComponent(data);

    if (data) {
      link.addClass('active').attr({
        'href': 'data:application/bpmn20-xml;charset=UTF-8,' + encodedData,
        'download': name
      });
    } else {
      link.removeClass('active');
    }
  }

  var exportArtifacts = debounce(async function() {

    try {

      const { svg } = await modeler.saveSVG();

      setEncoded(downloadSvgLink, 'diagram.svg', svg);
    } catch (err) {

      console.error('Error happened saving svg: ', err);
      setEncoded(downloadSvgLink, 'diagram.svg', null);
    }

    try {

      const { xml } = await modeler.saveXML({ format: true });
      setEncoded(downloadLink, 'diagram.bpmn', xml);
    } catch (err) {

      console.error('Error happened saving XML: ', err);
      setEncoded(downloadLink, 'diagram.bpmn', null);
    }
  }, 500);

  modeler.on('commandStack.changed', exportArtifacts);
});



// helpers //////////////////////

function debounce(fn, timeout) {

  var timer;

  return function() {
    if (timer) {
      clearTimeout(timer);
    }

    timer = setTimeout(fn, timeout);
  };
}


//Event Listener Request Form
/*
const request_form = document.getElementById('text');
request_form.addEventListener('submit', function (event) {
  event.preventDefault();
  const txt = request_form.text_field.value;
  modeler.saveXML({ format: true }, function (err, xml) {
    $.ajax({
      type: 'POST',
      url: '/gpt_request',
      data: {txt: txt, model:xml}
    }).done(function(response){
      document.getElementById("gpt_answer").innerHTML = response;
  
    });
  });
});
*/


// Label Suggestions
const label_button = document.getElementById('labels_button');
label_button.addEventListener('click', function (event) {
  event.preventDefault();
  let product;
  document.getElementById("wait").style.display="block";

  modeler.saveXML({ format: true }, function (err, xml) {
    try {
      $.ajax({
        type: 'POST',
        url: '/label_suggestion',
        data: {model:xml}
      }).done(function(response){
        product = response;
  
        var table = document.getElementById('labels');
        table.getElementsByTagName("tbody")[0].innerHTML = table.rows[1].innerHTML;
  
        console.log(product)
  
        for(let i = 0; i < product.length; i++){
          var row = table.insertRow(-1);
          var cell_old = row.insertCell(0);
          var cell_new = row.insertCell(1);
          cell_old.innerHTML = product[i][1];
          cell_new.innerHTML = product[i][0];
        };
  
        document.getElementById("inconsistency_field").style.display="none";
        document.getElementById("label_suggestion").style.display="block";
        document.getElementById("noAssociation").style.display="none";
        document.getElementById("wait").style.display="none";
    
      });
    }

    catch {
      document.getElementById("inconsistency_field").style.display="none";
      document.getElementById("label_suggestion").style.display="block";
      document.getElementById("noAssociation").style.display="none";
      document.getElementById("wait").style.display="none";

      alert("GPT Request Error: Request could not be handled");
    }

  });
});



  //Best Practices 7PMG
/*
  const pmg = document.getElementById('7PMG');
  pmg.addEventListener('click', function (event) {
    event.preventDefault();
    let product;

    addUserChat("Does the Business Process Model adhere to the 7PMG?");
    addPendingAnimation();

    modeler.saveXML({ format: true }, function (err, xml) {
      $.ajax({
        type: 'POST',
        url: '/best_practices',
        data: {model:xml}
      }).done(function(response){
        document.getElementById("pending").remove();
        product = response;
        addBotChat(product);
    
      });
    });
  });

*/
/*

const predict_form = document.getElementById("predict_next");
predict_form.addEventListener('click', function (event) {
  event.preventDefault();
  modeler.saveXML({ format: true }, function (err, xml) {
    $.ajax({
      type: 'POST',
      url: '/predict_next',
      data: {model:xml}
    }).done(async function(response){
      try{
        await modeler.importXML(response);
      } catch{
        document.getElementById("gpt_answer_2").innerHTML = "No successful response: \n" + response;
      }
      

    });
  });
});

*/


// Best Practices: 7PMG


//context form
const context_send = document.getElementById("send_context");
context_send.addEventListener('click', function (event) {
  event.preventDefault();
  document.getElementById("wait").style.display="block";

  const pname = document.getElementById("process_name").value;
  const desc = document.getElementById("description").value;
  console.log(desc);
  document.getElementById("context").style.display="none";

  $.ajax({
    type: 'POST',
    url: '/context',
    data: {name: pname, desc:desc}
  }).done(async function(response){
    try{
      console.log(response)
      if(response!= "200"){
        document.getElementById("noText").innerHTML =  response[0];

        // add associations to table 
        var associations = response[4];
        console.log(response)
        var table = document.getElementById('activities');
        table.getElementsByTagName("tbody")[0].innerHTML = table.rows[1].innerHTML;

        for(let i = 0; i < associations.length; i++){
          var row = table.insertRow(-1);
          var cell_performer = row.insertCell(0);
          var cell_activity = row.insertCell(1);
          cell_performer.innerHTML = associations[i][0];
          cell_activity.innerHTML = associations[i][1];
        };
        document.getElementById("inconsistency_field").style.display="none";
        document.getElementById("label_suggestion").style.display="none";
        document.getElementById("noAssociation").style.display="block";
        document.getElementById("suggestion_buttons").style.display="block";
        document.getElementById("wait").style.display="none";

        //document.getElementById("noAssociation").innerHTML =  response[3];
      }

    } catch{
      document.getElementById("noText").innerHTML = "No successful response: \n" + response;
      document.getElementById("wait").style.display="none";
    };
  });

});

//Inconsistency checking
const inconsistencies = document.getElementById("inconsistencies");
inconsistencies.addEventListener('click', function (event) {
  event.preventDefault();
  document.getElementById("wait").style.display="block";

  modeler.saveXML({ format: true }, function (err, xml) {
    try{ $.ajax({
      type: 'POST',
      url: '/inconsistencies',
      data: {model:xml}
    }).done(async function(response){
        document.getElementById("inconsistency_field").innerHTML = response;
        document.getElementById("inconsistency_field").style.display="block";
        document.getElementById("noAssociation").style.display="none";
        document.getElementById("label_suggestion").style.display="none";
        document.getElementById("wait").style.display="none";
      
    });
  } catch{
    document.getElementById("inconsistency_field").innerHTML = "No successful response: \n" + response;
    document.getElementById("wait").style.display="none";
  }

});
});

//Unsolved Questions
const quest = document.getElementById("questions");
quest.addEventListener('click', function (event) {
  event.preventDefault();
  providedPrompts(0);
});

// Ways of Automization 
const auto = document.getElementById("auto");
auto.addEventListener('click', function (event) {
  event.preventDefault();
  providedPrompts(1);
});

// Ways of Enhancement
const enhance = document.getElementById("enhance");
enhance.addEventListener('click', function (event) {
  event.preventDefault();
  providedPrompts(2);
});

// weaknesses
const weak = document.getElementById("weaknesses");
weak.addEventListener('click', function (event) {
  event.preventDefault();
  providedPrompts(3);
});


function providedPrompts(index){
  var prompts = [
    "What questions does the process raise that remain unanswered? Provide a enumeration",
    "Which process tasks can be automated? How can this automation be implemented?",
    "Provide possibilites to enhance the process.",
    "Does the process currently display any weaknesses? Provide a enumeration"
  ];

  var input = prompts[index];
  input != "" && output(input);
}

//chatbot
const label = document.getElementById("sendMessage");
label.addEventListener('click', function (event) {
  event.preventDefault();
  const inputField = document.getElementById("input");
  let input = inputField.value.trim();
  input != "" && output(input);
  inputField.value = "";

});



document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("input");
  inputField.addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
      let input = inputField.value.trim();
      input != "" && output(input);
      inputField.value = "";
    }
  });
});



function output(input) {
  let product;
  var data; 
  addUserChat(input);
  addPendingAnimation();

  modeler.saveXML({ format: true }, function (err, xml) {
    try{
      $.ajax({
        type: 'POST',
        url: '/gpt_request',
        data: {txt: input, model:xml}
      }).done(function(response){
        product = response;
        document.getElementById("pending").remove();
        product = formatHTMLOutput(product);
        console.log(product);
        addBotChat(product);
    
      });
    }

    catch{
      document.getElementById("pending").remove();
      addBotChat("GPT Request Error: Request could not be handled.");
    }

  });

}

function formatHTMLOutput(product){
  product = product.replace(/- /g, "<br>-");
  product = product.replace(/0/g, "<br>0");
  product = product.replace(/1/g, "<br>1");
  product = product.replace(/2/g, "<br>2");
  product = product.replace(/3/g, "<br>3");
  product = product.replace(/4/g, "<br>4");
  product = product.replace(/5/g, "<br>5");
  product = product.replace(/6/g, "<br>6");
  product = product.replace(/7/g, "<br>7");
  product = product.replace(/8/g, "<br>8");
  product = product.replace(/9/g, "<br>9");

  return product


}

function addUserChat(input){
  const mainDiv = document.getElementById("message-section");
  let userDiv = document.createElement("div");
  userDiv.id = "user";
  userDiv.classList.add("message");
  userDiv.innerHTML = `<span id="user-response">${input}</span>`;
  mainDiv.appendChild(userDiv);
  var scroll = document.getElementById("message-section");
  scroll.scrollTop = scroll.scrollHeight;
}

function addBotChat(product) {
  const mainDiv = document.getElementById("message-section");
  let botDiv = document.createElement("div");
  botDiv.id = "bot";
  botDiv.classList.add("message");
  botDiv.innerHTML = `<span id="bot-response">${product}</span>`;
  mainDiv.appendChild(botDiv);
  var scroll = document.getElementById("message-section");
  scroll.scrollTop = scroll.scrollHeight;
}

function addPendingAnimation(){
  const mainDiv = document.getElementById("message-section");
  let botDiv = document.createElement("div");
  botDiv.id = "pending";
  botDiv.classList.add("message");
  botDiv.innerHTML = `<span id="bot-pending"><div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div></span>`;
  mainDiv.appendChild(botDiv);
  var scroll = document.getElementById("message-section");
  scroll.scrollTop = scroll.scrollHeight;
}








  