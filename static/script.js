const API_URL = '/api/libros';

function cargarLibros() {
  fetch(API_URL)
    .then(response => response.json())
    .then(data => {
      const tbody = document.getElementById('tabla-body');
      tbody.innerHTML = '';
      data.forEach(libro => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${libro.id}</td>
          <td>${libro.titulo}</td>
          <td>${libro.autor}</td>
          <td>
            <button class="btn" onclick="editarLibro(${libro.id})">Editar</button>
            <button class="btn" onclick="eliminarLibro(${libro.id})">Eliminar</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    });
}

function agregarLibro() {
  const titulo = document.getElementById('titulo').value;
  const autor = document.getElementById('autor').value;

  fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ titulo, autor })
  })
    .then(response => response.json())
    .then(() => {
      document.getElementById('titulo').value = '';
      document.getElementById('autor').value = '';
      cargarLibros();
    });
}

function editarLibro(id) {
  const titulo = prompt("Nuevo título:");
  const autor = prompt("Nuevo autor:");
  if (titulo && autor) {
    fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ titulo, autor })
    })
      .then(() => cargarLibros());
  }
}

function eliminarLibro(id) {
  if (confirm("¿Eliminar este libro?")) {
    fetch(`${API_URL}/${id}`, { method: 'DELETE' })
      .then(() => cargarLibros());
  }
}

cargarLibros();