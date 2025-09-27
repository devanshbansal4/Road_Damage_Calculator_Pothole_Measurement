// JavaScript function to toggle between image and video sections
function toggleInputType(inputType) {
    console.log("Toggling input type: ", inputType);  // Debugging line

    // Hide both divs
    document.getElementById("image").style.display = "none";
    document.getElementById("video").style.display = "none";

    // Show the selected div
    if (inputType === "image") {
        console.log("Displaying Image Section");
        document.getElementById("image").style.display = "block";
    } else if (inputType === "video") {
        console.log("Displaying Video Section");
        document.getElementById("video").style.display = "block";
    }
}

// Automatically show the image section when the page loads
window.onload = function() {
    toggleInputType("image");
};
