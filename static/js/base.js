// Navigation functionality
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navList = document.querySelector('.nav-list');
    const userMenu = document.querySelector('.user-menu');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    // Hamburger menu toggle
    hamburger?.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navList?.classList.toggle('active');
    });

    // User menu dropdown
    userMenu?.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu?.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        dropdownMenu?.classList.remove('active');
    });

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger?.classList.remove('active');
            navList?.classList.remove('active');
        });
    });
});

// Search form submission
const searchForm = document.querySelector('.search-form');
searchForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = document.querySelector('#query')?.value.trim();
    if (query) {
        // Handle search - you can implement your search logic here
        console.log('Searching for:', query);
    }
});