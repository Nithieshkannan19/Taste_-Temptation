let order = [];  
let total = 0; 

function additem() {
  let item = document.getElementById("items").value;
  let qty = document.getElementById("qty").value;
  if (item === "Select") {
    alert("Please select an item.");
    return;
  }
  if (qty <= 0) {
    alert("Please enter a valid quantity.");
    return;
  }
  let price = getPrice(item);
  let amount = qty * price;
  order.push({"item": item, "quantity": qty, "amount": amount});
  total += amount;
  displayOrder();
  console.log("add Place order..")
}

function removeitem(index) {
  let item = order[index];
  console.log(item);
  total -= item.amount;
  order.splice(index, 1);
  displayOrder();
}

function displayOrder() {
  let table = document.getElementById("ordertable");
  table.innerHTML = "";  
  let row = table.insertRow();
  row.innerHTML = "<th>Item</th><th>Quantity</th><th>Amount</th><th>Action</th>";
  order.forEach(function(item, index) {
  row = table.insertRow();
  row.innerHTML = "<td>" + item.item + "</td><td>" + item.quantity + "</td><td>&#36;" + item.amount + "</td><td><button onclick=\"removeitem(" + index + ")\">Remove</button></td>";
});
  document.getElementById("totalprice").innerHTML = "TOTAL AMOUNT: &#36;" + total;
}

function getPrice(item) {
  switch(item) {
    case "Chicken Lollipop":
      return 12;
    case "Butter Chicken":
      return 16;
    case "Paneer Tikka":
      return 9;
    case "Chicken Soup":
      return 8;
    case "Corn Soup":
      return 6;
    case "Tomato Soup":
      return 5.50;
    case "Kothu Parotta":
      return 4.50; 
    case "Chilli Parota":
      return 4;
    case "Bun Parotta":
      return 1;
    case "Scrambled Egg":
      return 0.75;
    case "Half Boil":
      return 1.25;
    case "Egg Gravy":
      return 0.75;
    case "Masal Dosa":
      return 1.50;
    case "Ghee Roast":
      return 2.50;
    case "Paneer Dosa":
      return 3;
    case "Mutton Biriyani":
      return 9;
    case "Chicken Biriyani":
      return 8;
    case "Hyderabad Biriyani":
      return 8.50;
    case "Veg Noodles":
      return 5.25;
    case "Spl Noodles":
      return 6;
    case "Paneer Noodles":
      return 6.50;
    case "Mojito":
      return 2.25;
    case "Oreo Shake":
      return 3;
    case "Caramel Shake":
      return 2.75;
    default:
      return 0;
  }
}

function placeorder() {
    var totalprice = document.getElementById("totalprice");
    var totalamount = totalprice.innerHTML.split("$")[1];
    alert("Order placed successfully! Total amount: $" + totalamount);
    localStorage.setItem("totalAmt",totalamount);
    let xhr = new XMLHttpRequest();
    console.log("place order")
    xhr.open("POST", "/placeorder", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify({"order_items": order, "total_amount": total});
    xhr.send(data);
}