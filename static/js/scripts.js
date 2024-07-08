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
            $(this).css('transform', 'scale(1)');
        }
    );

    // Confirm deletion of menu item
    $('form').on('submit', function() {
        return confirm('Are you sure you want to delete this item?');
    });
});

