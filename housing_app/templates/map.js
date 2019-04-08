function initMap() {
              var apt_coordinates = {lat: 38.0325982, lng: -78.4955055};
              var apt_coor_2 = {lat:38.0327987, lng: -78.4952891};
              var apt_coor_3 ={lat:38.037524, lng:-78.4989593}; 
              var apt_coor_4 ={lat:38.0372172, lng:-78.5015677}; 
              var apt_coor_5 ={lat:38.0286472 , lng:-78.5112196 }; 
              var apt_coor_6 ={lat:38.0316282, lng: -78.4842689};

              var apt_coor_7 ={lat:38.0350752, lng:-78.4981588};
              var apt_coor_8 ={lat:38.0416242, lng:-78.503709};
              //var apt_coor_9a ={lat:38.0698574, lng:-78.4659562;
              var apt_coor_10 ={lat:38.0286541, lng:-78.4816677};
              var apt_coor_11 ={lat:38.0423332, lng:-78.5114287};
              var apt_coor_12 ={lat:38.0410028, lng:-78.50382};
              var apt_coor_13 ={lat:38.0698574, lng:78.4659562};
              //var geocoder;
              var map = new google.maps.Map(document.getElementById('map'), { center: apt_coordinates,
              zoom: 14,
              styles: [
                        // {elementType: 'marker', stylers: [{color: '#333333'}]}
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
             var marker = new google.maps.Marker({position: apt_coordinates, map: map, label: 'The Flats'});
              var marker2 = new google.maps.Marker({position: apt_coor_2, map: map, label: 'Venable'}); 
             //var marker3 = new google.maps.Marker({position: apt_coor_3, map: map},label: 'The Standard'}); 
              var marker4 = new google.maps.Marker({position: apt_coor_4, map: map, label: 'Grandmarc'}); 
              var marker5 = new google.maps.Marker({position: apt_coor_5, map: map, label: '1800 JPA'}); 
             var marker6 = new google.maps.Marker({position: apt_coor_6, map: map, label: '112 West Market St.'});
              var marker7 = new google.maps.Marker({position: apt_coor_7, map: map, label: '1115 Wertland St.'});
              var marker8 = new google.maps.Marker({position: apt_coor_8, map: map, label: '64 University Way'});

              var marker10 = new google.maps.Marker({position: apt_coor_10, map: map, label: '300 4th St. SE'});
              var marker11 = new google.maps.Marker({position: apt_coor_11, map: map, label: '2021 Ivy Rd'});
              var marker12 = new google.maps.Marker({position: apt_coor_12, map: map, label: '1801 Lambeth Lane'});
              var marker13 = new google.maps.Marker({position: apt_coor_13, map: map, label: 'Reserve at Belvedere'});



              // Loop through our array of markers & place each one on the map

/*
          function codeAddress() {

            //for each apartment
            var address = apartment.location; //not sure how to access this
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
            });*/
          }


