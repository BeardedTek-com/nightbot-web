const btn = document.querySelector(".mobile-menu")
const menu = document.querySelector(".navmenu")

// Add Event Listener
btn.addEventListener("click", () =>{
menu.classList.toggle("hidden")
})

const modalEl = document.getElementById('info-popup');
const loginModal = new Modal(modalEl, {
    placement: 'center'
});



const closeModalEl = document.getElementById('close-modal');
closeModalEl.addEventListener('click', function() {
    loginModal.hide();
});
