function initMap() {
              var apt_coordinates = {lat: 38.0325982, lng: -78.4955055};
              var apt_coor_2 = {lat:38.0327987, lng: -78.4952891};
              var apt_coor_3 ={lat:38.037524 , lng:-78.4989593 }; 
              var apt_coor_4 ={lat:38.0372172, lng:-78.5015677}; 
              var apt_coor_5 ={lat:38.0286472 , lng:-78.5112196 }; 
              var geocoder;
              var map = new google.maps.Map(document.getElementById('map'), { center: apt_coordinates,
              zoom: 14,
              styles: [
                        {elementType: 'geometry', stylers: [{color: '#bbbbbb'}]},
                        {elementType: 'labels.text.stroke', stylers: [{color: '#4f4f4f'}]},
                        {elementType: 'labels.text.fill', stylers: [{color: '#ffbebc'}]},
                        {
                          featureType: 'administrative.locality',
                          elementType: 'labels.text.fill',
                          stylers: [{color: '#b7ffc7'}]
                        },
                        {
                          featureType: 'road',
                          elementType: 'labels.text.fill',
                          stylers: [{color: '#b7ffc7'}]
                        },
                        {
                          featureType: 'road.highway',
                          elementType: 'geometry',
                          stylers: [{color: '#b7ffc7'}]
                        },
                        {
                          featureType: 'road.highway',
                          elementType: 'geometry.stroke',
                          stylers: [{color: '#b7ffc7'}]
                        },
                        {
                          featureType: 'road.highway',
                          elementType: 'labels.text.fill',
                          stylers: [{color: '#ffbebc'}]
                        },
                        {
                          featureType: 'poi.park',
                          elementType: 'geometry',
                          stylers: [{color: '#ffbebc'}]
                        },
                        {
                          featureType: 'transit',
                          elementType: 'geometry',
                          stylers: [{color: '#2f3948'}]
                        },
                         {
                          featureType: 'transit.station',
                          elementType: 'labels.text.fill',
                          stylers: [{color: '#b7ffc7'}]
                        },
                        ]
              });
             //  var marker = new google.maps.Marker({position: apt_coordinates, map: map, label: 'The Flats'});
             //  var marker2 = new google.maps.Marker({position: apt_coor_2, map: map, label: 'Venable'}); 
             // //var marker3 = new google.maps.Marker({position: apt_coor_3, map: map},label: 'The Standard'}); 
             //  var marker4 = new google.maps.Marker({position: apt_coor_4, map: map, label: 'Grandmarc'}); 
             //  var marker5 = new google.maps.Marker({position: apt_coor_5, map: map, label: '1800 JPA'}); 
              
              // Loop through our array of markers & place each one on the map


          function codeAddress() {

            //for each apartment
            var address = apartment.location;
            geocoder.geocode( { 'address': address}, function(results, status) {
              if (status == 'OK') {
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
              } else {
                alert('Geocode was not successful for the following reason: ' + status);
              }
            });
          }


}

initMap();



<!--Start of map stuff-->
     <?php
$data = file_get_contents('apartment_data.csv');
$api_key = 'AIzaSyBnnca1doBE-nE14750VNFA4VtqlLrcJZk';
$lines = explode("\n",$data);

foreach ($lines as $key => $value){
	if ($key>0&&strlen($value)>20){ // skip csv header row and blank rows
		$line = explode(",",$value);
		$markers[$key] = trim($line[0]).','.trim($line[1]).','.trim($line[2]).','.trim($line[3]). ',' .trim($line[4]).
		','.trim($line[5]). ',' .trim($line[6]).','.trim($line[7]). ',' .trim($line[8]).','.trim($line[9]). ','
		.trim($line[10]).','.trim($line[11]). ',' .trim($line[12]). ',' .trim($line[13]);
		//name, company,location, price, size, bedrooms, furnished, pets, description, bathrooms, number, distance to grounds, image
	}
}


?>

