const API_URL = "https://kiire-fallas-api.onrender.com";
const ADMIN_PASSWORD = "KiireFallas123!";

const loginForm = document.getElementById("adminLoginForm");
const loginMensaje = document.getElementById("loginMensaje");
const loginCard = document.getElementById("loginCard");
const adminPanel = document.getElementById("adminPanel");

const tabs = document.querySelectorAll(".admin-tab");
const sections = document.querySelectorAll(".admin-section");

const adminResponsableForm = document.getElementById("adminResponsableForm");
const adminResponsableMensaje = document.getElementById("adminResponsableMensaje");

const adminCierreForm = document.getElementById("adminCierreForm");
const adminCierreMensaje = document.getElementById("adminCierreMensaje");

const adminConsultaForm = document.getElementById("adminConsultaForm");
const adminConsultaMensaje = document.getElementById("adminConsultaMensaje");
const detalleTicket = document.getElementById("detalleTicket");

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const password = document.getElementById("adminPassword").value;

  if (password === ADMIN_PASSWORD) {
    loginMensaje.textContent = "";
    loginCard.style.display = "none";
    adminPanel.style.display = "block";
    return;
  }

  loginMensaje.textContent = "Contraseña incorrecta";
  loginMensaje.className = "message error";
});

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((btn) => btn.classList.remove("active"));
    sections.forEach((section) => {
      section.style.display = "none";
      section.classList.remove("active");
    });

    tab.classList.add("active");
    const target = document.getElementById(tab.dataset.target);
    target.style.display = "block";
    target.classList.add("active");
  });
});

adminResponsableForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const ticketId = document.getElementById("ticketIdResponsable").value.trim();
  const responsable = document.getElementById("nuevoResponsable").value.trim();
  const correo_responsable = document.getElementById("nuevoCorreoResponsable").value.trim();

  try {
    const response = await fetch(`${API_URL}/tickets/${ticketId}/responsable`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        responsable,
        correo_responsable
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "No se pudo actualizar el responsable");
    }

    adminResponsableMensaje.textContent = `Responsable actualizado correctamente para el ticket ${data.ticket_codigo}`;
    adminResponsableMensaje.className = "message success";
    adminResponsableForm.reset();
  } catch (error) {
    adminResponsableMensaje.textContent = error.message;
    adminResponsableMensaje.className = "message error";
  }
});

adminCierreForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const ticketId = document.getElementById("ticketIdCierre").value.trim();
  const observacion = document.getElementById("nuevaObservacionCierre").value.trim();

  try {
    const response = await fetch(`${API_URL}/tickets/${ticketId}/cerrar`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        observacion
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "No se pudo cerrar el caso");
    }

    adminCierreMensaje.textContent = `Caso cerrado correctamente para el ticket ${data.ticket_codigo}`;
    adminCierreMensaje.className = "message success";
    adminCierreForm.reset();
  } catch (error) {
    adminCierreMensaje.textContent = error.message;
    adminCierreMensaje.className = "message error";
  }
});

adminConsultaForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const ticketId = document.getElementById("ticketIdConsulta").value.trim();

  try {
    const response = await fetch(`${API_URL}/tickets/${ticketId}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "No se pudo consultar el ticket");
    }

    adminConsultaMensaje.textContent = "Ticket encontrado";
    adminConsultaMensaje.className = "message success";

    document.getElementById("d_id").textContent = data.id ?? "";
    document.getElementById("d_ticket_codigo").textContent = data.ticket_codigo ?? "";
    document.getElementById("d_nombre_reportante").textContent = data.nombre_reportante ?? "";
    document.getElementById("d_correo_reportante").textContent = data.correo_reportante ?? "";
    document.getElementById("d_comercio").textContent = data.comercio ?? "";
    document.getElementById("d_titulo_error").textContent = data.titulo_error ?? "";
    document.getElementById("d_producto").textContent = data.producto ?? "";
    document.getElementById("d_prioridad").textContent = data.prioridad ?? "";
    document.getElementById("d_descripcion").textContent = data.descripcion ?? "";
    document.getElementById("d_responsable").textContent = data.responsable ?? "";
    document.getElementById("d_correo_responsable").textContent = data.correo_responsable ?? "";
    document.getElementById("d_estado").textContent = data.estado ?? "";
    document.getElementById("d_observacion").textContent = data.observacion ?? "";
    document.getElementById("d_nit").textContent = data.nit ?? "";

    const imagenSpan = document.getElementById("d_imagen_url");
    if (data.imagen_url) {
      imagenSpan.innerHTML = `<a href="${data.imagen_url}" target="_blank" rel="noopener noreferrer">Ver imagen</a>`;
    } else {
      imagenSpan.textContent = "Sin imagen";
    }

    detalleTicket.style.display = "block";
  } catch (error) {
    adminConsultaMensaje.textContent = error.message;
    adminConsultaMensaje.className = "message error";
    detalleTicket.style.display = "none";
  }
});