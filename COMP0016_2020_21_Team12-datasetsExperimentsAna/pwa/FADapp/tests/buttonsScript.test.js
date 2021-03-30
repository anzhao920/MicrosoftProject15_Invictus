
const buttonsScript = require("../public/javascripts/buttonsScript.js");

test("Returns correct searching element", () => {
    var searchList = ['location', 'country', 'depthVsTemp', 'DepthVsSalinity'];
    for (var i = 0; i < 4; i ++) {
        expect(buttonsScript.setSearchElements(searchList[i])).toEqual([searchList[i]]);
        expect(buttonsScript.setSearchElements(searchList[i])).toEqual([]);
    }
    
});

test("Returns correct searching result page with search items", () => {
    const jsdomAlert = window.alert;
    window.alert = () => {};

    let assignMock = jest.fn();
    delete window.location;
    window.location = { assign: assignMock };
    afterEach(() => {
        assignMock.mockClear();
    });

    for (var i = 0; i < 2; i++) {
        for (var j = 0; j < 2; j++) {
            for (var k = 0; k < 2; k++) {
                for (var l = 0; l < 2; l++) {
                    var searchList = [];
                    if (i == 0 && j == 0 && k == 0 && l == 0) {       
                        expect(buttonsScript.getSearchElements(1)).toEqual("Please select searching element(s)");
                        expect(buttonsScript.getSearchElements(2)).toEqual("Please select searching element(s)");
                    } else {
                        if (i == 1) {
                            buttonsScript.setSearchElements('location');
                            searchList.push('location');
                        }
                        if (j == 1) {
                            buttonsScript.setSearchElements('country');
                            searchList.push('country');
                        }
                        if (k == 1) {
                            buttonsScript.setSearchElements('depthVsTemp');
                            searchList.push('depthVsTemp');
                        }
                        if (l == 1) {
                            buttonsScript.setSearchElements('DepthVsSalinity');
                            searchList.push('DepthVsSalinity');
                        }
                        expect(buttonsScript.getSearchElements(1)).toEqual("FADDataTableView.html?" + searchList);
                        expect(buttonsScript.getSearchElements(2)).toEqual("FADDataGraphView.html?" + searchList);
                        if (i == 1) {
                            buttonsScript.setSearchElements('location');
                        }
                        if (j == 1) {
                            buttonsScript.setSearchElements('country');
                        }
                        if (k == 1) {
                            buttonsScript.setSearchElements('depthVsTemp');
                        }
                        if (l == 1) {
                            buttonsScript.setSearchElements('DepthVsSalinity');
                        }
                    }
                }
            }
        }
    }
    window.alert = jsdomAlert;
});

