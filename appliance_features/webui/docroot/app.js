function Refresh() {
  const loader = document.getElementById("loading-modal")
  loader.innerHTML = '<p>Refreshing...</p>'
  loader.show()
  window.location.reload()
}

function AutoRefresh() {
  setTimeout(Refresh, 60*1000)
}

function doReboot() {
  const timeout = 2000
  const waiter = () => {
    fetch('/index.html')
      .then(() => { location.href = '/'})
      .catch((error) => { loader.innerHTML += '😴 '; setTimeout(waiter, timeout)})
  }
  const loader = document.getElementById("loading-modal")
  loader.innerHTML = '<p>Appliance Reboot Requested</p><p>Hold Tight</p>'
  loader.show()
  fetch('/cgi-bin/reboot.py').catch((error) => {})
  setTimeout(waiter, timeout)
}

function doPoweroff() {
  const loader = document.getElementById("loading-modal")
  loader.innerHTML = "<p>Appliance Power Off Requested</p><p>We're Done Here</p>"
  loader.show()
  fetch('/cgi-bin/poweroff.py').catch((error) => {})
}

function doStop() {
  const loader = document.getElementById("loading-modal")
  loader.innerHTML = '<p>Stop Appliance Requested</p><p>Please Be Patient</p>'
  loader.show()
  fetch('/cgi-bin/stop.py')
    .then(() => { location.reload(); })
}

function doStart() {
  const loader = document.getElementById("loading-modal")
  loader.innerHTML = '<p>Start Appliance Requested</p><p>Please Be Patient</p>'
  loader.show()
  fetch('/cgi-bin/start.py')
    .then(() => { location.reload(); })
}
