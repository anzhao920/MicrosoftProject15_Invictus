//The maximum zoom level to cluster data point data on the map.
var maxClusterZoomLevel = 8;

//The URL to the FAD location data.
var FADsLocationDataUrl = '/API/AllFADs';
const headingColor = 'DarkOrchid';
const waypointsColor = 'blue';

//The URL to the icon image. 
var iconImageUrl = 'images/iconFAD.png';

var map, popup, datasource, iconLayer, centerMarker, searchURL, lineLayer, checkboxState, FADCoords;
var FADWaypointMarkers;
var listItemTemplate = '<div class="listItem" onclick="itemSelected(\'{id}\')"><div class="listItem-title">{title}</div>{city}<br />Open until {closes}<br />{distance} miles away</div>';

function initialize() {
    fetch('javascripts/AzureMapsAPIKey.txt')
        .then(response => response.text()).then(function (AzureMapsKey) {
            //Initialize a map instance.
            map = new atlas.Map('myMap', {
                center: [13.9094, -60.9789],
                zoom: 2,
                view: 'Auto',
                //Add authentication details for connecting to Azure Maps.
                authOptions: {
                    authType: 'subscriptionKey',
                    subscriptionKey: AzureMapsKey
                }
            });

            //Create a popup but leave it closed so we can update it and display it later.
            popup = new atlas.Popup();

            //Use MapControlCredential to share authentication between a map control and the service module.
            var pipeline = atlas.service.MapsURL.newPipeline(new atlas.service.MapControlCredential(map));

            //Create an instance of the SearchURL client.
            searchURL = new atlas.service.SearchURL(pipeline);

            //If the user presses the search button, geocode the value they passed in.
            document.getElementById('searchBtn').onclick = performSearch;

            //If the user presses enter in the search textbox, perform a search.
            document.getElementById('searchTbx').onkeyup = function (e) {
                if (e.keyCode === 13) {
                    performSearch();
                }
            };

            //If the user presses the My Location button, use the geolocation API to get the users location and center/zoom the map to that location.
            document.getElementById('myLocationBtn').onclick = setMapToUserLocation;

            //Wait until the map resources are ready.
            map.events.add('ready', function () {
                //Add the zoom control to the map.
                map.controls.add(new atlas.control.ZoomControl(), {
                    position: 'top-right'
                });
                //Add the arrow icon used for FAD headings.
                map.imageSprite.add('arrow-icon', 'images/purpleArrowRight.png');

                //Add an HTML marker to the map to indicate the center used for searching.
                centerMarker = new atlas.HtmlMarker({
                    htmlContent: '<div class="mapCenterIcon"></div>',
                    position: map.getCamera().center,
                });

                map.markers.add(centerMarker);

                //Create a data source and add it to the map and enable clustering.
                datasource = new atlas.source.DataSource(null, {
                    cluster: true,
                    clusterMaxZoom: maxClusterZoomLevel - 1
                });

                map.sources.add(datasource);
                //Dictionary that stores T if the waypoints of the FAD are shown and F otw
                checkboxState = {};
                //Stores the html markers of FADs
                FADWaypointMarkers = {};
                //Load all the FAD data now that the data source has been defined. 
                loadFadData();
                //For each FAD(id), store the lineLayer of its previous waypoints.
                lineLayer = {};

                //Create a bubble layer for rendering clustered data points.
                var clusterBubbleLayer = new atlas.layer.BubbleLayer(datasource, null, {
                    radius: 12,
                    color: '#007faa',
                    strokeColor: 'white',
                    strokeWidth: 2,
                    filter: ['has', 'point_count'] //Only render data points which have a point_count property, which clusters do.
                });

                //Create a symbol layer to render the count of locations in a cluster.
                var clusterLabelLayer = new atlas.layer.SymbolLayer(datasource, null, {
                    iconOptions: {
                        image: 'none' //Hide the icon image.
                    },
                    textOptions: {
                        textField: ['get', 'point_count_abbreviated'],
                        size: 12,
                        font: ['StandardFont-Bold'],
                        offset: [0, 0.4],
                        color: 'white'
                    }
                });

                map.layers.add([clusterBubbleLayer, clusterLabelLayer]);

                //Load a custom image icon into the map resources.
                map.imageSprite.add('myCustomIcon', iconImageUrl).then(function () {
                    //Create a layer to render a FAD symbol above each bubble for an individual location.
                    iconLayer = new atlas.layer.SymbolLayer(datasource, null, {
                        iconOptions: {
                            //Pass in the id of the custom icon that was loaded into the map resources.
                            image: 'myCustomIcon',
                            //Optionally scale the size of the icon.
                            font: ['SegoeUi-Bold'],
                            //Anchor the center of the icon image to the coordinate.
                            anchor: 'center',
                            //Allow the icons to overlap.
                            allowOverlap: true
                        },
                        filter: ['!', ['has', 'point_count']] //Filter out clustered points from this layer.
                    });

                    map.layers.add(iconLayer);

                    //When the mouse is over the cluster and icon layers, change the cursor to be a pointer.
                    map.events.add('mouseover', [clusterBubbleLayer, iconLayer], function () {
                        map.getCanvasContainer().style.cursor = 'pointer';
                    });

                    //When the mouse leaves the item on the cluster and icon layers, change the cursor back to the default which is grab.
                    map.events.add('mouseout', [clusterBubbleLayer, iconLayer], function () {
                        map.getCanvasContainer().style.cursor = 'grab';
                    });

                    //Add a click event to the cluster layer. When someone clicks on a cluster, zoom into it by 2 levels. 
                    map.events.add('click', clusterBubbleLayer, function (e) {
                        map.setCamera({
                            center: e.position,
                            zoom: map.getCamera().zoom + 2
                        });
                    });

                    //Add a click event to the icon layer and show the shape that was clicked.
                    map.events.add('click', iconLayer, function (e) {
                        showPopup(e.shapes[0]);
                    });

                    //Add an event to monitor when the map has finished moving.
                    map.events.add('render', function () {
                        //Give the map a chance to move and render data before updating the list.
                        updateListItems();
                    });
                });
            });
        });
}

