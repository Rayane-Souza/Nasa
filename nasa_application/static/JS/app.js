function showSection(sectionId) {
    // Remover a classe 'active' de todas as abas e seções
    const tabs = document.querySelectorAll('.tab-link');
    const sections = document.querySelectorAll('.section');

    tabs.forEach(tab => tab.classList.remove('active'));
    sections.forEach(section => section.classList.remove('active'));

    // Ativar a aba e a seção correspondente
    document.querySelector(`.tab-link[onclick="showSection('${sectionId}')"]`).classList.add('active');
    document.getElementById(sectionId).classList.add('active');
}
