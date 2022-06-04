(function () {
  "use strict";

  document.addEventListener('click', async event => {
    if (event.target.id === 'button') {
      const stream = await window.navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      const video = document.getElementById('video');
      stream.getAudioTracks();
      stream.getVideoTracks();
      video.srcObject = stream;
      video.play();
    }
  });
})();

document.querySelector('form').addEventListener("submit", function (e) {
    e.preventDefault();
    let param = document.querySelector('input[name="myparam"]').value;
    window.location.href = 'http://127.0.0.1:8000/' + "#" + param;
});

