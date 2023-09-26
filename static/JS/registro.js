// JavaScript para la navegación entre pasos
const formSteps = document.querySelectorAll('.tab');
const prevStepButtons = document.querySelectorAll('.prev');
const nextStepButtons = document.querySelectorAll('.next');

let currentStep = 0;

// Ocultar todos los pasos excepto el primero
formSteps.forEach((step, index) => {
    if (index === 0) {
        step.style.display = 'block';
    } else {
        step.style.display = 'none';
    }
});

// Función para mostrar el siguiente paso
function showNextStep() {
    formSteps[currentStep].style.display = 'none';
    currentStep++;
    if (currentStep < formSteps.length) {
        formSteps[currentStep].style.display = 'block';
    }
}

// Función para mostrar el paso anterior
function showPrevStep() {
    formSteps[currentStep].style.display = 'none';
    currentStep--;
    if (currentStep >= 0) {
        formSteps[currentStep].style.display = 'block';
    }
}

// Event listeners para los botones de navegación
prevStepButtons.forEach(button => {
    button.addEventListener('click', showPrevStep);
});

nextStepButtons.forEach(button => {
    button.addEventListener('click', showNextStep);
});


var currentTab = 0;
showTab(currentTab);

function showTab(n) {
  var tabs = document.getElementsByClassName("tab");
  tabs[n].style.display = "block";
  if (n == 0) {
    document.getElementsByClassName("prev")[0].style.display = "none";
  } else {
    document.getElementsByClassName("prev")[0].style.display = "inline";
  }
  if (n == (tabs.length - 1)) {
    document.getElementsByClassName("next")[0].innerHTML = "Registrarse";
  } else {
    document.getElementsByClassName("next")[0].innerHTML = "Siguiente";
  }
}

function nextPrev(n) {
  var tabs = document.getElementsByClassName("tab");
  if (n == 1 && !validateForm()) return false;
  tabs[currentTab].style.display = "none";
  currentTab = currentTab + n;
  if (currentTab >= tabs.length) {
    document.getElementById("registrationForm").submit();
    return false;
  }
  showTab(currentTab);
}

function validateForm() {
  // Agrega aquí tus validaciones de formulario si es necesario
  return true;
}