<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
      html, body, #map-canvas { height: 100%; margin: 0; padding: 0;}
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=<?=$AIzaSyBnnca1doBE-nE14750VNFA4VtqlLrcJZk?>">
    </script>
    <script type="text/javascript">
		var map;
		var marker = {};
		function initialize() {
			var mapOptions = {
			center: {lat: 38.0325982, lng: -78.4955055},
			zoom: 14
		};
		map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions,
		styles[
		 {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f5f5f5"
      }
    ]
  },
  {
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "weight": 1.5
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "weight": 1.5
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#bdbdbd"
      }
    ]
  },
  {
    "featureType": "administrative.locality",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#ffb0b8"
      },
      {
        "weight": 2
      }
    ]
  },
  {
    "featureType": "administrative.locality",
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#dc858e"
      },
      {
        "weight": 1
      }
    ]
  },
  {
    "featureType": "landscape.man_made",
    "elementType": "geometry",
    "stylers": [
      {
        "visibility": "simplified"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#eeeeee"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "weight": 1.5
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#757575"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e5e5e5"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#ffffff"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "weight": 3
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#757575"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#dadada"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#616161"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e5e5e5"
      }
    ]
  },
  {
    "featureType": "transit.station",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#eeeeee"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#c9c9c9"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  }]);
		var markers = [];

		<?php
			$counter = 0;
			foreach ($markers as $index => $list){
				   $marker_details = explode(',',$list);
				   echo 'markers["m'.($index-1).'"] = {};'."\n";
				   echo "markers['m".($index-1)."'].name = '".$marker_details[0]."';\n";
				   echo "markers['m".($index-1)."'].company = '".$marker_details[1]."';\n";
				   echo "markers['m".($index-1)."'].location = '".$marker_details[2]."';\n";
				   echo "markers['m".($index-1)."'].price = '".$marker_details[3]."';\n";
				   echo "markers['m".($index-1)."'].size = '".$marker_details[4]."';\n";
				   echo "markers['m".($index-1)."'].bedrooms = '".$marker_details[5]."';\n";
				   echo "markers['m".($index-1)."'].furnished = '".$marker_details[6]."';\n";
				   echo "markers['m".($index-1)."'].pets = '".$marker_details[7]."';\n";
				   echo "markers['m".($index-1)."'].description= '".$marker_details[8]."';\n";
				   echo "markers['m".($index-1)."'].bathrooms= '".$marker_details[9]."';\n";
				   echo "markers['m".($index-1)."'].number = '".$marker_details[10]."';\n";
				   echo "markers['m".($index-1)."'].distgrounds = '".$marker_details[11]."';\n";
				   echo "markers['m".($index-1)."'].image = '".$marker_details[12]."';\n";
				   $counter++;
		   }
		?>
		var totalMarkers = <?=$counter?>;
		var i = 0;
		var infowindow;
		var contentString;
		for (var i = 0; i<totalMarkers; i++){

            contentString = '<div class="content">'+
				  '<h1 class="firstHeading">'+markers['m'+i].name+'</h1>'+
				  '<div class="bodyContent">'+
				  '<p>'+markers['m'+i].price+'</p>'+
				  '</div>'+
				  '</div>';


			infowindow = new google.maps.InfoWindow({
				  content: contentString

				  });

            geocoder.geocode( { 'address': markers['m'+i].address}, function(results, status) {
              if (status == 'OK') {
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    title: markers['m'+i].name,
                    infowindow:infowindow
                });
              } else {
                alert('Geocode was not successful for the following reason: ' + status);
              }
            });


			};


			google.maps.event.addListener(marker['c'+i], 'click', function() {
					for (var key in marker){
						marker[key].infowindow.close();
					}
					this.infowindow.open(map, this);

			});
		}

      }
	  /*function panMap(la,lo){
			map.panTo(new google.maps.LatLng(la,lo));

	  }*/
	  function openMarker(mName){
		  //console.log(marker);
		  for (var key in marker){
			  marker[key].infowindow.close();
		  }
		  for (var key in marker){

			if (marker[key].name.search(mName) != -1){
				marker[key].infowindow.open(map,marker[key]);
			}
		  }
	  }
      google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>
  <body>
<div id="map-canvas"></div>
  </body>
</html>



            <div id="map"></div>

             <script>

              function initMap() {
              var apt_coordinates = {lat: 38.0325982, lng: -78.4955055};

              var geocoder;
              var map = new google.maps.Map(document.getElementById('map'), { center: apt_coordinates,
              zoom: 14,
       // add styles here

              });



                }
             </script>

                <script async defer
                src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBnnca1doBE-nE14750VNFA4VtqlLrcJZk&callback=initMap">
                </script>

        </div>