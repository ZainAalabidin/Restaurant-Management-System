document.addEventListener('DOMContentLoaded', function () {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const totalPriceElement = document.querySelector('#total-price');

    quantityInputs.forEach(input => {
        input.addEventListener('input', updateTotalPrice);
    });

    function updateTotalPrice() {
        let totalPrice = 0;
        quantityInputs.forEach(input => {
            const price = parseFloat(input.dataset.price);
            const quantity = parseInt(input.value);
            if (!isNaN(price) && !isNaN(quantity)) {
                totalPrice += price * quantity;
            }
        });
        totalPriceElement.textContent = totalPrice.toFixed(2);
    }
    // Initial calculation
    updateTotalPrice();
});

$(document).ready(function(){
    console.log("Hello, welcome To Our Restaurant");
});

$(document).ready(function() {
    // Add hover effect for menu items
    $('.menu-item').hover(
        function() {
            $(this).css('transform', 'scale(1.02)');
        },
        function() {
            $(this).css('transform', 'scale(100)');
        }
    );

    // Confirm deletion of menu item
    $('form.del').on('submit', function() {
        return confirm('Are you sure you want to delete this item?');
    });
});
