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