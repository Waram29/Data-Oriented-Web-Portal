document.addEventListener("DOMContentLoaded", function () {
  const pwd1 = document.getElementById("passwordInput");
  const pwd2 = document.getElementById("passwordInputConfirm");
  const toggle1 = document.getElementById("togglePassword");
  const toggle2 = document.getElementById("togglePasswordConfirm");

  if (toggle1 && pwd1) {
    toggle1.addEventListener("click", () => {
      const type = pwd1.type === "password" ? "text" : "password";
      pwd1.type = type;
      toggle1.classList.toggle("visible");
    });
  }

  if (toggle2 && pwd2) {
    toggle2.addEventListener("click", () => {
      const type = pwd2.type === "password" ? "text" : "password";
      pwd2.type = type;
      toggle2.classList.toggle("visible");
    });
  }
});


// Affichage dynamique des services par hopital
document.addEventListener('DOMContentLoaded', function () {
    const hopitalSelect = document.getElementById('hopital');
    const serviceSelect = document.getElementById('service');

    hopitalSelect.addEventListener('change', function () {
        const hopitalId = this.value;
        serviceSelect.innerHTML = '<option value="">Chargement...</option>';

        if (hopitalId) {
            fetch(`/comptes/ajax/get-services/?hopital_id=${hopitalId}`)
                .then(response => response.json())
                .then(data => {
                    serviceSelect.innerHTML = '<option value="">-- Sélectionner un service --</option>';
                    data.forEach(service => {
                        const option = document.createElement('option');
                        option.value = service.id;
                        option.textContent = service.nom;
                        serviceSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Erreur lors du chargement des services:', error);
                    serviceSelect.innerHTML = '<option value="">Erreur de chargement</option>';
                });
        } else {
            serviceSelect.innerHTML = '<option value="">-- Sélectionner un hôpital d’abord --</option>';
        }
    });
});
