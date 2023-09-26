$(document).ready(function () {
    // Obtén el elemento select del Tipo de Contenido
    var tipoContenidoSelect = $('#id_tipo_contenido');
  
    // Obtén los elementos de los diferentes tipos de contenido
    var contenidoTexto = $('#contenido-texto');
    var contenidoImagenURL = $('#contenido-imagen-url');
    var contenidoImagenArchivo = $('#contenido-imagen-archivo');
    var contenidoVideoURL = $('#contenido-video-url');
    var contenidoVideoArchivo = $('#contenido-video-archivo');
    var contenidoRuta = $('#contenido-ruta');
  
    // Función para mostrar u ocultar los campos de contenido según la selección
    function actualizarCamposDeContenido() {
      var tipoContenidoSeleccionado = tipoContenidoSelect.val();
  
      // Oculta todos los campos de contenido
      contenidoTexto.hide();
      contenidoImagenURL.hide();
      contenidoImagenArchivo.hide();
      contenidoVideoURL.hide();
      contenidoVideoArchivo.hide();
      contenidoRuta.hide();
  
      // Muestra el campo de contenido correspondiente al Tipo de Contenido seleccionado
      if (tipoContenidoSeleccionado === 'Texto') {
        contenidoTexto.show();
      } else if (tipoContenidoSeleccionado === 'Imagen URL') {
        contenidoImagenURL.show();
      } else if (tipoContenidoSeleccionado === 'Imagen Archivo') {
        contenidoImagenArchivo.show();
      } else if (tipoContenidoSeleccionado === 'Video URL') {
        contenidoVideoURL.show();
      } else if (tipoContenidoSeleccionado === 'Video Archivo') {
        contenidoVideoArchivo.show();
      } else if (tipoContenidoSeleccionado === 'Ruta') {
        contenidoRuta.show();
      }
    }
  
    // Llama a la función para actualizar los campos de contenido cuando cambie la selección
    tipoContenidoSelect.change(actualizarCamposDeContenido);
  
    // Llama a la función inicialmente para configurar los campos de contenido según el valor predeterminado
    actualizarCamposDeContenido();
  });
  