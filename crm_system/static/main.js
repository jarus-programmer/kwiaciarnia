document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');
    let hoverTimeout;
    
    dropdowns.forEach(dropdown => {
        const submenu = dropdown.querySelector('.submenu');
        
        dropdown.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            this.classList.add('active');
            submenu.style.display = 'block';
        });
        
        dropdown.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(() => {
                this.classList.remove('active');
                submenu.style.display = 'none';
            }, 300);
        });
        
        submenu.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
        });
        
        submenu.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(() => {
                dropdown.classList.remove('active');
                submenu.style.display = 'none';
            }, 200);
        });

        dropdown.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                this.classList.toggle('active');
                submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});