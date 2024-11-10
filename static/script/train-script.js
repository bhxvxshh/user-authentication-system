const warpper = document.querySelector('warpper');
const busPage = document.querySelector('.train-page');
const nextBusPage = document.querySelector('.nx-btn');

function noSpaces(input) {
    if (input.value.indexOf(' ') !== -1) {
        alert('Spaces are not allowed in this field.');
        input.value = input.value.replace(/\s/g, ''); // Remove spaces
    }
}

nextBusPage.addEventListener('click',()=>{
    warpper.classList.add('active');
})

busPage.addEventListener('click',()=>{
    warpper.classList.remove('active');
})