/**
 * Helper function that creates a symbol layer on top of a line.
 * @param {*} linesDataSource 
 */
function getSymbolLayerForLine(linesDataSource) {
    var symbolLayer = new atlas.layer.SymbolLayer(linesDataSource, null, {
        //Specify how much space should be between the symbols in pixels.
        lineSpacing: 50,
        //Tell the symbol layer that the symbols are being rendered along a line.
        placement: 'line',
        iconOptions: {
            image: 'arrow-icon',
            allowOverlap: true,
            anchor: 'center',
            size: 0.5
        }
    });
    return symbolLayer;
}

function addLineLayerForFAD(FADId, waypoints, color) {
    if (FADId in lineLayer) {
        // Ignore the case when the line already exists.
        return;
    }
    // Create line datasource for adding line layers to the map.
    var linesDataSource = new atlas.source.DataSource();
    map.sources.add(linesDataSource);
    linesDataSource.add(new atlas.data.LineString(waypoints));
    lineLayer[FADId] = new atlas.layer.LineLayer(linesDataSource);
    map.layers.add(lineLayer[FADId]);
    if (FADId.indexOf('heading') != -1) {
        //Line shows the heading of FADId.
        map.layers.add(getSymbolLayerForLine(linesDataSource));
    } else {
        //Line shows previous location, thus create markers for waypoints.
        FADWaypointMarkers[FADId] = [];
        for (waypointIdx in waypoints) {
            var waypoint = waypoints[waypointIdx];
            crtMarker = new atlas.HtmlMarker({
                htmlContent: '<div class="waypointIcon"></div>',
                position: waypoint,
                visible: true
            });
            map.markers.add(crtMarker);
            //Add markers to dictionary s.t. their visibility can be controlled.
            FADWaypointMarkers[FADId].push(crtMarker);
        }
    }
    updateLineLayerForFAD(FADId, true, color);
}

function updateLineLayerForFAD(FADId, isVisible, color) {

    lineLayer[FADId].setOptions(getOptionsForLayer(isVisible, color));
    if (!(FADId in FADWaypointMarkers)) {
        //The FAD has no markers yet.
        return;
    }
    for (crtMarkerIdx in FADWaypointMarkers[FADId]) {
        crtMarker = FADWaypointMarkers[FADId][crtMarkerIdx];
        crtMarker.setOptions({
            visible: isVisible
        });
    }
}

function getOptionsForLayer(isVisible, color) {
    return {
        strokeColor: color,
        strokeDashArray: [6, 6],
        strokeWidth: 2,
        strokeOpacity: 0.5,
        visible: isVisible
    };
}

function getUniqueFADsFromObj(objs) {
    var uniqueFADs = {};
    for (objIdx in objs) {
        obj = objs[objIdx];
        uniqueFADs[obj['FADId']] = obj;
    }
    return uniqueFADs;
}

