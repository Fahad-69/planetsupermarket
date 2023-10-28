var updateButtons = document.getElementsByName('purchase')

var url = '/update_item/'

for (const updateButton of updateButtons) {
    updateButton.addEventListener("click", function () {
        var productId = this.getAttribute("data-product")
        var action = this.getAttribute("data-action")
        if (user == "AnonymousUser") {
            window.location.href = "/login";
        } else {
            updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId,action) {
    console.log('User is logged in, sending data...')

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })
}

document.addEventListener("DOMContentLoaded", function () {
    const payment = document.getElementById("payment");
    const cardinfo = document.getElementById("cardinfo");
    const cc = document.getElementById("cc");
    const exp = document.getElementById("exp");
    const cvv = document.getElementById("cvv");

    payment.addEventListener("change", function () {
        if (payment.value === "credit") {
            cardinfo.style.display = "block";
            cc.setAttribute("name", "cc");
            exp.setAttribute("name", "exp");
            cvv.setAttribute("name", "cvv");
            cc.setAttribute("required", true);
            exp.setAttribute("required", true);
            cvv.setAttribute("required", true);
        } else {
            cardinfo.style.display = "none";
            cc.removeAttribute("name", "cc");
            exp.removeAttribute("name", "exp");
            cvv.removeAttribute("name", "cvv");
            cc.removeAttribute("required", true);
            exp.removeAttribute("required", true);
            cvv.removeAttribute("required", true);
        }
    });
});