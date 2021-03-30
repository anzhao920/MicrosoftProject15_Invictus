
function _export() {
  body = window.document.body.innerHTML;
  startpoint= "<!-- export startpoint -->";
  endpoint= "<!-- export endpoint -->";
  printdb= body.substring(body.indexOf(startpoint) + 26); 
  printdb = printdb.substring(0, printdb.indexOf(endpoint));
  window.document.body.innerHTML = printdb ;
  window.print();
  window.document.body.innerHTML = body ;
}

async function getFADData(searchID) {
  var FADDataUrl;
  if (searchID == undefined) {
    FADDataUrl = '/API/AllFADs';
  } else {
    FADDataUrl = `/API/FAD/${searchID}`;
  }
  var dataPromise = fetch(FADDataUrl).then(response => response.text());
  return dataPromise;
}

function addNewTitle(name) {
  var newTitle = document.createElement("th");
  newTitle.scope = "col";
  newTitle.innerHTML = name;
  return newTitle;
}
