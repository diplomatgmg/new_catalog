const checkboxes = document.querySelectorAll('.family');
const searchInput = document.querySelector('#search');

function filterItems() {
    const query = searchInput.value.toLowerCase();

    checkboxes.forEach((checkbox) => {
        const label = checkbox.parentElement.textContent.toLowerCase();
        const match = label.includes(query);
        checkbox.closest('div').style.display = match ? 'block' : 'none';
    });
}

searchInput.addEventListener('input', filterItems);
