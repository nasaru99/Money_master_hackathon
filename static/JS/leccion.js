
    // JavaScript para la navegación entre pasos
    const formSteps = document.querySelectorAll('.form-step');
    const prevStepButtons = document.querySelectorAll('.prev-step');
    const nextStepButtons = document.querySelectorAll('.next-step');

    // Ocultar todos los pasos excepto el primero
    formSteps.forEach((step, index) => {
        if (index === 0) {
            step.style.display = 'block';
        } else {
            step.style.display = 'none';
        }
    });

    // Función para mostrar el siguiente paso
    function showNextStep(currentStep) {
        currentStep.style.display = 'none';
        const nextIndex = Array.from(formSteps).indexOf(currentStep) + 1;
        if (nextIndex < formSteps.length) {
            formSteps[nextIndex].style.display = 'block';
        }
    }

    // Función para mostrar el paso anterior
    function showPrevStep(currentStep) {
        currentStep.style.display = 'none';
        const prevIndex = Array.from(formSteps).indexOf(currentStep) - 1;
        if (prevIndex >= 0) {
            formSteps[prevIndex].style.display = 'block';
        }
    }

    // Event listeners para los botones de navegación
    prevStepButtons.forEach(button => {
        button.addEventListener('click', () => {
            const currentStep = button.closest('.form-step');
            showPrevStep(currentStep);
        });
    });

    nextStepButtons.forEach(button => {
        button.addEventListener('click', () => {
            const currentStep = button.closest('.form-step');
            showNextStep(currentStep);
        });
    });

    const tipoContenidoField = document.getElementById("id_tipo_contenido");
    const contenidoTextoField = document.getElementById("id_contenido_texto");
    const contenidoImagenURLField = document.getElementById("id_contenido_imagen_url");
    const contenidoImagenArchivoField = document.getElementById("id_contenido_imagen_archivo");
    const contenidoVideoURLField = document.getElementById("id_contenido_video_url");
    const contenidoVideoArchivoField = document.getElementById("id_contenido_video_archivo");
    const contenidoRutaField = document.getElementById("id_contenido_ruta");

    // Función para mostrar u ocultar campos según el tipo de contenido seleccionado
    function mostrarOcultarCampos() {
        const tipoContenido = tipoContenidoField.value;

        contenidoTextoField.style.display = tipoContenido === "Texto" ? "block" : "none";
        contenidoImagenURLField.style.display = tipoContenido === "Imagen URL" ? "block" : "none";
        contenidoImagenArchivoField.style.display = tipoContenido === "Imagen Archivo" ? "block" : "none";
        contenidoVideoURLField.style.display = tipoContenido === "Video URL" ? "block" : "none";
        contenidoVideoArchivoField.style.display = tipoContenido === "Video Archivo" ? "block" : "none";
        contenidoRutaField.style.display = tipoContenido === "Ruta" ? "block" : "none";
    }

    // Agregar un evento de cambio para el campo "Tipo de Contenido"
    tipoContenidoField.addEventListener("change", mostrarOcultarCampos);

    // Llamar a la función al cargar la página para mostrar los campos iniciales
    mostrarOcultarCampos();