// JavaScript TypeError and XSS vulnerability demo
function processUser(user) {
    // TypeError: Accessing property of null
    const name = null.name;
    
    // Security: innerHTML XSS Risk
    document.getElementById("output").innerHTML = "Hello " + name;
}
