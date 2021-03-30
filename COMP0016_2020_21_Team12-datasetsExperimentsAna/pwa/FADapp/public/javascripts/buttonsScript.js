
var searchElements = [];

Array.prototype.remove = function(value) {
  var index = this.indexOf(value);
  if (index > -1) {
    this.splice(index, 1);
  }
};

function setSearchElements(itemToSearch) {
  if (searchElements.includes(itemToSearch)) {
    searchElements.remove(itemToSearch);
  } else {
    searchElements.push(itemToSearch);
  }
  return(searchElements);
}

function getSearchElements(type) {
  if (searchElements.length == 0) {
    alert("Please select searching element(s)");
    return "Please select searching element(s)";
  } else {
    if (type == 1) {
      window.location.assign("FADDataTableView.html?" + searchElements);
      return("FADDataTableView.html?" + searchElements);
    } else if (type == 2) {
      window.location.assign("FADDataGraphView.html?" + searchElements);
      return("FADDataGraphView.html?" + searchElements);
    }
  }
}


module.exports.setSearchElements = setSearchElements;
module.exports.getSearchElements = getSearchElements;
