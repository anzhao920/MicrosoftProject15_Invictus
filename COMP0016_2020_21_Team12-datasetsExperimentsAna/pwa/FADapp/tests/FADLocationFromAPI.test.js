const FADLocations = require("../public/javascripts/FADLocationFromAPI.js");

test("Returns the stroke options for visible stroke", () => {
    isVisible = true;
    expect(FADLocations.getOptionsForLayer(isVisible, 'red')).toEqual({
        strokeColor: 'red',
        strokeDashArray: [6, 6],
        strokeWidth: 2,
        strokeOpacity: 0.5,
        visible: isVisible
    });
});

test("Returns the correct details html", () => {
    expect(FADLocations.getMoreDetailsHtml('12829')).toEqual('<a href=\"/searchFADByID.html?12829\" target=\"_blank\" rel=\"noopener noreferrer\">View more details</a>');
});

test("Creates the correct checkbox html for checked FADId", () => {
    expectedHtml = '<input type="checkbox" id= "showWaypoints12829" onclick = "showWaypoints(\'showWaypoints12829\', \'12829\')\" checked />'
    expect(FADLocations.getCheckboxHtml('12829', true)).toEqual(expectedHtml);
});

test("Creates the correct checkbox html for unchecked FADId", () => {
    expectedHtml = '<input type="checkbox" id= "showWaypoints12829" onclick = "showWaypoints(\'showWaypoints12829\', \'12829\')\" checked />'
    expect(FADLocations.getCheckboxHtml('12829', true)).toEqual(expectedHtml);
});

test("Gets the unique previous locations for an FAD given its fully detailed JSON", () => {
    FADPrevLocations = [[-61.067, 13.567]];
    // 32951
    text = '[{"Unnamed: 0": 0.0, "ISO_country": "US", "FADId": 32951.0, "Latitude": 13.567, "Longitude": -61.067, "Year": 1887.0, "Month": 12.0, "Day": 4.0, "Time": 0, "WOD_unique": 13575254.0, "depth(m)": 514.0, "qc_flag": 0.0, "Temp": 8.89, "qc_flag.1": 0.0, "Sal": 0, "qc_flag.2": 0, "Oxy": 0, "qc_flag.3": 0, "Phos": 0, "qc_flag.4": 0, "dum5": 0, "qc_flag.5": 0, "Sil": 0, "qc_flag.6": 0, "dum7": 0, "qc_flag.7": 0, "NO3": 0, "qc_flag.8": 0, "pH": 0, "qc_flag.9": 0, "dum10": 0, "qc_flag.10": 0, "Chl": 0, "qc_flag.11": 0, "dum12": 0, "qc_flag.12": 0, "dum13": 0, "qc_flag.13": 0, "dum14": 0, "qc_flag.14": 0, "dum15": 0, "qc_flag.15": 0, "dum16": 0, "qc_flag.16": 0, "Alk": 0, "qc_flag.17": 0, "dum18": 0, "qc_flag.18": 0, "dum19": 0, "qc_flag.19": 0, "pCO2": 0, "qc_flag.20": 0, "DIC": 0, "qc_flag.21": 0, "dum22": 0, "qc_flag.22": 0, "dum23": 0, "qc_flag.23": 0, "BAC": 0, "qc_flag.24": 0, "dum25": 0, "qc_flag.25": 0, "dum26": 0, "qc_flag.26": 0, "dum27": 0, "qc_flag.27": 0, "dum28": 0, "qc_flag.28": 0, "dum29": 0, "qc_flag.29": 0, "dum30": 0, "qc_flag.30": 0, "dum31": 0, "qc_flag.31": 0, "dum32": 0, "qc_flag.32": 0, "Trit": 0, "qc_flag.33": 0, "He": 0, "qc_flag.34": 0, "dHE3": 0, "qc_flag.35": 0, "dC14": 0, "qc_flag.36": 0, "dC13": 0, "qc_flag.37": 0, "Arg": 0, "qc_flag.38": 0, "Neo": 0, "qc_flag.39": 0, "CFC11": 0, "qc_flag.40": 0, "CFC12": 0, "qc_flag.41": 0, "CFC113": 0, "qc_flag.42": 0, "O18": 0, "qc_flag.43": 0}]';
    FADJson = JSON.parse(text);
    expect(FADLocations.getUniqueFADLocations(FADJson)).toEqual(FADPrevLocations);
});

test("Gets the unique previous locations for an FAD given its JSON", () => {
    FADPrevLocations = [[-61.067, 13.567], [-61.068, 13.568]];
    // FADId: 32951
    text = '[{"FADId": 32951.0, "Latitude": 13.567, "Longitude": -61.067}, {"FADId": 32951.0, "Latitude": 13.568, "Longitude": -61.068}, {"FADId": 32951.0, "Latitude": 13.567, "Longitude": -61.067}]';
    FADJson = JSON.parse(text);
    expect(FADLocations.getUniqueFADLocations(FADJson)).toEqual(FADPrevLocations);
});

test("Gets the most recent FAD data for each FADId given JSON dataset", () => {
    uniqueFADs = {};
    uniqueFADs["1"] = { "FADId": "1", "Latitude": 13.568, "Longitude": -61.068 };
    uniqueFADs["2"] = { "FADId": "2", "Latitude": 13.567, "Longitude": -61.067 };
    text = '[{"FADId": "1", "Latitude": 13.567, "Longitude": -61.067}, {"FADId": "1", "Latitude": 13.568, "Longitude": -61.068}, {"FADId": "2", "Latitude": 13.567, "Longitude": -61.067}]';

    FADJson = JSON.parse(text);
    expect(FADLocations.getUniqueFADsFromObj(FADJson)).toEqual(uniqueFADs);
});
