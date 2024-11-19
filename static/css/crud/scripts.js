document.addEventListener('DOMContentLoaded', () => {
    const carritoLista = document.getElementById('carrito-lista');
    const totalElement = document.getElementById('total');
    let carrito = [];
    let total = 0;

    document.querySelectorAll('.agregar-carrito').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.target.getAttribute('data-id');
            const nombreProducto = e.target.parentElement.querySelector('.card-title').textContent;
            const precioProducto = parseFloat(e.target.parentElement.querySelector('.card-text').textContent.slice(1));

            carrito.push({ id, nombreProducto, precioProducto });
            total += precioProducto;

            // Actualizar carrito
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = `${nombreProducto} - $${precioProducto.toFixed(2)}`;
            carritoLista.appendChild(li);

            // Actualizar total
            totalElement.textContent = total.toFixed(2);
        });
    });
});
