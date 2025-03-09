function login() {
    var userInput = prompt("JOIN AS: restaurant or NGO");

    if (!userInput) {
        alert("No option selected. Please enter 'restaurant' or 'ngo'.");
        return;
    }

    userInput = userInput.toLowerCase().trim();
    if (userInput === "restaurant") {
        window.location.href = "restaurant.html"; 
    } else if (userInput === "ngo") {
        window.location.href = "ngo.html"; 
    } else {
        alert("Invalid option selected. Please type 'restaurant' or 'ngo'.");
    }
}



