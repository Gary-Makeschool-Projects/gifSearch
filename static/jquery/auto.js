// this is where the magic happens with a single post request to the server
function magicalShit() {
    // grab the fucking data
    var bla = $('#search').val();
    //lets test and see if we grabbed the data
    console.log(bla); // verify that shit works by opening up the console yourself
    // now create a json object out of that data bro
    var idkwhattonamethisobject = new Object();
    // assign input data into object because why tf not
    idkwhattonamethisobject.search_term = bla;
    // yikes bro ._.
    var yikes = JSON.stringify(idkwhattonamethisobject);
    // ajax the JSON to the server aka send that shit to the backend
    $.post('test', yikes, function(data) {
        const ref = $('#gifs');
        ref.empty();
        for (url of data) {
            ref.append(`<img src="${url}"/>`);
        }
    });
    // stop link reloading the page becasue that shit was pretty annoying
    //event.preventDefault();
}
// this function does absolutley fucking nothing but just listens for changes on the client side
$(document).ready(function() {
    $('#search').on('change keyup paste', function() {
        // lets call the magical function
        magicalShit();
        console.log('i sense change...im calling the backend to beat your ass');
    });
});
