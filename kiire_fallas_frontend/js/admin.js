const API_URL = "https://kiire-fallas-api.onrender.com";
const ADMIN_PASSWORD = "KiireFallas123!";

const loginForm = document.getElementById("adminLoginForm");
const loginMensaje = document.getElementById("loginMensaje");
const loginCard = document.getElementById("loginCard");
const adminPanel = document.getElementById("adminPanel");

const adminForm = document.getElementById("adminForm");
const adminMensaje = document.getElementById("adminMensaje");

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

adminForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const ticketId = document.getElementById("ticketId").value.trim();
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

    adminMensaje.textContent = `Responsable actualizado correctamente para el ticket ${data.ticket_codigo}`;
    adminMensaje.className = "message success";
    adminForm.reset();
  } catch (error) {
    adminMensaje.textContent = error.message;
    adminMensaje.className = "message error";
  }
});