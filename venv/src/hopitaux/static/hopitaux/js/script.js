// Gestion des checkboxes
document.addEventListener('DOMContentLoaded', function() {
    const mainCheckbox = document.querySelector('th .checkbox');
    const rowCheckboxes = document.querySelectorAll('tbody .checkbox');
    const selectionInfo = document.querySelector('.selection-info');
            
    function updateSelectionCount() {
        const checkedCount = document.querySelectorAll('tbody .checkbox:checked').length;
        selectionInfo.textContent = `${checkedCount} sur 5 sélectionné`;
    }
            
    mainCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
            updateSelectionCount();
    });
            
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectionCount();
                    
            // Mettre à jour le checkbox principal
            const allChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
            const someChecked = Array.from(rowCheckboxes).some(cb => cb.checked);
                    
            mainCheckbox.checked = allChecked;
            mainCheckbox.indeterminate = someChecked && !allChecked;
        });
    });
});

function closeNav(){
    document.getElementById("mySidebar").style.width="0";
    document.querySelector("body").style.overflow= "auto"

}