function loadFadData() {
    // Use the API to get FAD data.
    fetch(FADsLocationDataUrl)
        .then(response => response.text())
        .then(function (objs) {
            objs = JSON.parse(objs);
            var features = [];
            //Expected JSON properties.
            // var row = ['FADId', 'Latitude', 'Longitude','depth_m_', 'Temp'];

            var uniqueFADs = getUniqueFADsFromObj(objs);
            //Store the current coordinates of each FAD as they can be changed only in the database.
            FADCoords = {};

            for (objIdx in uniqueFADs) {
                obj = uniqueFADs[objIdx];
                FADCoords[obj['FADId']] = [parseFloat(obj['Longitude']), parseFloat(obj['Latitude'])];

                features.push(new atlas.data.Feature(new atlas.data.Point([parseFloat(obj['Longitude']), parseFloat(obj['Latitude'])]), {
                    FADId: obj['FADId'],
                    Depth: obj['depth_m_'],
                    Temp: obj['Temp']
                }));
            }

            //Add the features to the data source.
            datasource.add(features);
            //Initially update the list items.
            updateListItems();
        });
}

function performSearch() {
    var query = document.getElementById('searchTbx').value;

    //Perform a fuzzy search on the users query.
    searchURL.searchFuzzy(atlas.service.Aborter.timeout(3000), query, {
        // //Pass in the array of country ISO2 for which we want to limit the search to.
        view: 'Auto'
    }).then(results => {
        //Parse the response into GeoJSON so that the map can understand.
        var data = results.geojson.getFeatures();

        if (data.features.length > 0) {
            //Set the camera to the bounds of the results.
            map.setCamera({
                bounds: data.features[0].bbox,
                padding: 40
            });
        } else {
            document.getElementById('listPanel').innerHTML = '<div class="statusMessage">Unable to find the location you searched for.</div>';
        }
    });
}

function setMapToUserLocation() {
    //Request the user's location.
    navigator.geolocation.getCurrentPosition(function (position) {
        //Convert the geolocation API position into a longitude/latitude position value the map can understand and center the map over it.
        map.setCamera({
            center: [position.coords.longitude, position.coords.latitude],
            zoom: maxClusterZoomLevel + 1
        });
    }, function (error) {
        //If an error occurs when trying to access the users position information, display an error message.
        switch (error.code) {
            case error.PERMISSION_DENIED:
                alert('User denied the request for Geolocation.');
                break;
            case error.POSITION_UNAVAILABLE:
                alert('Position information is unavailable.');
                break;
            case error.TIMEOUT:
                alert('The request to get user position timed out.');
                break;
            case error.UNKNOWN_ERROR:
                alert('An unknown error occurred.');
                break;
        }
    });
}

function getUniqueFADLocations(objs) {
    var uniquePoints = {};
    var waypoints = [];
    for (objIdx in objs) {
        obj = objs[objIdx];
        pointObj = JSON.stringify({ "Lng": obj['Longitude'], "Lat": obj['Latitude'] })
        uniquePoints[pointObj] = obj;
    }
    for (objIdx in uniquePoints) {
        obj = uniquePoints[objIdx];
        //Add the past coordinates of the FAD
        waypoints.push([parseFloat(obj['Longitude']), parseFloat(obj['Latitude'])]);
    }
    return waypoints;
}

function getPreviousPointsForFAD(FADId) {
    crtFADUrl = `/API/FAD/${FADId}`;
    fetch(crtFADUrl)
        .then(response => response.text())
        .then(function (objs) {
            objs = JSON.parse(objs);
            //Expected JSON properties.
            // var row = ['FADId', 'Latitude', 'Longitude','depth_m_', 'Temp'];
            //Add the unique previous locations of the FAD to its lineLayer.
            addLineLayerForFAD(FADId, getUniqueFADLocations(objs), waypointsColor);
        });
}

function showHeadingForFAD(FADId, heading) {
    var camera = map.getCamera();
    var d = 1 / (2 * camera.zoom);
    const x = FADCoords[FADId][0];
    const y = FADCoords[FADId][1];
    var newX = x + Math.cos(heading) * d;
    var newY = y + Math.sin(heading) * d;
    addLineLayerForFAD(FADId + '_heading', [[x, y], [newX, newY]], headingColor);
}

function showWaypoints(checkBoxId, FADId) {
    if (document.getElementById(checkBoxId).checked) {
        checkboxState[FADId] = true;
        if (!(FADId in lineLayer)) {
            getPreviousPointsForFAD(FADId);
        } else {
            updateLineLayerForFAD(FADId, true, waypointsColor);
        }
    }
    else {
        checkboxState[FADId] = false;
        updateLineLayerForFAD(FADId, checkboxState[FADId], waypointsColor);
    }
}

