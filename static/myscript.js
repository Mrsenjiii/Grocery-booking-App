let productCounts = {}; // Object to store counts for each product

function increment(productName) {
  if (!productCounts[productName]) {
    productCounts[productName] = 1;
  } else {
    productCounts[productName]++;
  }
  updateCartCount(productName);
}

function decrement(productName) {
  if (productCounts[productName] && productCounts[productName] > 0) {
    productCounts[productName]--;
    updateCartCount(productName);
  }
}

function updateCartCount(productName) {
  const cartButton = document.getElementById("cart" + productName);
  cartButton.innerText = `Add to Cart : ${productCounts[productName] || 0}`;


  const dataQuantityInput = document.getElementById("quantityof_" + productName);
  dataQuantityInput.value = productCounts[productName] || 0;
  cartButton.innerText = `Add to Cart : ${productCounts[productName] || 0}`;
}

function category_edit(category_id){
  var id = category_id
  // get the element to change the css 
  var box_to_view = document.getElementById("edit-box")
  // input for changing the value to category id here
  var input_val_change = document.getElementById("c_id");

  // Change the value of the input element
  input_val_change.value =  category_id;
  box_to_view.style.setProperty("display", "block", "important");

  // get the input element to change the input value to category id
}

function close_edit_category(){

  // get the element to change the css 
  var box_to_view = document.getElementById("edit-box")
  box_to_view.style.setProperty("display", "none", "important");

  // get the input element to change the input value to category id
}

function open_edit(){
 
  // get the element to change the css 
  var box_to_view = document.getElementById("edit-box")
  // input for changing the value to category id here
  

  // Change the value of the input element

  box_to_view.style.setProperty("display", "block", "important");

  // get the input element to change the input value to category id
}
