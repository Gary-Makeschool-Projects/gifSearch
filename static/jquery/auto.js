// this is where the magic happens with a single post request to the server
function doWork() {
    // grab the fucking data
    var bla = $('#search').val(); // yah that shit works
    //lets test and see if we grabbed the data
    console.log(bla);
    // now create a json object out of that data
    var myObject = new Object();
    // assign input data into object
    myObject.search_term = bla;
    // yikes bro
    var yikes = JSON.stringify(myObject);
    // ajax the JSON to the server
    $.post('reciever', yikes, function() {});
    // stop link reloading the page
    event.preventDefault();
}
// this function does absolutley fucking nothing but just listens for changes on the client side
$(document).ready(function() {
    $('#search').on('change keyup paste', function() {
        // lets call the magical function
        doWork();
        console.log('fuck yah');
    });
});
