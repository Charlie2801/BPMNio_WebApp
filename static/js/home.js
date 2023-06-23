
/* Set the width of the sidebar to 250px (show it) */
document.getElementById("panel_board").style.display="none";
document.getElementById("openbtn").style.display="none";
document.getElementById("text").style.display="none";
document.getElementById("context").style.display="none";
document.getElementById("plain_text_answer").style.display="none";
document.getElementById("suggestion_panel").style.display="none";

function openNav() {
    document.getElementById("mySidepanel").style.width = "150px";
    document.getElementById("suggestion_panel").style.display="block";
    document.getElementById("panel_board").style.display="block";
  }
  
  /* Set the width of the sidebar to 0 (hide it) */
  function closeNav() {
    document.getElementById("text").style.display="none";
    document.getElementById("plain_text_answer").style.display="none";
    document.getElementById("mySidepanel").style.width = "0";
    document.getElementById("suggestion_panel").style.display="none";
  } 

  function openTextRequest() {
    //document.getElementById("panel_board").style.display="none";
    if(document.getElementById("text").style.display=="block"){
      document.getElementById("text").style.display="none";
    }
    else{
      document.getElementById("text").style.display="block";     
    }
  }

  function openContextCard() {
    //document.getElementById("panel_board").style.display="none";
    if(document.getElementById("context").style.display=="block"){
      document.getElementById("context").style.display="none";
    }
    else{
      document.getElementById("context").style.display="block";     
    }
  }

  function openCNBP(){
    document.getElementById("gpt_answer_2").innerHTML = "Please wait for your answer to be generated.";
    document.getElementById("panel_board").style.display="none";
    document.getElementById("plain_text_answer").style.display="block";
  }

  function closeMessage(){
    document.getElementById("text").style.display="none";
  }




