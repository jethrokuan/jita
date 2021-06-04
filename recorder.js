// This example uses MediaRecorder to record from a live audio stream,
// and uses the resulting blob as a source for an audio element.
//
// The relevant functions in use are:
//
// navigator.mediaDevices.getUserMedia -> to get audio stream from microphone
// MediaRecorder (constructor) -> create MediaRecorder instance for a stream
// MediaRecorder.ondataavailable -> event to listen to when the recording is ready
// MediaRecorder.start -> start recording
// MediaRecorder.stop -> stop recording (this will generate a blob of data)
// URL.createObjectURL -> to create a URL from a blob, which we can use as audio src

var recordButton, stopButton, recorder;

window.onload = function () {
  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    recorder = new MediaRecorder(stream);
    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    recorder.addEventListener('dataavailable', onRecordingReady);

    setInterval('recordSnippet()', 8000);
  });
};

function recordSnippet() {
    recorder.start();
    setTimeout(() => {
        recorder.stop();
    }, 7000);
}
function onRecordingReady(e) {
    var audio = document.getElementById('audio');
    var artist = document.getElementById('artist');
    var title = document.getElementById('title');
    var tab = document.getElementById('tab');
    var debug = document.getElementById('debug');
    var confidence = document.getElementById('confidence');
    // e.data contains a blob representing the recording
    // let blob = new Blob(e.data, {type:'audio/mpeg-3'});
    console.log(e.data);
    audio.src = URL.createObjectURL(e.data);
    fetch("http://127.0.0.1:5000/read", {
        method: "POST",
        body: e.data
    }).then(result => {
	return result.json();
    }).then(result => {
        artist.innerHTML = result["artist"];
        title.innerHTML = result["title"];
        tab.innerHTML = result["tab"];
        confidence.innerHTML = result["input_confidence"];
        debug.innerHTML = JSON.stringify(result);
    });

    // audio.play();
}
