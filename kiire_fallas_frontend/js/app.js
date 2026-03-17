const API_URL = "http://127.0.0.1:8000";

const ticketForm = document.getElementById("ticketForm");
const mensaje = document.getElementById("mensaje");
const ticketsBody = document.getElementById("ticketsBody");
const btnRecargar = document.getElementById("btnRecargar");

document.addEventListener("DOMContentLoaded", () => {
  cargarTickets();
});

btnRecargar.addEventListener("click", cargarTickets);

ticketForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData();
  formData.append("nombre_reportante", document.getElementById("nombre_reportante").value.trim());
  formData.append("correo_reportante", document.getElementById("correo_reportante").value.trim());
  formData.append("comercio", document.getElementById("comercio").value.trim());
  formData.append("titulo_error", document.getElementById("titulo_error").value.trim());
  formData.append("categoria", document.getElementById("categoria").value.trim());
  formData.append("prioridad", document.getElementById("prioridad").value);
  formData.append("descripcion", document.getElementById("descripcion").value.trim());

  const imagenInput = document.getElementById("imagen");
  if (imagenInput && imagenInput.files.length > 0) {
    formData.append("imagen", imagenInput.files[0]);
  }

  try {
    const response = await fetch(`${API_URL}/tickets`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "No se pudo crear el ticket");
    }

    const data = await response.json();
    mostrarMensaje(`Ticket creado correctamente: ${data.ticket_codigo}`, "success");
    ticketForm.reset();
    await cargarTickets();
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }
});

function mostrarMensaje(texto, tipo) {
  mensaje.textContent = texto;
  mensaje.className = `message ${tipo}`;
}

async function cargarTickets() {
  try {
    const response = await fetch(`${API_URL}/tickets`);

    if (!response.ok) {
      throw new Error("No se pudieron cargar los tickets");
    }

    const tickets = await response.json();
    renderizarTickets(tickets);
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }
}

function renderizarTickets(tickets) {
  ticketsBody.innerHTML = "";

  if (!tickets.length) {
    ticketsBody.innerHTML = `
      <tr>
        <td colspan="10">No hay tickets registrados.</td>
      </tr>
    `;
    return;
  }

  tickets.forEach((ticket) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${ticket.id}</td>
      <td>${ticket.ticket_codigo ?? ""}</td>
      <td>${ticket.comercio ?? ""}</td>
      <td>${ticket.titulo_error ?? ""}</td>
      <td>${ticket.prioridad ?? ""}</td>
      <td>${ticket.responsable ?? ""}</td>
      <td>${ticket.correo_responsable ?? ""}</td>
      <td><span class="estado-badge">${ticket.estado ?? ""}</span></td>
      <td>
        ${
          ticket.imagen_url
            ? `<a href="${ticket.imagen_url}" target="_blank" rel="noopener noreferrer">Ver imagen</a>`
            : "Sin imagen"
        }
      </td>
      <td>
        <span style="color: #6b7280;">Sin acciones</span>
      </td>
    `;

    ticketsBody.appendChild(tr);
  });
}