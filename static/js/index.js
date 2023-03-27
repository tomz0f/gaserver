var setViewLatLng = new L.LatLng(38.329355001, 28.0694747494);
var mymap = L.map('mapid').setView(setViewLatLng, 19)
var latlng2 = new L.LatLng(38.329355001, 28.0694747494);

//--------------------------------\
//  BUNLARI HAKEDECEK NE YAPTIM?  )>
//--------------------------------/

var parsel = L.polygon(
  [
    [38.331455001, 28.0724747494],
    [38.331255001, 28.0654747494],
    [38.329055001, 28.0654747494],
    [38.329255001, 28.0724747494]
  ],{
    color: 'red'
}).addTo(mymap);
let googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
});
googleSat.addTo(mymap)

navigator.geolocation.getCurrentPosition(function (location, options = {
    enableHighAccuracy: true,
    timeout: 500,
    maximumAge: 0
  }) {
  
    let redIcon = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    
      L.marker(latlng2, { icon: redIcon }).bindPopup().addTo(mymap);
      
    const parselData = getParsel(location)

    
});

const getParsel = async function (location){
  let result = await fetch(`/parselSorgu/${location.coords.latitude}/${location.coords.longitude}`, {
    method: "GET",
  })
  let parselData = await result.json();
  return parselData;
}

const search = () => {
  let query = document.getElementById("query").value;
  if (query == "") {
    window.alert('Lütfen bir isim giriniz...')
  } else {
    query = query.replace(/%20/g, " ");
    window.location.href = '/search?query='+query;
  }
};