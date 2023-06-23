/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./static/js/home.js":
/*!***************************!*\
  !*** ./static/js/home.js ***!
  \***************************/
/***/ (() => {

eval("\r\n/* Set the width of the sidebar to 250px (show it) */\r\ndocument.getElementById(\"panel_board\").style.display=\"none\";\r\ndocument.getElementById(\"openbtn\").style.display=\"none\";\r\ndocument.getElementById(\"text\").style.display=\"none\";\r\ndocument.getElementById(\"plain_text_answer\").style.display=\"none\";\r\n\r\nfunction openNav() {\r\n    document.getElementById(\"mySidepanel\").style.width = \"250px\";\r\n    process = document.getElementById(\"process-div\");\r\n    if (window.getComputedStyle(process).display === \"none\"){\r\n        document.getElementById(\"panel_board\").style.display=\"block\";\r\n    }\r\n  }\r\n  \r\n  /* Set the width of the sidebar to 0 (hide it) */\r\n  function closeNav() {\r\n    document.getElementById(\"text\").style.display=\"none\";\r\n    document.getElementById(\"plain_text_answer\").style.display=\"none\";\r\n    document.getElementById(\"mySidepanel\").style.width = \"0\";\r\n  } \r\n\r\n  function openTextRequest() {\r\n    document.getElementById(\"panel_board\").style.display=\"none\";\r\n    document.getElementById(\"text\").style.display=\"block\";\r\n  }\r\n\r\n  function openCNBP(){\r\n    document.getElementById(\"gpt_answer_2\").innerHTML = \"Please wait for your answer to be generated.\";\r\n    document.getElementById(\"panel_board\").style.display=\"none\";\r\n    document.getElementById(\"plain_text_answer\").style.display=\"block\";\r\n  }\r\n\r\n\r\n\r\n\r\n\n\n//# sourceURL=webpack:///./static/js/home.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./static/js/home.js"]();
/******/ 	
/******/ })()
;