function updateListItems() {
    //Hide the center marker.
    centerMarker.setOptions({
        visible: false
    });

    //Get the current camera/view information for the map.
    var camera = map.getCamera();

    var listPanel = document.getElementById('listPanel');

    //Check to see if the user is zoomed out a lot. If they are, tell them to zoom in closer, perform a search or press the My Location button.
    if (camera.zoom < maxClusterZoomLevel) {
        //Close the popup as clusters may be displayed on the map. 

        popup.close();

        listPanel.innerHTML = '<div class="statusMessage">Search for a location, zoom the map, or press the "My Location" button to see individual locations.</div>';
    } else {

        //Update the location of the centerMarker.
        centerMarker.setOptions({
            position: camera.center,
            visible: true
        });

        //List the ten closest locations in the side panel.
        var html = [], properties;

        /* Generating HTML for each item. */

        //Get all the shapes that have been rendered in the bubble layer. 
        var data = map.layers.getRenderedShapes(map.getCamera().bounds, [iconLayer]);

        //Create an index of the distances of each shape.
        var distances = {};
        data.forEach(function (shape) {
            if (shape instanceof atlas.Shape) {
                //Calculate the distance from the center of the map to each shape and store in the index. Round to 2 decimals.
                distances[shape.getId()] = Math.round(atlas.math.getDistanceTo(camera.center, shape.getCoordinates(), 'miles') * 100) / 100;
            }
        });

        //Sort the data by distance.
        data.sort(function (x, y) {
            return distances[x.getId()] - distances[y.getId()];
        });

        data.forEach(function (shape) {
            properties = shape.getProperties();
            showHeadingForFAD(properties['FADId'], 180);
            html.push('<div class="listItem" onclick="itemSelected(\'', shape.getId(), '\')"><div class="listItem-title">',
                properties['FADId'],
                '</div>',
                getMoreDetailsHtml(properties['FADId']),
                '<br />',
                'The temperature is ',
                properties['Temp'],
                '<br />',
                'The depth is ',
                properties['Depth'],
                ' meters',
                '<br />',
                //Get the distance of the shape.
                distances[shape.getId()],
                ' miles away</div>');
        });

        listPanel.innerHTML = html.join('');

        //Scroll to the top of the list panel incase the user has scrolled down.
        listPanel.scrollTop = 0;
    }
}

//When a user clicks on a result in the side panel, look up the shape by its id value and show popup.
function itemSelected(id) {
    //Get the shape from the data source using it's id. 
    var shape = datasource.getShapeById(id);
    showPopup(shape);

    //Center the map over the shape on the map.
    var center = shape.getCoordinates();
    var offset;

    //If the map is less than 700 pixels wide, then the layout is set for small screens.
    if (map.getCanvas().width < 700) {
        //When the map is small, offset the center of the map relative to the shape so that there is room for the popup to appear.
        offset = [0, -80];
    }

    map.setCamera({
        center: center,
        centerOffset: offset
    });
}

function getCheckboxHtml(FadId, isChecked) {
    checkboxId = `showWaypoints${FadId}`;
    if (isChecked) {
        return `<input type="checkbox" id= \"${checkboxId}\" onclick = \"showWaypoints(\'${checkboxId}\', \'${FadId}\')\" checked />`;
    } else {
        return `<input type="checkbox" id= \"${checkboxId}\" onclick = \"showWaypoints(\'${checkboxId}\', \'${FadId}\')\" />`;
    }
}

function getMoreDetailsHtml(FadId) {
    return `<a href="/searchFADByID.html?${FadId}" target="_blank" rel="noopener noreferrer">View more details</a>`;
}

function showPopup(shape) {
    var properties = shape.getProperties();
    //Calculate the distance from the center of the map to the shape in miles, round to 2 decimals.
    var distance = Math.round(atlas.math.getDistanceTo(map.getCamera().center, shape.getCoordinates(), 'miles') * 100) / 100;

    var html = ['<div class="storePopup">'];
    checkboxId = `showWaypoints${properties['FADId']}`;

    html.push('<div class="popupTitle">',
        properties['FADId'],
        '</div>',
        getMoreDetailsHtml(properties['FADId']),
        '<br />',
        getCheckboxHtml(properties['FADId'], checkboxState[properties['FADId']]),
        '<label for=', checkboxId, '>Show previous locations</label>',
        '<br />',
        'The temperature is ',
        properties['Temp'],
        '<br />',
        'The depth is ',
        properties['Depth'],
        ' meters',
        //Add the distance information.  
        '<br/>', distance,
        ' miles away'
    );
    html.push('</div></div>');

    //Update the content and position of the popup for the specified shape information.
    popup.setOptions({
        //Create a table from the properties in the feature.
        content: html.join(''),
        position: shape.getCoordinates()
    });

    //Open the popup.
    popup.open(map);
}


//Initialize the application when the page is loaded.
if (window) {
    window.onload = initialize;
}

module.exports.getOptionsForLayer = getOptionsForLayer;
module.exports.getMoreDetailsHtml = getMoreDetailsHtml;
module.exports.getCheckboxHtml = getCheckboxHtml;
module.exports.getUniqueFADLocations = getUniqueFADLocations;
module.exports.getUniqueFADsFromObj = getUniqueFADsFromObj;
