
document.addEventListener('DOMContentLoaded', function () {
    const hopitalSelect = document.getElementById('hopital');
    const serviceSelect = document.getElementById('service');

    hopitalSelect.addEventListener('change', function () {
        const hopitalId = this.value;
        serviceSelect.innerHTML = '<option value="">Chargement...</option>';

        if (hopitalId) {
            fetch(`/rapports/ajax/get-services/?hopital_id=${hopitalId}`)
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

