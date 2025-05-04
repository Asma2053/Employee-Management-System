// Global variable to track the active clock-in
let activeClockInId = null;
let activeClockIn = false;


function saveLocationData(time, latitude, longitude) {
    console.log("📤 Sending clock-in data...", { time, latitude, longitude });

    fetch('/attendancedetails/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ time, latitude, longitude })
    })
    .then(handleResponse)
    .then(data => {
        alert("Clock-in successful!");  // Simplified message
        console.log("✅ Clock-in response:", data);
        activeClockInId = true;
        localStorage.setItem('activeClockInId', activeClockInId);
    })
    .catch(handleError);
}


function handleResponse(response) {
    if (!response.ok) {
        return response.json().then(err => {
            throw new Error(err.error || "Server error");
        }).catch(() => {
            throw new Error("Non-JSON response from server");
        });
    }
    return response.json();
}

function handleError(error) {
    console.error("❌ API Error:", error);
    alert(error.message || "Clock-in failed");
}




function buttonOneClick() {
    if (activeClockIn) {
        alert("You're already clocked in!");
        return;
    }

    const currentTime = new Date().toISOString();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            console.log("📍 Location captured, saving clock-in...");
            saveLocationData(currentTime, latitude, longitude);
        }, function(error) {
            alert("Geolocation error: " + error.message);
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}


function buttonTwoClick() {

    const currentTime = new Date().toISOString();
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                saveLocationDataClockout(
                    currentTime,
                    position.coords.latitude,
                    position.coords.longitude
                );
            },
            error => {
                alert("Geolocation error: " + error.message);
            },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    } else {
        alert("Geolocation not supported");
    }
}



// Clock-out function (updated)
function saveLocationDataClockout(time, latitude, longitude) {

    fetch('/attendancedetailsclockout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            timestamp_clock_out: time,
            latitude_clock_out: latitude,
            longitude_clock_out: longitude
        })
    })
    .then(response => {
        if (!response.ok) return response.json().then(err => { throw err; });
        return response.json();
    })
    .then(data => {
        if (data.error) throw new Error(data.error);
        alert("Clock-out saved successfully!");
        console.log("Clock-out data:", data);
        // Clear the active clock-in
        // activeClockInId = null;
        localStorage.removeItem('activeClockInId');
    })
    .catch(error => {
        alert("Clock-out failed: " + error.message);
        console.error("Error:", error);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    activeClockInId = localStorage.getItem('activeClockInId');
});

// Shared response handler
function handleResponse(response) {
    if (!response.ok) {
        return response.json().then(err => {
            throw new Error(err.error || "Server error");
        });
    }
    return response.json();
}



// Shared error handler
function handleError(error) {
    console.error("API Error:", error);
    alert(error.message || "Operation failed");
    throw error;  // Re-throw for further handling if needed
}



